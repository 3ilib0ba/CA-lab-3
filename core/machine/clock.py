# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
from enum import Enum


class Trace(str, Enum):
    """
    Trace type:
        - no    -- no trace
        - inst  -- trace every instruction
    """
    NO = 'no'
    INST = 'inst'


class ClockGenerator:
    """
    Clock Generator class
        - _tick  -- number of ticks
        - _inst  -- number of instructions
    """

    def __init__(self) -> None:
        self._tick = 0
        self._inst = 0

    def tick(self) -> None:
        self._tick += 1

    def inst(self) -> None:
        self._inst += 1

    def __str__(self) -> str:
        return f'tick: {self._tick}, inst: {self._inst}'
