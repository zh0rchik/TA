from enum import Enum

LEN_OPERAND = 16
BINARY_BITS = {'0', '1'}

NO_ERRORS = '000'                 # Нет ошибок
DIVISION_BY_ZERO = '001'          # Деление на ноль
INCORRECT_OPCODE = '010'          # Неверный код операции
INCORRECT_INPUT = '011'           # Неверная форма ввода
INCORRECT_OPERAND_LENGTH = '100'  # Неверная длина ввода
GRID_OVERFLOW = '101'             # Переволнение разрядной сетки

MULTIPLICATION = '00'
DIVISION = '11'

if __name__ == "__main__":

    file = open("input.txt")

    kod, op1, op2 = file.readline().split(' ')
    res = 0
    err = '000'

    if set(op1) - BINARY_BITS or set(op2) - BINARY_BITS:
        err = INCORRECT_INPUT
    elif kod != MULTIPLICATION and kod != DIVISION:
        err = INCORRECT_OPCODE
    elif len(op1) > LEN_OPERAND or len(op2) > LEN_OPERAND:
        err = INCORRECT_OPERAND_LENGTH
    elif int(op2, 2) == 0:
        err = DIVISION_BY_ZERO
    else:
        if kod == MULTIPLICATION:
            res = bin(int(op1, 2) * int(op2, 2))[2:]
        elif kod == DIVISION:
            res = bin(int(op1, 2) // int(op2, 2))[2:]

        if len(res) > LEN_OPERAND:
            err = GRID_OVERFLOW
            res = res[-LEN_OPERAND:]

    print(f"kod = {kod}\nop1 = {str(op1).zfill(LEN_OPERAND)}\nop2 = {str(op2).zfill(LEN_OPERAND)}\n"
          f"res = {str(res).zfill(LEN_OPERAND)}\nerr = {err}")