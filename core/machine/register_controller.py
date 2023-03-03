from typing import Iterator

from core.exceptions import RegisterIsNotWritable, RegisterIsNotReadable
from core.machine.alu import _strip_number
from core.model import RegisterInfo, Register


def _register_data():
    """
    Get register info for data registers:
        - Readable
        - Writable
        - 4 bytes
    """
    return RegisterInfo(
        can_read=True,
        can_write=True
    )


def _register_pointer():
    """
    Get register info for pointer registers:
        - Readable
        - Not writable
        - 4 bytes
    """
    return RegisterInfo(
        can_read=True,
        can_write=False
    )


def _register_index():
    """
    Get register info for index registers:
        - Readable
        - Writable
    """
    return RegisterInfo(
        can_read=True,
        can_write=True
    )


__available_registers__: dict[str, RegisterInfo] = {
    'RAX': _register_data(),
    'RBX': _register_data(),
    'RDX': _register_data(),
    'RSX': _register_data(),

    'RIP': _register_pointer(),

    'RSI': _register_index(),
    'RDI': _register_index(),
}


class RegisterController:
    """
    Register Controller class
    """

    def __init__(self) -> None:
        """
        Initialize states for registers
        """
        self.__states__: dict[str, int] = {
            register: 0 for register in self.keys()
        }

    def get(self, register: Register) -> int:
        """
        Get readable register value
        """
        if not self.is_readable(register.name):
            raise RegisterIsNotReadable
        return self.__states__[register.name]

    def set(self, register: Register, value: int) -> None:
        """
        Set writable register value
        """
        if not self.is_writable(register.name):
            raise RegisterIsNotWritable
        self.__states__[register.name] = _strip_number(value)

    def get_instruction_pointer(self) -> int:
        """
        Get instruction pointer value
        """
        return self.__states__['RIP']

    def set_instruction_pointer(self, pointer: int) -> None:
        """
        Set instruction pointer value
        """
        self.__states__['RIP'] = pointer

    @staticmethod
    def is_readable(register_name: str) -> bool:
        """
        Check if register is readable
        """
        return __available_registers__[register_name].can_read

    @staticmethod
    def is_writable(register_name: str) -> bool:
        """
        Check if register is writable
        """
        return __available_registers__[register_name].can_write

    @staticmethod
    def contains(register_name: str) -> bool:
        """
        Check if here is register with such name
        """
        return register_name in RegisterController.keys()

    @staticmethod
    def keys() -> Iterator[str]:
        """
        Generate names of available registers
        """
        yield from __available_registers__

    def __repr__(self) -> str:
        return str(self.__states__)
