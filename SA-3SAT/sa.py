from random import randint

def evaluate(solution):
    global data
    numberTrue = 0
    for i in range(clausesNumber):
        cont = 0
        c1 = data[i][0]
        c2 = data[i][1]
        c3 = data[i][2]
        if(c1 < 0):
            c1 = c1*-1
            if(solution[c1-1] == 0): cont+=1
        else:
            if(solution[c1-1] == 1): cont+=1

        if(c2 < 0):
            c2 = c2*-1
            if(solution[c2-1] == 0): cont+=1
        else:
            if(solution[c2-1] == 1): cont+=1

        if(c3 < 0):
            c3 = c3*-1
            if(solution[c3-1] == 0): cont+=1
        else:
            if(solution[c3-1] == 1): cont+=1

        if(cont>0): numberTrue+=1

    return numberTrue

def randomValues():
    solution = []
    for i in range(variablesNumber):
        solution.append(randint(0,1))
    return solution

def randomSearch():
    solution = []
    solution = randomValues()
    trueClauses = evaluate(solution)
    funcEvalLimit = input('iterations for random search: ')
    for i in range(int(funcEvalLimit)):
        s = randomValues()
        trueClausesS = evaluate(s)
        print(trueClausesS)
        if(trueClauses < trueClausesS):
            trueClauses = trueClausesS
            solution = s
    return (solution, trueClauses)


def readFile():
    global data, variablesNumber, clausesNumber
    data = []
    x = input('Variables number: ')
    file = open('uf' + x + '-01.cnf','r')
    variablesNumber = int(x)
    if(variablesNumber == 20): clausesNumber = 91
    elif(variablesNumber == 100): clausesNumber = 430
    else: clausesNumber = 1065
    lines = file.readlines()
    for i in lines:
        k = i.replace(' 0','').split(' ')
        if len(k) < 3: continue
        c1 = k[0]
        c2 = k[1]
        c3 = k[2]
        if(c1.startswith('-')):
            c1 = c1.split('-')[1]
            c1 = int(c1) * -1
        else: c1 = int(c1)
        if(c2.startswith('-')):
            c2 = c2.split('-')[1]
            c2 = int(c2) * -1
        else: c2 = int(c2)
        if(c3.startswith('-')):
            c3 = c3.split('-')[1]
            c3 = int(c3) * -1
        else: c3 = int(c3)
        data.append((c1,c2,c3))



readFile()

sol = []
sol,number = randomSearch()

print(str(number) + '/' + str(clausesNumber))
print(sol)
