class Expression:
    expression = ""
    flag = True
    CORRECT_SYNTAX = True
    CORRECT_OPERANDS = True
    CHECK_DIVISION_BY_ZERO = False
    OVERFLOW = False

    def __init__(self, expression):
        self.expression = expression
        self.result = self.get_result()
        self.flag = self.check_correct()

    def check_correct(self):
        try:
            for number in self.expression.split():
                if number not in ["+", "-", "*", "/", "(", ")"]:
                    if not (-32768 <= float(number) <= 32767):
                        self.CORRECT_OPERANDS = False
        except ValueError:
            self.CORRECT_SYNTAX = False

        return self.CORRECT_OPERANDS and self.CORRECT_SYNTAX \
            and not(self.CHECK_DIVISION_BY_ZERO) and not(self.OVERFLOW)

    def get_result(self):
        st = []
        units = []

        for unit in self.expression.split():
            if unit in ["+", "-"]:
                if len(st) == 0 or st[len(st) - 1] == "(":
                    st.append(unit)
                else:
                    while len(st) != 0 and st[len(st) - 1] in ["*", "/", "+", "-"]:
                        units.append(st.pop())
                    st.append(unit)
            elif unit in ["*", "/"]:
                if len(st) == 0 or st[len(st) - 1] in ["+", "-", "("]:
                    st.append(unit)
                else:
                    while len(st) != 0 and st[len(st) - 1] in ["*", "/"]:
                        units.append(st.pop())
                    st.append(unit)
            elif unit == "(":
                st.append(unit)
            elif unit == ")":
                while len(st) != 0 and st[len(st) - 1] != "(":
                    units.append(st.pop())
                if len(st) != 0:
                    st.pop()
            else:
                units.append(unit)

        while len(st) > 0:
            units.append(st.pop())

        self.transform_record = " ".join(units)

        units = self.transform_record.split()
        st = []

        for unit in units:
            if unit not in ["+", "-", "*", "/", "(", ")"]:
                st.append(float(unit))
            else:
                op2 = st.pop()
                op1 = st.pop()

                if unit == "+":
                    st.append(op1 + op2)
                elif unit == "-":
                    st.append(op1 - op2)
                elif unit == "*":
                    st.append(op1 * op2)
                elif unit == "/":
                    try:
                        st.append(op1 / op2)
                    except ZeroDivisionError:
                        self.CHECK_DIVISION_BY_ZERO = True

        try:
            result = st.pop()
        except IndexError:
            result = "Undefined"

        if not (self.CHECK_DIVISION_BY_ZERO) and not (-32768 <= result <= 32767):
            self.OVERFLOW = True

        return result

if __name__ == "__main__":
    print("Введите выражение, где элементы отделены пробелом: ")
    e = Expression(input())

    if e.flag:
        print(e.result)
        print(e.transform_record)
    elif not(e.CORRECT_SYNTAX):
        print("Ошибка: выражение введено некорректно.")
    elif not(e.CORRECT_OPERANDS):
        print("Ошибка: в выражение могут быть числа с плавающей точкой, которые не меньше -32768 и не больше 32767")
    elif e.OVERFLOW:
        print("Ошибка: переполнение.")
    elif e.CHECK_DIVISION_BY_ZERO:
        print("Ошибка: попытка деления на 0.")
