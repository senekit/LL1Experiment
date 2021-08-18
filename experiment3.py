from prettytable import PrettyTable

table = PrettyTable()
step = 0
table.field_names = ['step', '已匹配', '未匹配', '使用函数']
s = ''
t = '(i+i)*#'
tag = True


def error():
    global tag
    tag = False

def advance():
    global table, step, s, t, tag
    s += t[0]
    t = t[1:]

def E() -> None:
    global table, step, s, t, tag
    step += 1
    row = [step, s, t, 'E']
    table.add_row(row)
    T()
    G()

    if (len(t) == 1 and t[0] != '#') or not tag:
        print(table)
        print('failed')
    elif t[0] == '#' and tag:
        print(table)
        print('success')


def G() -> None:
    global table, step, s, t, tag
    if not tag:
        return

        # print('G')
    step += 1

    if t[0] == '+':
        advance()
        row = [step, s, t, 'G->+TG']
        table.add_row(row)
        T()
        G()
    elif t[0] == '-':
        advance()
        row = [step, s, t, 'G->-TG']
        table.add_row(row)
        T()
        G()
    else:
        row = [step, s, t, 'G->ε']
        table.add_row(row)
        pass
    return


def T() -> None:
    global table, step, s, t, tag
    if not tag:
        return
    # print('T')
    step += 1
    row = [step, s, t, 'T']
    table.add_row(row)
    F()
    S()
    return


def S() -> None:
    global table, step, s, t, tag
    if not tag:
        return
    # print('S')
    step += 1
    if t[0] == '*':
        advance()
        row = [step, s, t, 'S->*FS']
        table.add_row(row)
        F()
        S()
    elif t[0] == '/':
        advance()
        row = [step, s, t, 'S->/FS']
        table.add_row(row)
        F()
        S()
    else:
        row = [step, s, t, 'S->ε']
        table.add_row(row)
        pass
    return


def F() -> None:
    global table, step, s, t, tag
    if not tag :
        return
    # print('F')
    step += 1
    if t[0] == 'i':
        advance()
        row = [step, s, t, 'F->i']
        table.add_row(row)
    elif t[0] == '(':
        advance()
        row = [step, s, t, 'F->(E)']
        table.add_row(row)
        E()
        if t[0] == ')':
            advance()
            step += 1
            row = [step, s, t, 'F->(E)']
            table.add_row(row)
        else:
            error()
    else:
        error()

    return


def print_info():
    global t
    print('递归下降分析程序')
    print('姓名： 王濡瑶')
    print('班级： 软件工程1906')
    print('学号： 8209190629')
    print('输入字符串： '+ t)
    pass


def control():
    print_info()
    global table, step, s, t, tag
    E()


if __name__ == '__main__':
    control()
