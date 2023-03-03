# pylint: disable=missing-function-docstring
import sys

from core.machine.config import NULL_TERM


class IOController:
    """
    Input-Output Controller class
    """

    def putc_out(self, char: int) -> None:
        """
        Put symbol into stdout
        """
        sys.stdout.write(chr(char))

    def putc_err(self, char: int) -> None:
        """
        Put symbol into stderr
        """
        sys.stderr.write(chr(char))

    def getc(self) -> int:
        """
        Get symbol from stdint
        """
        char: str = sys.stdin.read(1)
        if char:
            return ord(char)
        return NULL_TERM
