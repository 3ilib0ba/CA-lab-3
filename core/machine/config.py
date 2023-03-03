"""
Machine configuration
"""

BYTE = 8

# Word size
N_BITS = 32

# Minimum number
MIN_NUM = -2 ** (N_BITS - 1)

# Maximum number
MAX_NUM = 2 ** (N_BITS - 1) - 1

# Available data memory cells
MEMORY_SIZE = 256

# Null terminator (end of string)
NULL_TERM = 0x00

STDIN: int = 0
STDOUT: int = 1
STDERR: int = 2
