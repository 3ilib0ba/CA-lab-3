# Лабораторная работа №3. На кончиках пальцев

## Цель

- экспериментальное знакомство с устройством процессоров через моделирование; 
- получение опыта работы с компьютерной системой на нескольких уровнях организации.

### Выполнил
ФИО: Иванов Евгений Дмитриевич<br>
Группа: P33111

### Вариант

`asm | cisc | harv | hw | tick | struct | stream | mem | prob5`

## Язык программирования

### BNF

``` ebnf
<program>       ::= <section_text> | <section_data> <section_text>

<section_data>  ::= "section .data" <line> <data>
<data>          ::= <data_line> 
                  | <data_line> <data>
<data_line>     ::= <var_name> <var_value> <line> <extra_s> 
                  | <extra_s>
<var_name>      ::= <word> ":"
<var_value>     ::= <string> | <number> | <buffer>
<string>        ::= "\'" <word> "\'" 
                  | "\"" <word> "\""
<buffer>        ::= "buf " <number>

<section_text>  ::= "section .text" <line> <instructions>
<instructions>  ::= <instruction> 
                  | <instruction> <instructions>
<instruction>   ::= <label_and_maybe_step> <line> <extra_s>
                  | <step> <line> <extra_s>
<label_and_maybe_step>  ::= <label> | <label> <step>
<label>         ::= "." <word_without_space> ":"
<step>          ::= <command> <operand(-s)>

<word>          ::= <letter_or_digit_or_space> 
                  | <letter_or_digit_or_space> <word>
<word_without_space>        ::= <letter_or_digit> 
                              | <letter_or_digit> <word_without_space>
<letter_or_digit>           ::= <letter> | <digit>
<letter_or_digit_or_space>  ::= <letter> | <digit> | <space>
<extra_s>       ::= <line_or_space> | <line_or_space> <extra_s>
<line_or_space> ::= <line> | <space>
<line>          ::= "\n" 
<spaces>        ::= <space> | <space> <spaces>
<space>         ::= " " | "\t"
<letter>        ::= [a-z] | [A-Z] | [!@#$%^&*()_+-=]
<number>        ::= <digit> | <digit> <number>
<digit>         ::= [0-9]
<comment>       ::= ";" <text>
```

### Секция данных

``` asm
section .data
    HELLO:      "Hello"         ; строка
    NUMBER_HEX: 0xDEAD          ; число в 16 СС
    NUMBER_DEC: -15             ; число в 10 СС
    ARRAY:      buf 5           ; массив из 5 элементов
    NULL_TERM:  0x00
```

### Секция кода

```
section .text
    .print_char:                ; метка
        MOV %rdx, #HELLO[%rdi]  ; загрузка в rdx HELLO[rdi]
        CMP %rdx, #NULL_TERM    ; выставить флаги по операции вычитания rdx и константы
                                ; (прямая адресация)
        JE .exit                ; переход в случае равенства(флаг Z выставлен)
        MOV #STDOUT, %rdx       ; вывод символа из $rdx
        INC %rdi                ; rdi++
        JMP .print_char         ; безусловный переход к метке .print_char
    .exit:
        HLT                     ; завершение работы
```

### Инструкции

Инструкции могут принимать неограниченное количество операндов.

```
ADD %RAX, #VAR              ; %RAX + #VAR        -> %RAX
ADD %RAX, #VAR, 0xf1        ; #VAR + 0xf1        -> %RAX
ADD %RAX, #VAR, 0xf1, %RDX  ; #VAR + 0xf1 + %RDX -> %RAX
```

При трансляции сложная инструкция преобразуется в несколько простых.

[Документация по инструкциям](resources/instructions.md)





## Апробация

1. [cat](test/examples/cat.pyasm)
2. [hello](test/examples/hello.pyasm)
3. [prob5](test/examples/prob5.pyasm)

Журналы и коды алгоритмов можно посмотреть в каталоге [test/examples](test/examples).

| ФИО         | алг.  | LoC | code байт | code инстр. | инстр. | такт. | 
|-------------|-------|-----|-----------|-------------|--------|-------|
| Иванов Е.Д. | cat   | 12  | 643       | 6           | 28     | 46    |
| Иванов Е.Д. | hello | 14  | 765       | 7           | 69     | 116   |
| Иванов Е.Д. | prob5 | 43  | 1965      | 27          | 1468   | 3143  |















