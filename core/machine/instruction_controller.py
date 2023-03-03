# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
import operator
from types import UnionType
from typing import Callable, Optional, Iterator, Iterable

from core.machine.alu import ALU, Flag
from core.machine.clock import ClockGenerator
from core.exceptions import (
    OperandIsNotWriteable, ProgramExit
)
from core.machine.config import NULL_TERM
from core.machine.memory_controller import MemoryController
from core.model import (
    Address, Register, Label, Operand, Instruction,
    Destination, Source, IndirectAddress
)
from core.machine.register_controller import RegisterController


class InstructionController:
    """
    Instruction Controller class
        - current       -- the current executing instruction
        - current_sub   -- the current executing sub instruction
    """

    __reduce_ops__ = {
        'add', 'sub', 'mul', 'div',
        'mod', 'xor', 'and', 'or',
    }

    def __init__(
            self,
            clock: ClockGenerator,
            alu: ALU,
            memory: MemoryController,
            registers: RegisterController
    ) -> None:
        self.current: Optional[Instruction] = None
        self.current_sub: Optional[Instruction] = None

        self.clock = clock
        self.alu = alu
        self.memory = memory
        self.registers = registers

    def get_operand_value(self, operand: Operand) -> int:
        """
        Get operand value.
            - Indirect Address: shift address and work like with direct
            - Direct Address: get value with MemoryController
            - Register: get value with RegisterController
            - Label: get index
            - Constant: just get value
        """
        if isinstance(operand, IndirectAddress):
            offset: int = self.get_operand_value(operand.offset)
            return self.memory.get(
                Address(
                    label=operand.label,
                    value=(operand.value + offset)
                )
            )
        if isinstance(operand, Address):
            return self.memory.get(operand)
        if isinstance(operand, Register):
            return self.registers.get(operand)
        return operand.value

    def set_operand_value(self, operand: Operand, value: int) -> None:
        """
        Set operand value.
            - Indirect Address: shift address and work like with direct
            - Direct Address: set value with MemoryController
            - Register: set value with RegisterController
            - Other: throw OperandIsNotWriteable
        """
        if isinstance(operand, IndirectAddress):
            offset: int = self.get_operand_value(operand.offset)
            self.memory.set(
                Address(
                    label=operand.label,
                    value=(operand.value + offset)
                ), value
            )
        elif isinstance(operand, Address):
            self.memory.set(operand, value)
        elif isinstance(operand, Register):
            self.registers.set(operand, value)
        else:
            raise OperandIsNotWriteable(operand.value)

    def _same_bus(self, op1: Operand, op2: Operand) -> bool:
        """
        Check if operands fetching require the same bus:
            - memory bus
            - register bus
        """
        return (
                isinstance(op1, (Address, IndirectAddress)) and
                isinstance(op2, (Address, IndirectAddress))
        ) or (
                isinstance(op1, Register) and isinstance(op2, Register)
        )

    def _jump_to(self, label: Label) -> None:
        """
        Set instruction pointer to label value
        """
        self.registers.set_instruction_pointer(label.value - 1)

    def _reduce_op(
            self,
            reducer: Callable,
            dest: Destination,
            *operands: Source
    ) -> Iterator:
        """
        Defines operation behavior applying reducer function to operands
            - Two operands.
                Apply reducer to them and save result into "dest"
            - Three and more operands.
                Apply reducer to "*operands" and save result into "dest"
        """
        operand: Source = operands[0]
        op1: int = self.get_operand_value(dest)
        # if operands require the same bus
        if self._same_bus(dest, operand):
            self.clock.tick()
            yield
        op2: int = self.get_operand_value(operand)
        self.clock.tick()
        yield
        result = self.alu.operation(reducer, op1, op2)
        self.clock.tick()
        yield
        self.set_operand_value(dest, result)

    def _jmp_if(self, label: Label, condition: bool) -> None:
        """
        Jump to label if condition is True
        """
        if condition:
            self._jump_to(label)

    def i_add(self, dest: Destination, *ops: Source) -> Iterator:
        """
        ADD dest, *ops

        Sum operands amd save into dest
            - ADD A, B
                A = A + B
            - ADD A, B, C, D
                A = ((B + C) + D)
        """
        yield from self._reduce_op(operator.add, dest, *ops)

    def i_sub(self, dest: Destination, *ops: Source) -> Iterator:
        """
        SUB dest, *ops

        Subtract operands amd save into dest.
            - SUB A, B
                A = A - B
            - SUB A, B, C, D
                A = ((B - C) - D)
        """
        yield from self._reduce_op(operator.sub, dest, *ops)

    def i_mul(self, dest: Destination, *ops: Source) -> Iterator:
        """
        MUL dest, *ops

        Multiply operands amd save into dest
            - MUL A, B
                A = A * B
            - MUL A, B, C, D
                A = ((B * C) * D)
        """
        yield from self._reduce_op(operator.mul, dest, *ops)

    def i_div(self, dest: Destination, *ops: Source) -> Iterator:
        """
        DIV dest, *ops

        Divide (floor) operands amd save into dest.
            - DIV A, B
                A = A / B
            - DIV A, B, C, D
                A = ((B / C) / D)

        Can raise ALUDZeroDivisionError
        """
        yield from self._reduce_op(operator.floordiv, dest, *ops)

    def i_mod(self, dest: Destination, *ops: Source) -> Iterator:
        """
        MOD dest, *ops

        Modulo divide operands amd save into dest.
            - MOD A, B
                A = A % B
            - MOD A, B, C, D
                A = ((B % C) % D)

        Can raise ALUDZeroDivisionError
        """
        yield from self._reduce_op(operator.mod, dest, *ops)

    def i_xor(self, dest: Destination, *ops: Source) -> Iterator:
        """
        XOR dest, *ops

        Apply logical XOR to operands amd save into dest
            - XOR A, B
                A = A ^ B
            - XOR A, B, C, D
                A = ((B ^ C) ^ D)
        """
        yield from self._reduce_op(operator.xor, dest, *ops)

    def i_and(self, dest: Destination, *ops: Source) -> Iterator:
        """
        AND dest, *ops

        Apply logical AND to operands amd save into dest
            - AND A, B
                A = A & B
            - AND A, B, C, D
                A = ((B & C) & D)
        """
        yield from self._reduce_op(operator.and_, dest, *ops)

    def i_or(self, dest: Destination, *ops: Source) -> Iterator:
        """
        OR dest, *ops

        Apply logical OR to operands amd save into dest
            - OR A, B
                A = A | B
            - OR A, B, C, D
                A = ((B | C) | D)
        """
        yield from self._reduce_op(operator.or_, dest, *ops)

    def i_dec(self, dest: Destination) -> Iterator:
        """
        DEC dest

        Decrement (-1) operand
        """
        value: int = self.get_operand_value(dest)
        self.clock.tick()
        yield
        self.set_operand_value(dest, value - 1)

    def i_inc(self, dest: Destination) -> Iterator:
        """
        INC dest

        Increment (+1) operand
        """
        value: int = self.get_operand_value(dest)
        self.clock.tick()
        yield
        self.set_operand_value(dest, value + 1)

    def i_jmp(self, label: Label) -> None:
        """
        JMP label

        Jump to label without condition
        """
        self._jump_to(label)

    def i_je(self, label: Label) -> None:
        """
        JE label

        Jump to label if Z Flag is set (operands are equal)
        """
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.Z)
        )

    def i_jne(self, label: Label) -> None:
        """
        JE label

        Jump to label if Z Flag is not set (operands are not equal)
        """
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.Z)
        )

    def i_jl(self, label: Label) -> None:
        """
        JL label

        Jump to label if N Flag is set (first < second)
        """
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.N)
        )

    def i_jg(self, label: Label) -> None:
        """
        JL label

        Jump to label if N Flag is not set (first > second)
        """
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.N)
        )

    def i_jle(self, label: Label) -> None:
        """
        JLE label

        Jump to label if Z or N flag is set (first <= second)
        """
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    self.alu.get_flag(Flag.N)
            )
        )

    def i_jge(self, label: Label) -> None:
        """
        JGE label

        Jump to label if Z or not N flag is set (first >= second)
        """
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    not self.alu.get_flag(Flag.N)
            )
        )

    def i_mov(self, dest: Destination, src: Source) -> Iterator:
        """
        MOV dest, src

        Move value from src to dest

        If dest is #STDOUT or #STDERR then src value
        will be written in stdout or stderr respectively
        """
        value: int = self.get_operand_value(src)
        self.clock.tick()
        yield
        self.set_operand_value(dest, value)

    def i_movn(self, dest: Address, src: Source) -> Iterator:
        """
        MOVN dest, src

        Move number value from src to #STDOUT or #STDERR
        """
        value: int = self.get_operand_value(src)
        self.clock.tick()
        yield
        for digit in str(value):
            self.set_operand_value(dest, ord(digit))
            self.clock.tick()
            yield

    def i_ldn(self, dest: Address, src: Source) -> Iterator:
        """
        LDN dest, src

        Get number value from #STDIN and write into dest
        """
        result: str = ''
        while (digit := self.get_operand_value(src)) != NULL_TERM:
            result += chr(digit)
            self.clock.tick()
            yield
        self.set_operand_value(dest, int(result))

    def i_cmp(self, var: Source, src: Source) -> Iterator:
        """
        CMP op1, op2

        Compare two operands by subtracting and set flags
        """
        op1: int = self.get_operand_value(var)
        # if operands require the same bus
        if self._same_bus(var, src):
            self.clock.tick()
            yield
        op2: int = self.get_operand_value(src)
        self.clock.tick()
        yield
        self.alu.operation(operator.sub, op1, op2)

    def i_hlt(self) -> Iterator:
        """
        HLT

        Stop execution
        """
        self.clock.tick()
        yield
        raise ProgramExit

    def __execute(self, instruction: Instruction) -> Iterator | None:
        result = self.get_all()[instruction.name](
            self, *instruction.operands
        )
        if isinstance(result, Iterable):
            yield from result

    def execute(self, instruction: Instruction) -> Iterator:
        """
        Execute instruction by its name
        """
        self.current = instruction
        self.current_sub = None

        if self.current.sub:
            for sub_instruction in self.current.sub:
                self.current_sub = sub_instruction
                result = self.__execute(sub_instruction)
                if isinstance(result, Iterable):
                    yield from result
        else:
            result = self.__execute(instruction)
            if isinstance(result, Iterable):
                yield from result

        # increment instruction pointer (next instruction)
        self.registers.set_instruction_pointer(
            self.registers.get_instruction_pointer() + 1
        )
        # increment ticks and instructions after execution
        self.clock.tick()
        self.clock.inst()
        yield

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        """
        Get dict with available instruction
        :return {instruction_name: instruction_executor_function}
        """
        return {
            key.replace('i_', ''): func
            for key, func in cls.__dict__.items()
            if key.startswith('i_')
        }


def generate_instruction_docs() -> None:
    """
    Generate documentation for pyasm instructions
    """
    doc_instructions: list[str] = [
        '### Instructions\n'
    ]
    for name, function in InstructionController.get_all().items():
        doc_instructions.append(f'#### {name}\n')
        docstring = function.__doc__
        if docstring:
            docstring = docstring.strip()
        doc_instructions.append(
            '```\n'
            f'{docstring}\n'
            '```\n'
        )
        for key, value in function.__annotations__.items():
            if isinstance(value, type):
                value = value.__name__
            elif isinstance(value, UnionType):
                value = ' | '.join(x.__name__ for x in value.__args__)
            doc_instructions.append(f'- **{key}**: `{value}`\n')

    with open('../../resources/instructions.md', 'w', encoding='utf8') as file:
        file.writelines(doc_instructions)


if __name__ == '__main__':
    generate_instruction_docs()
