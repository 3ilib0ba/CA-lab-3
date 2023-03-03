# pylint: disable=missing-function-docstring
from dataclasses import dataclass, field
from typing import TypeAlias


class Operand:
    """
    Operand base class. It can be:
        - Address
        - Constant
        - Label
        - IndirectAddress
        - Register
    """
    value: int

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class Constant(Operand):
    """
    Read-only integer value
    """
    value: int


@dataclass
class RegisterInfo:
    """
    Information about register
        - can_read  -- register is readable
        - can_write -- register is writable
    """
    can_read: bool
    can_write: bool


@dataclass
class Register(Operand):
    """
    Register model for translator.
        'RAX' -> Register('RAX')

    Available registers declared in core.machine.registers
    """
    name: str

    def __str__(self) -> str:
        return f'%{self.name}'


@dataclass
class Address(Operand):
    """
    Direct address model
        - value -- real address in data memory
        - label -- link to data memory address
    """
    value: int = -1
    label: str = ''

    def __str__(self) -> str:
        return f'#{self.label}'


@dataclass
class IndirectAddress(Operand):
    """
    Indirect address model
        - label     -- link to base data memory address
        - offset    -- offset operand that is being computed in runtime
    """
    offset: Operand
    label: str = ''

    def __str__(self) -> str:
        return f'#{self.label}[{self.offset}]'


class LOC:
    """
    Base model for .text section line. It can be:
        - Label
        - Instruction
    """


@dataclass
class Label(LOC, Operand):
    """
    Label model
        - name  --  link name to code section
        - value --  real address in code section
    """
    name: str
    value: int = -1

    def __str__(self) -> str:
        return self.name


@dataclass
class Instruction(LOC):
    """
    Instruction model
        - name      -- name of instruction
        - operands  -- list of operands this instruction uses
    """
    name: str
    operands: list[Operand] = field(default_factory=list)
    sub: list['Instruction'] = field(default_factory=list)

    def __str__(self) -> str:
        op_str: str = ', '.join(map(str, self.operands))
        return f'{self.name.upper()} {op_str}'


@dataclass
class DataSection:
    """
    section .data model (Data)
        - var_to_addr   -- hash-table {label: real_data_address}
        - memory        -- plain data memory of integer values
    """
    var_to_addr: dict[str, int] = field(default_factory=dict)
    memory: list[int] = field(default_factory=list)


@dataclass
class TextSection:
    """
    section .text model (Code)
        - labels    -- hash-table {label: real_code_address}
        - lines     -- array of instructions to execute
    """
    labels: dict[str, int] = field(default_factory=dict)
    lines: list[Instruction] = field(default_factory=list)


@dataclass
class Program:
    """
    Program model
        - data  -- section .data (Data)
        - text  -- section .text (Code)
    """
    data: DataSection = field(default_factory=DataSection)
    text: TextSection = field(default_factory=TextSection)


Destination: TypeAlias = Address | IndirectAddress | Register
Source: TypeAlias = Address | IndirectAddress | Register | Constant
