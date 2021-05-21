from prettytable import PrettyTable

Vn = set()
Vt = set()
First = {}
Follow = {}
Grams = []
production = {}
#Grams_no_left = []
AnalysisList = {}
start = ''
end = '#'
esp = 'ε'
isLL1 = True



def remove_left():
    for i in Grams:
        if i[0] == i[3]:
            temp = i.split('->')
            Grams.append(temp[0]+'->'+temp[0].lower())
            Grams.append(temp[0].lower()+'->'+temp[1][1:]+temp[0].lower())
            Grams.remove(i)


def get_First() -> None:
    return

def get_Follow() -> None:
    return

def LL1() -> None:
    global Vt, Vn, First, Follow, start, Grams, Grams_no_left, isLL1
    with open('./input.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            data = line.strip('\n')
            Grams.append(data)
    f.close()
    start = Grams[0][0]
    remove_left()
    for item in Grams:
        temp = item.split('->')
        Vn.add(temp[0])
        for i in temp[1]:
            Vt.add(i)
        if temp[0] not in production:
            production[temp[0]] = set()
        production[temp[0]].add(temp[1])
    Vt -= Vn
    print(Vt)
    print(Vn)
    print(production)


if __name__=='__main__':
    LL1()