class Expression:
    expression = ""
    CORRECT_SYNTAX = True
    CORRECT_OPERANDS = True

    def __init__(self, expression):
        self.expression = expression
    def check_correct(self):
        try:
            for number in self.expression.split():
                if number not in ["+", "-", "*", "/", "(", ")"] \
                        and not (-32768 <= float(number) <= 32767):
                        self.CORRECT_OPERANDS = False
        except ValueError:
            self.CORRECT_SYNTAX = False

        return self.CORRECT_OPERANDS and self.CORRECT_SYNTAX

    def get_transform(self):
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

        transform_record = " ".join(units)

        return transform_record

    def get_result(self):
        st = []
        units = self.get_transform().split()

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
                        quit("Ошибка: попытка деления на 0.")

        result = st.pop()

        if not(-32768 <= result <= 32767):
            quit("Ошибка: переполнение.")

        return result

if __name__ == "__main__":
    e = Expression(input("Введите выражение, где элементы отделены пробелом: "))

    if e.check_correct():
        print(e.get_result())
        print(e.get_transform())
    elif not(e.CORRECT_SYNTAX):
        quit("Ошибка: выражение введено некорректно.")
    elif not(e.CORRECT_OPERANDS):
        quit("Ошибка: в выражение могут быть числа с плавающей точкой, которые не меньше -32768 и не больше 32767.")