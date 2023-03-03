
import sys
from typing import Optional, Type

import typer

from core.exceptions import PyAsmException, CatchPyAsmException
from core.file_helper import translate_asm_file, read_program_from_file
from core.model import Program
from core.machine import Computer, Trace

app = typer.Typer(help='PyAsm Runner')


def print_exception(error: PyAsmException) -> None:
    """
    Print PyAsmException message in stderr
    """
    exc_type: Type[PyAsmException] = type(error)
    typer.echo(
        typer.style(
            f'{exc_type.__name__}: {error!s}',
            fg=typer.colors.RED
        ), err=True
    )


@app.command(name="translate")
def translate(
        asm_file_name: str,
        object_file_name: Optional[str] = typer.Option(
            None, '--output', '-o'
        )
) -> None:
    """
    Translate .asm code to object file
    """
    if object_file_name is None:
        object_file_name = f'{asm_file_name}.o'

    with CatchPyAsmException() as catcher:
        translate_asm_file(asm_file_name, object_file_name)
    if catcher.exception:
        print_exception(catcher.exception)
        sys.exit(1)


@app.command(name="exec")
def execute(
        obj_file_name: str,
        trace: Trace = typer.Option(
            Trace.NO, '--trace', '-t', case_sensitive=False
        )
) -> None:
    """
    Execute object file
    """
    program: Program = read_program_from_file(obj_file_name)
    computer: Computer = Computer()
    with CatchPyAsmException() as catcher:
        for ex in computer.execute_program(program, trace):
            if not trace:
                continue
            print(ex, file=sys.stderr, end='\n\n')
    if catcher.exception:
        print_exception(catcher.exception)
        sys.exit(1)


@app.command(name="run")
def run(
        asm_file_name: str,
        object_file_name: Optional[str] = typer.Option(
            None, '--output', '-o'
        ),
        trace: Trace = typer.Option(
            Trace.NO, '--trace', '-t', case_sensitive=False
        )
) -> None:
    """
    Translate and execute .pyasm file
    """
    if object_file_name is None:
        object_file_name = f'{asm_file_name}.o'

    translate(asm_file_name, object_file_name)
    execute(object_file_name, trace)


if __name__ == '__main__':
    app()
