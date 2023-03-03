### Инструкции
#### add
```
ADD dest, *ops

        Sum operands amd save into dest
            - ADD A, B
                A = A + B
            - ADD A, B, C, D
                A = ((B + C) + D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### sub
```
SUB dest, *ops

        Subtract operands amd save into dest.
            - SUB A, B
                A = A - B
            - SUB A, B, C, D
                A = ((B - C) - D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### mul
```
MUL dest, *ops

        Multiply operands amd save into dest
            - MUL A, B
                A = A * B
            - MUL A, B, C, D
                A = ((B * C) * D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### div
```
DIV dest, *ops

        Divide (floor) operands amd save into dest.
            - DIV A, B
                A = A / B
            - DIV A, B, C, D
                A = ((B / C) / D)

        Can raise ALUDZeroDivisionError
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### mod
```
MOD dest, *ops

        Modulo divide operands amd save into dest.
            - MOD A, B
                A = A % B
            - MOD A, B, C, D
                A = ((B % C) % D)

        Can raise ALUDZeroDivisionError
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### xor
```
XOR dest, *ops

        Apply logical XOR to operands amd save into dest
            - XOR A, B
                A = A ^ B
            - XOR A, B, C, D
                A = ((B ^ C) ^ D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### and
```
AND dest, *ops

        Apply logical AND to operands amd save into dest
            - AND A, B
                A = A & B
            - AND A, B, C, D
                A = ((B & C) & D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### or
```
OR dest, *ops

        Apply logical OR to operands amd save into dest
            - OR A, B
                A = A | B
            - OR A, B, C, D
                A = ((B | C) | D)
```
- **dest**: `Address | IndirectAddress | Register`
- **ops**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### dec
```
DEC dest

        Decrement (-1) operand
```
- **dest**: `Address | IndirectAddress | Register`
- **return**: `typing.Iterator`
#### inc
```
INC dest

        Increment (+1) operand
```
- **dest**: `Address | IndirectAddress | Register`
- **return**: `typing.Iterator`
#### jmp
```
JMP label

        Jump to label without condition
```
- **label**: `Label`
- **return**: `None`
#### je
```
JE label

        Jump to label if Z Flag is set (operands are equal)
```
- **label**: `Label`
- **return**: `None`
#### jne
```
JE label

        Jump to label if Z Flag is not set (operands are not equal)
```
- **label**: `Label`
- **return**: `None`
#### jl
```
JL label

        Jump to label if N Flag is set (first < second)
```
- **label**: `Label`
- **return**: `None`
#### jg
```
JL label

        Jump to label if N Flag is not set (first > second)
```
- **label**: `Label`
- **return**: `None`
#### jle
```
JLE label

        Jump to label if Z or N flag is set (first <= second)
```
- **label**: `Label`
- **return**: `None`
#### jge
```
JGE label

        Jump to label if Z or not N flag is set (first >= second)
```
- **label**: `Label`
- **return**: `None`
#### mov
```
MOV dest, src

        Move value from src to dest
```
- **dest**: `Address | IndirectAddress | Register`
- **src**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### movn
```
MOVN dest, src

        Move number value from src to #STDOUT or #STDERR
```
- **dest**: `Address`
- **src**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### ldn
```
LDN dest, src

        Get number value from #STDIN and write into dest
```
- **dest**: `Address`
- **src**: `Address | IndirectAddress | Register | Constant`
- **return**: `typing.Iterator`
#### cmp
```
CMP op1, op2

        Compare two operands by subtracting and set flags
```
- **var**: `Address | IndirectAddress | Register | Constant`
- **src**: `Address | IndirectAddress | Register | Constant`
- **return**: `None`
#### hlt
```
HLT

        Stop execution
```
- **return**: `typing.Iterator`
