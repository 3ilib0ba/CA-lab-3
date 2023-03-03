# pylint: disable=missing-function-docstring
"""
Util-functions for working with data
"""

import re

from core.machine.instruction_controller import InstructionController
from core.machine.register_controller import RegisterController

RE_NEG = r'-?'
RE_HEX = r'0[xX][0-9a-fA-F]+'
RE_OCT = r'0[oO][0-7]+'
RE_BIN = r'0[bB][01]+'
RE_DEC = r'[0-9]+'
RE_PNM = rf'({RE_DEC}|{RE_BIN}|{RE_OCT}|{RE_HEX})'
RE_NUM = rf'{RE_NEG}{RE_PNM}'

RE_REG = r'|'.join(map(lambda reg: f'(%{reg})', RegisterController.keys()))

RE_OPR = rf'({RE_NUM})|({RE_REG})'

RE_LBL = r'\.?[a-zA-Z_]+'

RE_STR = r'^(\'.*\')|(\".*\")$'

RE_VAR = r'[a-zA-Z_][0-9a-zA-Z_]*'

RE_DAD = rf'#{RE_VAR}'
RE_IAD = rf'#{RE_VAR}\[({RE_OPR})\]'

RE_ILR = rf'\[({RE_VAR})([+-])({RE_REG})\]'
RE_IRG = rf'\[({RE_REG})\]'
RE_ADR = rf'({RE_DAD})|({RE_ILR})|({RE_IRG})'


def is_number(string: str) -> bool:
    """
    Check if string is hex, oct, bin or dec number
    """
    return bool(
        re.fullmatch(
            RE_NUM,
            string.upper()
        )
    )


def convert_to_number(string: str) -> int:
    """
    Convert hex, oct, bin or dec number into simple integer
    """
    string = string.upper()

    if re.match(rf'{RE_NEG}{RE_HEX}', string):
        return int(string, 16)
    if re.match(rf'{RE_NEG}{RE_OCT}', string):
        return int(string, 8)
    if re.match(rf'{RE_NEG}{RE_BIN}', string):
        return int(string, 2)
    if re.match(rf'{RE_NEG}{RE_DEC}', string):
        return int(string)

    return 0


def is_string(string: str) -> bool:
    """
    Check if string is symbols surrounded by quotes
    """
    return bool(
        re.fullmatch(
            RE_STR,
            string
        )
    )


def is_register(string: str) -> bool:
    """
    Check if there is register with such name
    """
    return bool(
        re.fullmatch(
            RE_REG,
            string.upper()
        )
    )


def is_instruction(string: str) -> bool:
    """
    Check if there is instruction with such name
    """
    return string.lower() in InstructionController.get_all()


def is_direct_address(string: str) -> bool:
    """
    Check if string is direct address
    """
    return bool(
        re.fullmatch(
            RE_DAD,
            string.upper()
        )
    )


def is_indirect_address(string: str) -> bool:
    """
    Check if string is indirect address
    """
    return bool(
        re.fullmatch(
            RE_IAD,
            string.upper()
        )
    )


def is_label(string: str) -> bool:
    """
    Check if string is label
    """
    return bool(
        re.fullmatch(
            RE_LBL,
            string.upper()
        )
    )


def regularize_string(string: str) -> str:
    """
    Replace escape characters
    """
    return (
        string
        .replace('\\n', '\n')
        .replace('\\t', '\t')
        .replace('\\r', '\r')
    )
