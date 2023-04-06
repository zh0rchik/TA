def print_state(state, kod, op1, op2, res, err):
    print(f"\n{state}:\nkod = {str(kod).zfill(2)}\nop1 = {str(op1).zfill(LEN_OPERAND)}\nop2 = {str(op2).zfill(LEN_OPERAND)}\n"
          f"res = {str(res).zfill(LEN_OPERAND)}\nerr = {str(err).zfill(3)}")

LEN_OPERAND = 16
BINARY_BITS = {'0', '1'}

NO_ERRORS = '000'                 # Нет ошибок
DIVISION_BY_ZERO = '001'          # Деление на ноль
INCORRECT_OPCODE = '010'          # Неверный код операции
INCORRECT_INPUT = '011'           # Неверная форма ввода
INCORRECT_LEN = '100'             # Неверная длина ввода
OVERFLOW = '101'                  # Переволнение разрядной сетки

MULTIPLICATION = '00'
DIVISION = '11'

if __name__ == "__main__":
    kod, op1, op2, res, err = (0, 0, 0, 0, 0)
    print_state("S0", kod, op1, op2, res, err)

    file = open("input.txt")

    kod, op1, op2 = file.readline().split(' ')

    print_state("S1", kod, op1, op2, res, err)

    if set(op1) - BINARY_BITS or set(op2) - BINARY_BITS:
        err = INCORRECT_INPUT
        print_state("S2", kod, op1, op2, res, err)
    elif kod != MULTIPLICATION and kod != DIVISION:
        err = INCORRECT_OPCODE
        print_state("S3", kod, op1, op2, res, err)
    elif len(op1) != LEN_OPERAND or len(op2) != LEN_OPERAND:
        err = INCORRECT_LEN
        op1 = 0
        op2 = 0
        print_state("S4", kod, op1, op2, res, err)
    elif int(op2, 2) == 0:
        err = DIVISION_BY_ZERO
        print_state("S5", kod, op1, op2, res, err)
    else:
        if kod == MULTIPLICATION:
            res = bin(int(op1, 2) * int(op2, 2))[2:]

            if len(res) > LEN_OPERAND:
                err = OVERFLOW
                res = res[-LEN_OPERAND:]
                print_state("S8", kod, op1, op2, res, err)
            else:
                print_state("S6", kod, op1, op2, res, err)

        else:
            res = bin(int(op1, 2) // int(op2, 2))[2:]
            print_state("S7", kod, op1, op2, res, err)
    print_state("S0", kod, op1, op2, res, err)