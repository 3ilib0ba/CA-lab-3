# pylint: disable=missing-function-docstring
"""
Translating .pyasm code into object file
"""
import warnings
from typing import Iterator

from core.machine.config import NULL_TERM, STDIN, STDOUT, STDERR
from core.exceptions import (
    UndefinedInstruction, UndefinedLOC, UnexpectedOperand,
    UnexpectedDataValue, TextSectionNotFound, NoSuchLabel,
    OperandMustBeCharNotString, NotEnoughOperands
)
from core.machine.instruction_controller import InstructionController
from core.model import (
    Instruction, LOC, Label, Operand,
    Program, Address, DataSection, Constant,
    TextSection, Register, IndirectAddress
)
from core.translator.util import (
    is_number, is_string, is_register, is_label, convert_to_number,
    is_direct_address, is_indirect_address, regularize_string, is_instruction
)


def parse_operand(operand_str: str) -> Operand:
    """
    Get operand from string
    """
    if is_number(operand_str):
        return Constant(value=convert_to_number(operand_str))
    if is_string(operand_str):
        string: str = regularize_string(operand_str[1:-1])
        if len(string) != 1:
            raise OperandMustBeCharNotString(string)
        return Constant(value=ord(string))
    if is_register(operand_str):
        return Register(operand_str.upper()[1:])
    if is_indirect_address(operand_str):
        base, offset = operand_str.split('[')
        base = base[1:]
        offset = offset[:-1]
        return IndirectAddress(
            label=base,
            offset=parse_operand(offset)
        )
    if is_direct_address(operand_str):
        return Address(label=operand_str[1:])
    if is_label(operand_str):
        return Label(name=operand_str)

    raise UnexpectedOperand(f'"{operand_str}"')


def parse_operands(line: str) -> list[Operand]:
    """
    Get operand list from instruction
    """
    if not line:
        return []

    if ',' not in line:
        pass

    operands_str = map(str.strip, line.split(','))
    operands = map(parse_operand, operands_str)

    return list(operands)


def parse_instruction(line: str) -> Instruction:
    """
    Get instruction from line
    """
    cmd: str
    operands_str: str = ''

    if ' ' not in line:
        cmd = line
    else:
        cmd, operands_str = line.split(' ', 1)

    if not is_instruction(cmd):
        err_template: str = '-->{}<--'
        raise UndefinedInstruction(
            line.replace(cmd, err_template.format(cmd))
        )

    instruction: Instruction = Instruction(cmd.lower())
    operands: list[Operand] = parse_operands(operands_str)
    instruction.operands.extend(operands)
    instruction.sub = linearize_instruction(instruction)

    return instruction


def parse_line(line: str) -> Iterator[LOC]:
    """
    Generate LOC (instruction or label) from line
    Here can be:
        - Just a label
        - Just an instruction
        - A label with an instruction
    """
    label: str = ''
    instruction_str: str = line

    if ':' in line:
        label, instruction_str = map(str.strip, line.split(':', 1))

    if not is_label(label) and not instruction_str:
        raise UndefinedLOC(line)

    if is_label(label):
        yield Label(label)

    if instruction_str:
        yield parse_instruction(instruction_str)


def parse_data_line(line: str) -> tuple[str, list[Constant]]:
    """
    Get variable name and its value from data section
    """
    key, value = map(str.strip, line.split(':', 1))

    constant_mem: list[Constant]
    if value.startswith('buf '):
        _, count = value.split(None, 1)
        constant_mem = [Constant(0) for _ in range(int(count))]
    elif is_number(value):
        constant_mem = [Constant(value=convert_to_number(value))]
    elif is_string(value):
        string: str = value[1:-1]
        constant_mem = [
            Constant(value=ord(char))
            for char in regularize_string(string)
        ]
        constant_mem.append(Constant(value=NULL_TERM))
    else:
        raise UnexpectedDataValue(value)

    return key, constant_mem


def parse_data_section(code: str) -> DataSection:
    """
    Get data section from string
    """
    data: dict[str, int] = {
        'STDIN': STDIN,
        'STDOUT': STDOUT,
        'STDERR': STDERR
    }
    memory: list[int] = [
        0,
        0,
        0
    ]

    for line in code.splitlines():
        key, constant_mem = parse_data_line(line)
        if key in data:
            warnings.warn(f'Redefinition of variable "{key}"')
        data[key] = len(memory)
        memory.extend([constant.value for constant in constant_mem])

    return DataSection(
        var_to_addr=data,
        memory=memory
    )


def set_labels_indexes(
        lines: list[Instruction],
        labels: dict[str, int]
) -> None:
    """
    Set real addresses to instructions by label names
    """
    inst: Instruction
    for _, inst in enumerate(lines):
        operand: Operand
        for operand in inst.operands:
            if not isinstance(operand, Label):
                continue
            if operand.name not in labels:
                raise NoSuchLabel
            operand.value = labels[operand.name]


def parse_text_section(code: str) -> TextSection:
    """
    Get text (code) section from string
    """
    labels: dict[str, int] = {}
    lines: list[Instruction] = []

    line: str
    for line in code.splitlines():
        loc: LOC
        for loc in parse_line(line):
            if isinstance(loc, Label):
                if loc.name in labels:
                    warnings.warn(f'Redefinition of label "{loc.name}"')

                labels[loc.name] = len(lines)
            elif isinstance(loc, Instruction):
                lines.append(loc)
            else:
                raise TypeError(
                    f'Incorrect LOC type: {type(loc)}. '
                    f'Expected {LOC.__subclasses__()}'
                )

    set_labels_indexes(lines, labels)

    return TextSection(
        labels=labels,
        lines=lines
    )


def set_addresses_indexes(
        lines: list[Instruction],
        var_to_addr: dict[str, int]
) -> None:
    """
    Set real addresses to memory data by their names
    """
    inst: Instruction
    for inst in lines:
        operand: Operand
        for operand in inst.operands:
            if isinstance(operand, (Address, IndirectAddress)):
                operand.value = var_to_addr[operand.label]


_SECTION_TEXT = 'section .text'
_SECTION_DATA = 'section .data'

_TILL_THE_END = None


def parse_code(code: str) -> Program:
    """
    Get program from text
    """
    text_index: int = code.find(_SECTION_TEXT)
    if text_index == -1:
        raise TextSectionNotFound

    text_start, text_stop = text_index + len(_SECTION_TEXT) + 1, _TILL_THE_END

    data_index: int = code.find(_SECTION_DATA)
    if data_index == -1:
        return Program(
            text=parse_text_section(code[text_start:text_stop])
        )

    data_start, data_stop = data_index + len(_SECTION_DATA) + 1, _TILL_THE_END

    if text_index < data_index:
        text_stop = data_index - 1
    else:
        data_stop = text_index - 1

    program: Program = Program(
        data=parse_data_section(code[data_start:data_stop]),
        text=parse_text_section(code[text_start:text_stop])
    )

    set_addresses_indexes(program.text.lines, program.data.var_to_addr)

    return program


def linearize_instruction(instruction: Instruction) -> list[Instruction]:
    """
    Translate complex instruction into several simple instructions
    """
    if instruction.name in InstructionController.__reduce_ops__:
        operands: list[Operand] = instruction.operands
        op_num: int = len(operands)
        if op_num < 2:
            raise NotEnoughOperands

        if op_num == 2:
            return [Instruction(instruction.name, instruction.operands)]

        dest: Operand = operands[0]
        result: list[Instruction] = [
            Instruction('mov', [dest, operands[1]])
        ]
        for operand in operands[2:]:
            result.append(Instruction(
                instruction.name, [dest, operand]
            ))
        return result
    return []
