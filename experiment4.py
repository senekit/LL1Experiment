from prettytable import PrettyTable

def get_state(GS):
    result = []
    for i in GS:
        if i[0] not in result:
            result.append(i[0])
    return result


def get_FIRSTVT(GS):
    state = get_state(GS)
    firstvt_table = [[i] for i in state]
    for i in range(len(firstvt_table)):
        result = more_FIRSTVT(firstvt_table[i][0], GS)
        firstvt_table[i].extend(result)
    return firstvt_table

def more_FIRSTVT(target, GS):
    result = []
    for i in range(len(GS)):
        if GS[i][0] == target:
            if GS[i][1][0].islower() or GS[i][1][0].isalpha() == False:
                add_into_result(result, GS[i][1][0])
            else:
                if target != GS[i][1][0]:
                    temp = more_FIRSTVT(GS[i][1][0], GS)
                    add_into_result(result, temp)
                if len(GS[i][1]) >= 2:
                    if GS[i][1][1].islower() or GS[i][1][1].isalpha() == False:
                        add_into_result(result, GS[i][1][1])
    return result

def get_LASTVT(GS):
    state_all = get_state(GS)
    lastvt_table = [[i] for i in state_all]
    for i in range(len(lastvt_table)):
        result = more_LASTVT(lastvt_table[i][0], GS)
        lastvt_table[i].extend(result)
    return lastvt_table


def more_LASTVT(target, GS):
    result = []
    for i in range(len(GS)):
        if GS[i][0] == target:
            if GS[i][1][-1].islower() or GS[i][1][-1].isalpha() == False:
                add_into_result(result, GS[i][1][-1])
            else:
                if target != GS[i][1][-1]:
                    temp = more_LASTVT(GS[i][1][-1], GS)
                    add_into_result(result, temp)
                if len(GS[i][1]) >= 2:
                    if GS[i][1][-2].islower() or GS[i][1][-2].isalpha() == False:
                        add_into_result(result, GS[i][1][-2])
    return result


def add_into_result(old, add):
    for i in add:
        if i not in old:
            old.extend(i)


def get_table(firstvt, lastvt, GS):
    isflag = True
    state = get_priority_state(firstvt, lastvt)
    table = [["0" for col in range(len(state))] for row in range(len(state))]
    for i in range(len(GS)):
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            if x + 2 > length - 1:
                break
            if (GS[i][1][x] == GS[i][1][x + 2] and GS[i][1][x] == "#") or (
                    GS[i][1][x] == "(" and GS[i][1][x + 2] == ")"):
                y0, x0 = get_x_y(GS[i][1][x], GS[i][1][x + 2], state)
                if table[y0][x0] != "0":
                    isflag = False
                table[y0][x0] = "="
    for i in range(len(GS)):
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            if x + 1 > length - 1:
                break
            if GS[i][1][x] in state and GS[i][1][x + 1] not in state:
                temp = firstvt[GS[i][1][x + 1]]
                for q in temp:
                    y0, x0 = get_x_y(q, GS[i][1][x], state)
                    if table[x0][y0] != "0":
                        isflag = False
                    table[x0][y0] = "<"
    for i in range(len(GS)):
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            if x + 1 > length - 1:
                break
            if GS[i][1][x] not in state and GS[i][1][x + 1] in state:
                temp = lastvt[GS[i][1][x]]
                for q in temp:
                    y0, x0 = get_x_y(q, GS[i][1][x + 1], state)
                    if table[y0][x0] != "0":
                        isflag = False
                    table[y0][x0] = ">"

    return table, state, isflag


def get_x_y(para1, para2, state):
    y = -1
    x = -1
    for i in range(len(state)):
        if para1 == state[i]:
            y = i
    for i in range(len(state)):
        if para2 == state[i]:
            x = i
    return y, x

def get_priority_state(firstvt, lastvt):
    state = []
    for key, value in firstvt.items():
        for x in range(0, len(value)):
            if value[x] not in state:
                state.extend(value[x])
    for key, value in lastvt.items():
        for x in range(0, len(value)):
            if value[x] not in state:
                state.extend(value[x])
    return state


def analy_input_string(GS, table, state, input):
    ana_shed = []
    input_shed = []
    ana_shed.append("#")
    input_shed.extend(list(reversed(list(input))))
    show_count = 1
    print("%s %8s %8s %8s %8s" % ("步骤", "栈", "优先关系", "剩余输入串", "移进或规约"))
    while (True):
        print(show_count, end="")
        show_count += 1
        print("%12s" % ("".join(ana_shed)), end="")
        indicator = len(ana_shed) - 1
        if ana_shed[indicator].isupper():
            for i in reversed(range(len(ana_shed) - 1)):
                if ana_shed[i].isupper() == False:
                    indicator = i
                    break
        y, x = get_x_y(ana_shed[indicator], input_shed[-1], state)
        relationship = table[y][x]
        print("%8s" % (relationship), end="")

        print("%14s" % "".join(list((reversed("".join(input_shed))))), end="")
        if (relationship == "<" or relationship == "=") and len(input_shed) != 1:
            print("%8s" % ("移进"))
        elif relationship == ">":
            print("%8s" % ("归约"))
        else:
            print("%8s" % ("接受"))

        if len(ana_shed) == 2 and len(input_shed) == 1:
            break

        if relationship == "<" or relationship == "=":
            ana_shed.append(input_shed[-1])
            input_shed.pop()

        elif relationship == ">":
            if indicator == len(ana_shed) - 1:

                if Statute(GS, ana_shed[indicator], ana_shed[indicator]):
                    ana_shed.pop()
                    ana_shed.append("N")
            else:

                if Statute(GS, ana_shed[indicator - 1:indicator + 2], ana_shed[indicator]):
                    ana_shed.pop()
                    ana_shed.pop()
                    ana_shed.pop()
                    ana_shed.append("N")


def Statute(GS, input, symbol):
    for i in range(len(GS)):
        if len(GS[i][1]) == len(input) and symbol in GS[i][1]:

            count = 0
            for x in range(len(GS[i][1])):
                if GS[i][1][x] == symbol:
                    count += 1
                elif str(GS[i][1][x]).isupper() and str(input[x]).isupper():
                    count += 1

            if count == len(GS[i][1]):
                return True
    return False


if __name__ == '__main__':

    GS = [["A", "#E#"],
          ["E", "E+T"],
          ["E", "T"],
          ["T", "T*F"],
          ["T", "F"],
          ["F", "P|F"],
          ["F", "P"],
          ["P", "(E)"],
          ["P", "i"]]
    input_str = "i+i*i#"
    for i in GS:
        print("%s -> %s" % (i[0], i[1]))

    firstvt = {}
    result = get_FIRSTVT(GS)
    for i in range(len(result)):
        firstvt[str(result[i][0][0])] = result[i][1:]
    for key, value in firstvt.items():
        print("FIRSTVT(%s) = {%s}" % (key, str(value)[1:-1]))

    lastvt = {}
    result = get_LASTVT(GS)
    for i in range(len(result)):
        lastvt[str(result[i][0][0])] = result[i][1:]
    for i, j in lastvt.items():
        print("LASTVT(%s) = {%s}" % (i, str(j)[1:-1]))

    # 得到算符优先关系表
    table, state, isFlag = get_table(firstvt, lastvt, GS)
    print("%24s" % ("算符优先关系表"))
    print("---------------------------------------------------------")
    for i in state:
        print("%8s" % i, end="")
    print("")
    for i in range(len(table)):
        print("%s" % state[i], end="")
        print("%7s" % table[i][0], end="")
        for x in table[i][1:]:
            print("%8s" % x, end="")
        print("")
    print("是否是算符优先文法:%s" % (str(isFlag)))
    print("对输入串 %16s 进行规约" % (input_str))
    analy_input_string(GS, table, state, input_str)
