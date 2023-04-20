class Expression:
    str_state_cc = ""
    str_state_gt = ""
    expression = ""
    CORRECT_SYNTAX = True
    CORRECT_OPERANDS = True

    def __init__(self, expression):
        self.expression = expression
    def check_correct(self):
        self.str_state_cc += "check_out: S0 "
        self.str_state_cc += "check_out: S1 "
        try:
            for number in self.expression.split():
                if number not in ["+", "-", "*", "/", "(", ")"] \
                        and not (-32768 <= float(number) <= 32767):
                        self.CORRECT_OPERANDS = False
                        self.str_state_cc += "check_out: S2 "
        except ValueError:
            self.CORRECT_SYNTAX = False
            self.str_state_cc += "check_out: S3 "

        self.str_state_cc += "check_out: S4 "
        self.str_state_cc += "check_out: S0"
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
        self.str_state_gt += "get_result: S0 "
        st = []
        units = self.get_transform().split()
        self.str_state_gt += "get_result: S1 "

        for unit in units:
            if unit not in ["+", "-", "*", "/", "(", ")"]:
                st.append(float(unit))
                self.str_state_gt += "get_result: S2 "
            else:
                op2 = st.pop()
                op1 = st.pop()
                self.str_state_gt += "get_result: S3 "

                if unit == "+":
                    st.append(op1 + op2)
                    self.str_state_gt += "get_result: S4 "
                elif unit == "-":
                    st.append(op1 - op2)
                    self.str_state_gt += "get_result: S5 "
                elif unit == "*":
                    st.append(op1 * op2)
                    self.str_state_gt += "get_result: S6 "
                elif unit == "/":
                    try:
                        st.append(op1 / op2)
                        self.str_state_gt += "get_result: S7 "
                    except ZeroDivisionError:
                        self.str_state_gt += "get_result: S10 "
                        self.str_state_gt += "get_result: S0"
                        print(self.str_state_gt)
                        quit("Ошибка: попытка деления на 0.")

        result = st.pop()
        self.str_state_gt += "get_result: S8 "

        if not(-32768 <= result <= 32767):
            self.str_state_gt += "get_result: S9 "
            self.str_state_gt += "get_result: S0"
            print(self.str_state_gt)
            quit("Ошибка: переполнение.")

        self.str_state_gt += "get_result: S11 "
        self.str_state_gt += "get_result: S0"
        return result

if __name__ == "__main__":
    e = Expression(input("Введите выражение, где элементы отделены пробелом: "))

    if e.check_correct():
        print(e.get_result())
        print(e.get_transform())
    elif not(e.CORRECT_SYNTAX):
        print("Ошибка: выражение введено некорректно.")
    elif not(e.CORRECT_OPERANDS):
        print("Ошибка: в выражение могут быть числа с плавающей точкой, которые не меньше -32768 и не больше 32767.")

    print(e.str_state_cc)
    print(e.str_state_gt)