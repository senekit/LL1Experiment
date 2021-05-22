from prettytable import PrettyTable

Vn = set()
Vt = set()
First = {}
Follow = {}
Grams = []
production = {}
Grams_no_left = []
AnalysisList = {}
start = ''
end = '#'
esp = 'ε'
isLL1 = True


# 消除左递归
def remove_left():
    for i in Grams:
        temp = i.split('->')
        r = temp[1].split('|')
        if i[0] == i[3]:
            if r[-1][0] != i[0]:
                Grams_no_left.append(i[0].lower() + '->' + esp)
            for right in r:
                if right[0] == i[0]:
                    Grams_no_left.append(i[0].lower() + '->' + right[1:] + i[0].lower())
                else:
                    Grams_no_left.append(i[0] + '->' + right + i[0].lower())
        else:
            for right in r:
                Grams_no_left.append(i[0] + '->' + right)


def get_First() -> None:
    global Vt, Vn, First
    for item in Vt:
        First[item] = set(item)
    for item in Vn:
        First[item] = set()
    tag = True
    while (tag):
        tag = False
        for x in Vn:
            for y in production[x]:
                begin = len(First[x])
                temp = 0
                has_esp = True
                while has_esp and temp < len(y):
                    if esp in First[y[temp]]:
                        if y[temp] in Vn:
                            First[x] |= First[y[temp]] - set(esp)
                        else:
                            First[x] |= First[y[temp]]
                        temp += 1
                    else:
                        First[x] |= First[y[temp]] - set(esp)
                        has_esp = False
                if len(First[x]) != begin:
                    tag = True
    return


def get_Follow() -> None:
    for item in Vn:
        Follow[item] = set()
    Follow[start].add(end)
    tag = True
    while tag:
        tag = False
        for x in Vn:
            for y in production[x]:
                #  print(y)
                for i in range(len(y)):
                    if y[i] in Vt:
                        continue
                    begin = len(Follow[y[i]])
                    for j in range(i+1, len(y)):
                        if y[j] in Vt:
                            Follow[y[i]].add(y[j])
                            if begin != len(Follow[y[i]]):
                                tag = True
                            break
                        else:
                            Follow[y[i]] |= First[y[j]] - set(esp)
                            if esp in First[y[j]]:
                                Follow[y[i]] |= Follow[y[j]]
                            if begin != len(Follow[y[i]]):
                                tag = True
                            if esp not in First[y[j]]:
                                break
        for item in Grams_no_left:
            if item[-1] in Vn:
                begin = len(Follow[item[-1]])
                Follow[item[-1]] |= Follow[item[0]]
                if begin != len(Follow[item[-1]]):
                    tag =True

    return

def get_AnalysisList():
    global AnalysisList
    for i in Vn:
        AnalysisList[i] = dict()
        for j in Vt:
            AnalysisList[i][j] = None
        AnalysisList[i][end] = None
    for item in Grams_no_left:
        temp = item.split('->')
        if esp in First[temp[1][0]]:
            for b in Follow[temp[0]]:
                AnalysisList[temp[0]][b] = temp[0] + '->' + esp
        else:
            for a in First[temp[1][0]]:
                AnalysisList[temp[0]][a] = temp[0] + '->' +temp[1]



def printf() -> None:

    print("输入文法如下")
    for item in Grams:
        print('  ' + item)
    print("消除左递归后文法如下")
    for item in Grams_no_left:
        print("  " + item)
    print("非终结符")
    print(Vn)
    print("终结符")
    print(Vt)
    first_follw_table = PrettyTable()
    first_follw_table.field_names = ['非终结符', 'FIRST', 'FOLLOW']
    for item in Vn:
        row = []
        row.append(item)
        row.append(First[item])
        row.append(Follow[item])
        first_follw_table.add_row(row)
    print(first_follw_table)
    col = ['']
    for i in Vt:
        if i == esp:
            continue
        col.append(i)
    col.append(end)
    predit_table = PrettyTable(col)
    for i in AnalysisList:
        row = []
        row.append(i)
        for j in AnalysisList[i]:
            if j == esp:
                continue
            if AnalysisList[i][j] is None:
                row.append('')
            else:
                row .append(AnalysisList[i][j])
        predit_table.add_row(row)
    print(predit_table)
    return None


def LL1() -> None:
    global Vt, Vn, First, Follow, start, Grams, Grams_no_left, isLL1, AnalysisList
    with open('./input.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            data = line.strip('\n')
            Grams.append(data)
    f.close()
    start = Grams[0][0]
    remove_left()
    for item in Grams_no_left:
        temp = item.split('->')
        Vn.add(temp[0])
        i = 0
        while i < len(temp[1]):
            Vt.add(temp[1][i])
            i += 1
        Vt -= Vn
    for item in Vn:
        production[item] = set()
    for item in Grams_no_left:
        temp = item.split('->')
        production[temp[0]].add(temp[1])
    '''  
    print(production)
    print(Grams_no_left)
    print(Vt)
    print(Vn)   '''
    #print(production)

    get_First()
    get_Follow()
    get_AnalysisList()
    printf()



def analysis(s) -> PrettyTable():

    ans = PrettyTable()
    ans.field_names=['步骤', '分析栈', '剩余输入串', '匹配']
    stk = '#'+start
    time = 0
    while len(stk) and len(s):
        row = []
        time += 1
        row.append(time)
        row.append(stk)
        row.append(s)
        top = stk[-1]
        if top in Vt:
            if top == s[0]:
                row.append(s[0]+'匹配')
                ans.add_row(row)
                stk = stk[:-1]
                s = s[1:]
                continue
            else:
                row.append('匹配失败')
                ans.add_row(row)
                return ans
        else:
            if top == end:
                row.append('accept')
                ans.add_row(row)
                return ans
            if top in Vn:
                if AnalysisList[top][s[0]] is None:
                    row.append('匹配失败')
                    ans.add_row(row)
                    return ans
                else:
                    row.append(str(AnalysisList[top][s[0]]))
                    ans.add_row(row)
                    stk = stk[:-1]
                    temp = AnalysisList[top][s[0]].split('->')
                    if temp[1] == esp:

                        continue
                    stk = stk + temp[1][::-1]
                    continue
    while len(stk):
        time += 1
        top = stk[-1]
        if top == end:
            row = []
            row.append(time)
            row.append(stk)
            row.append(s)
            row.append('accept')
            ans.add_row(row)
            return ans
        if esp not in production[top]:
            row = []
            row.append(time)
            row.append(stk)
            row.append(s)
            row.append('failure')
            ans.add_row(row)
            return ans
        else:
            row = []
            row.append(time)
            row.append(stk)
            row.append(s)
            row.append(top+'->'+esp)
            stk = stk[:-1]
            ans.add_row(row)

    time += 1
    row = []
    row.append(time)
    row.append(stk)
    row.append(s)
    row.append('failure')
    ans.add_row(row)
    return ans





if __name__ == '__main__':
    LL1()
    test = []
    with open('./data.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            data = line.strip('\n')
            test.append(data)
    f.close()
    for item in test:
        print(item)
        print(analysis(item))

