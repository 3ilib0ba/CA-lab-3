# pylint: disable=missing-function-docstring
from core.exceptions import DataNotFound, NotEnoughMemory
from core.machine.io_controller import IOController
from core.model import Address

from core.machine.alu import _strip_number
from core.machine.config import MEMORY_SIZE, STDIN, STDOUT, STDERR


class MemoryController:
    """
    Memory Controller class allows to work with data
    """

    def __init__(self, io_controller: IOController) -> None:
        self._memory: list[int] = [
            0 for _ in range(MEMORY_SIZE)
        ]
        self.io_controller = io_controller

    def load_data(self, program_data: list[int]) -> None:
        """
        Load program data into memory
        """
        data_amount: int = len(program_data)
        if data_amount > MEMORY_SIZE:
            raise NotEnoughMemory(
                f"Memory size: {MEMORY_SIZE}, "
                f"program data size: {data_amount}"
            )
        self._memory[:data_amount] = program_data

    def _check_bounds(self, address: Address) -> None:
        """
        Check if address value is correct.
        If not raise DataNotFound exception
        """
        if not 0 <= address.value <= len(self._memory):
            raise DataNotFound(
                f'Cannot get address {address.value}'
            )

    def get(self, address: Address) -> int:
        """
        Check address bounds and get value
        """
        self._check_bounds(address)
        if address.value == STDIN:
            self._memory[address.value] = self.io_controller.getc()
        return self._memory[address.value]

    def set(self, address: Address, value: int) -> None:
        """
        Check address and set value
        """
        self._check_bounds(address)
        self._memory[address.value] = _strip_number(value)
        if address.value == STDOUT:
            self.io_controller.putc_out(self._memory[address.value])
        elif address.value == STDERR:
            self.io_controller.putc_err(self._memory[address.value])

    def __repr__(self) -> str:
        return str(self._memory)
