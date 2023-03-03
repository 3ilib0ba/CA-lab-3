from enum import Enum
from typing import Callable

from core.machine.config import MIN_NUM, MAX_NUM, N_BITS


class Flag(Enum):
    N = 0
    Z = 1
    V = 2
    C = 3


def _strip_number(value: int | str) -> int:
    """
    Convert char or big integer to N_BITS-format
    """
    if isinstance(value, str):
        value = ord(value)

    return (
            (-1) ** _get_sign(value) *
            (value & ((1 << N_BITS) - 1))
    )


def _get_zero(number: int) -> bool:
    """
    Check number if it's zero
    """
    return (number & ((1 << N_BITS) - 1)) == 0


def _get_overflow(number: int) -> bool:
    """
    Check number if it's not in [MIN_NUM; MAX_NUM] range
    """
    return not MIN_NUM <= number <= MAX_NUM


def _get_sign(number: int) -> bool:
    """
    Check number if it's negative
    """
    return bool(number & (1 << (N_BITS - 1)))


def _get_carry(number: int) -> bool:
    """
    Check if the number's (N_BITS)-th bit is set
    """
    if number < 0:
        return not bool(number & (1 << N_BITS))
    return bool(number & (1 << N_BITS))


class ALU:
    """
    Arithmetic Logic Unit
    """

    def __init__(self) -> None:
        self.flags: dict[str, bool] = {
            flag: False
            for flag in Flag.__members__
        }

    def set_flag(self, flag: Flag, value: bool) -> None:
        """
        Make flag equal to value
        """
        self.flags[flag.name] = value

    def get_flag(self, flag: Flag) -> bool:
        """
        Get flag value
        """
        return self.flags[flag.name]

    def operation(
            self,
            operation: Callable,
            first: int,
            second: int
    ) -> int:
        """
        Perform operation with two numbers and set flags
        """
        result: int = operation(first, second)
        self.set_flag(Flag.N, _get_sign(result))
        self.set_flag(Flag.Z, _get_zero(result))
        self.set_flag(Flag.V, _get_overflow(result))
        self.set_flag(Flag.C, _get_carry(result))
        return _strip_number(result)

    def __str__(self) -> str:
        return str(self.flags)
