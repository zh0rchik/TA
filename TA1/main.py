states = "S0"
if __name__ == "__main__":
    text = []
    index_repeat = []
    index_until = []
    with open("source.txt", "r") as fr:
        states += " S1"
        for line in fr:
            text.append(line)
            states += " S2"
            if 'repeat' in line:
                index_repeat.append(text.index(line))
                states += " S3"
            if 'until' in line:
                index_until.append(text.index(line))
                states += " S4"
    fr.close()
    states += " S5"

    if len(index_repeat) == 0:
        with open("out.txt", "w") as fw:
            states += " S6"
            for i in range(len(text)):
                fw.write(text[i])
                states += " S7"

        states += " S0"
    else:
        body_of_cycle = []
        states += " S8"
        for i in range(index_repeat[0] + 1, index_until[len(index_until) - 1]):
            s = text[i][1:]
            body_of_cycle.append(s)
            states += " S9"

        text[index_repeat[0]], text[index_until[len(index_until) - 1]] = \
            text[index_until[len(index_until) - 1]], text[index_repeat[0]]
        states += " S10"
        new_code = []
        states += " S11"

        for i in range(index_repeat[0]):
            new_code.append(text[i])
            states += " S12"

        for i in range(len(body_of_cycle)):
            new_code.append(body_of_cycle[i])
            states += " S13"

        for i in range(index_repeat[0], len(text)):
            new_code.append(text[i])
            states += " S14"

        for i in range(len(new_code)):
            if 'until' in new_code[i] and i == index_repeat[0] + len(new_code) - len(text):
                new_code[i] = new_code[i].replace('until ', 'while not(')
                new_code[i] = new_code[i].replace(';', ') do begin')
                states += " S15"
            if 'repeat' in new_code[i] and i == index_until[len(index_until) - 1] + len(new_code) - len(text):
                new_code[i] = new_code[i].replace('repeat', 'end;')
                states += " S16"

        with open("out.txt", "w") as fw:
            states += " S17"
            for i in new_code:
                fw.write(i)
                states += " S18"
        fw.close()
        states += " S0"

    print(states)