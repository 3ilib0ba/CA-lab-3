# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
import pickle

from core.model import Program
from core.translator import minify_text, parse_code


def translate_asm_file(asm_file_name: str, object_file_name: str) -> None:
    """
    Translates .pyasm file to .pyasm.o object file
    :param asm_file_name: file name with source code
    :param object_file_name: filename of result object file
    """
    source_code: str = read_source_code(asm_file_name)
    minified_code: str = minify_text(source_code)
    program: Program = parse_code(minified_code)
    write_program_to_file(program, object_file_name)


def read_source_code(file_name: str) -> str:
    """
    Get the source code of .pyasm file
    :param file_name: file name with source code
    """
    with open(file_name, 'r', encoding='utf8') as asm_file:
        return asm_file.read()


def read_program_from_file(file_name: str) -> Program:
    """
    Unpickle program model from .pyasm.o object file
    :param file_name: filename of object file
    """
    with open(file_name, 'rb') as object_file:
        return pickle.load(object_file)


def write_program_to_file(program: Program, file_name: str) -> None:
    """
    Pickle program model and write it to .pyasm.o object file
    :param program: program to pickle
    :param file_name: object file name
    :return:
    """
    with open(file_name, 'wb') as object_file:
        pickle.dump(program, object_file, protocol=pickle.HIGHEST_PROTOCOL)
