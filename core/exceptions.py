from types import TracebackType
from typing import Type, Literal, Optional


class PyAsmException(Exception):
    """
    Base Exception class
    """


class UndefinedInstruction(PyAsmException):
    """
    Raised when there is no such instruction
    """


class UndefinedLOC(PyAsmException):
    """
    Raised when translator can't classify line as Label or Instruction
    """


class UnexpectedOperand(PyAsmException):
    """
    Raised when translator couldn't parse operand
    """


class UnexpectedArguments(PyAsmException):
    """
    Raised when instruction argument type doesn't match expected
    """


class NotEnoughOperands(PyAsmException):
    """
    Raised when instruction needs more operands
    """


class UnexpectedDataValue(PyAsmException):
    """
    Raised when data value is neither number nor string
    """


class TextSectionNotFound(PyAsmException):
    """
    Raised when
        section .text
    in assembly code not found
    """


class DataNotFound(PyAsmException):
    """
    Raised when variable in data section not found
    """


class IncorrectDataType(PyAsmException):
    """
    Raised when needed data has another type
    """


class OperandIsNotWriteable(PyAsmException):
    """
    Raised when trying to write in constant
    """


class NoSuchLabel(PyAsmException):
    """
    Raised when translator can not find label
    """


class ProgramExit(PyAsmException):
    """
    End of program
    """


class NumberOutOfRange(PyAsmException):
    """
    Raised when number in code is out of range
    """


class OperandMustBeCharNotString(PyAsmException):
    """
    Raised when string length is greater than one
    """


class NotEnoughMemory(PyAsmException):
    """
    Raised when not enough memory to load program data
    """


class ALUZeroDivisionError(PyAsmException):
    """
    Raised when ALU tries to divide by zero
    """


class RegisterIsNotReadable(PyAsmException):
    """
    Raised when trying to write into not-readable register
    """


class RegisterIsNotWritable(PyAsmException):
    """
    Raised when trying to write into not-writable register
    """


class CatchPyAsmException:
    """
    Context manager that handles unexpected exceptions
    """

    def __init__(self):
        self.exception: Optional[PyAsmException] = None

    def __enter__(self) -> 'CatchPyAsmException':
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> Optional[Literal[True]]:
        if exc_val and isinstance(exc_val, PyAsmException):
            self.exception = exc_val
        elif exc_val and exc_type:
            tb_info: str = exc_tb and str(exc_tb.tb_frame) or "<None>"
            self.exception = PyAsmException(
                f'Unhandled exception.\n'
                f'\t{exc_type.__name__}: {str(exc_val)}\n'
                f'\tInformation: {tb_info}'
            )

        return True
