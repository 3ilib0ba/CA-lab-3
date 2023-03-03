"""
Preprocessing assembly code

Probably it's not a good decision, because we couldn't
definitely determine row and column of error or warning
"""

import re


def _remove_comment(line: str) -> str:
    """
    Removes assembly comments
    """
    return re.sub(r';.*', '', line)


def _remove_extra_spaces(line: str) -> str:
    """
    Removes extra sequential spaces
    """
    return re.sub(r'\s+', ' ', line)


def minify_text(asm_text: str) -> str:
    """
    Minifies assembly code

    - removes comments
    - strips lines
    - removes empty lines
    - removes extra sequential spaces
    """
    lines: list[str] = asm_text.splitlines()

    remove_comments = map(_remove_comment, lines)
    strip_lines = map(str.strip, remove_comments)
    remove_empty_lines = filter(bool, strip_lines)
    remove_extra_spaces = map(_remove_extra_spaces, remove_empty_lines)

    minified_text: str = '\n'.join(remove_extra_spaces)
    return minified_text
