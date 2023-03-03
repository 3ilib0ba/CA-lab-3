# pylint: disable=missing-function-docstring
"""
Computer system containing:
    - clock generator
    - arithmetic logic unit
    - input-output controller
    - register controller
    - data memory controller
    - instruction controller
"""
from typing import Iterator

from core.machine.alu import ALU
from core.machine.clock import ClockGenerator, Trace
from core.exceptions import ProgramExit
from core.machine.instruction_controller import InstructionController
from core.machine.io_controller import IOController
from core.machine.memory_controller import MemoryController
from core.model import Program, TextSection
from core.machine.register_controller import RegisterController


class Computer:
    """
    Computer class
    """

    def __init__(self) -> None:
        self.clock = ClockGenerator()
        self.alu = ALU()
        self.io_controller = IOController()
        self.r_controller = RegisterController()
        self.m_controller = MemoryController(self.io_controller)
        self.instruction_executor = InstructionController(
            self.clock,
            self.alu,
            self.m_controller,
            self.r_controller
        )

    def execute_program(
            self,
            program: Program,
            trace: Trace
    ) -> Iterator['Computer']:
        """
        Execute given program
        """
        self.m_controller.load_data(program.data.memory)
        code: TextSection = program.text

        while (
                (pointer := self.r_controller.get_instruction_pointer())
                < len(code.lines)
        ):
            try:
                current_instruction = code.lines[pointer]
                gen: Iterator = (
                    self.instruction_executor.execute(current_instruction)
                )
                if trace == Trace.INST:
                    [*_] = gen
                    yield self
                else:
                    [*_] = gen
            except ProgramExit:
                return

    def __str__(self):
        lines: list[str] = [
            f'- INS: {self.instruction_executor.current}'
        ]
        if self.instruction_executor.current_sub:
            lines.append(f'- SUB: {self.instruction_executor.current_sub}')
        lines.append(f'- REG: {self.r_controller}')
        lines.append(f'- ALU: {self.alu}')
        lines.append(f'- CLK: {self.clock}')
        return '\n'.join(lines)
