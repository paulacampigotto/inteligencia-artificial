from random import randint
import random
from math import exp

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
    for i in range(int(funcEvalLimit)):
        s = randomValues()
        trueClausesS = evaluate(s)
        if(trueClauses < trueClausesS):
            trueClauses = trueClausesS
            solution = s
    return (solution, trueClauses)

def initSolution():
    s = []
    if(variablesNumber == 20):
        for i in range(20):
            if(i%2 == 0): s.append(0)
            else:
                s.append(1)
    elif(variablesNumber == 100):
        for i in range(100):
            if(i%2 == 0): s.append(0)
            else:
                s.append(1)

    else:
        for i in range(250):
            if(i%2 == 0): s.append(250)
            else:
                s.append(1)
    return s

def generateNeighborhood(solution):
    for i in range(variablesNumber):
        x = randint(0,100)
        if(x <= 5): # probability of changing the variable value = 5%
            if(solution[i] == 0): solution[i] = 1
            else: solution[i] = 0
    return solution

def saSearch(initialSolution):
    bestSolution = initialSolution
    iterT = 0
    currentT = t0
    while(currentT > 0.0001):
        while(iterT < saMax):  # iterT = number of iterations in currentT
            iterT+=1
            s = generateNeighborhood(initialSolution)
            delta = evaluate(s) - evaluate(initialSolution)
            if(delta > 0):
                initialSolution = s
                if(evaluate(s) > evaluate(bestSolution)): bestSolution = s
            else:
                x = round(random.uniform(0,1),4)
                if(x < exp((delta*-1)/currentT)):
                    initialSolution = s
        currentT = currentT * alpha
        iterT = 0
    return bestSolution, evaluate(bestSolution)



def readFile():
    global data, clausesNumber
    data = []
    file = open('uf' + str(variablesNumber) + '-01.cnf','r')
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


global variablesNumber, funcEvalLimit, alpha, initialSolution

#global parameter
variablesNumber = 20

#parameters random search
funcEvalLimit = 1000

#parameters sa search
alpha = 0.8
saMax =  10000 #iterations for thermal balance
t0 = 30 # initial temperature
initialSolution = initSolution()


readFile()

sol = []
sol,number = randomSearch()
print('Random: ')
print(str(number) + '/' + str(clausesNumber))
print(sol)

sol2, number2 = saSearch(initialSolution)
print('SA: ')
print(str(number2) + '/' + str(clausesNumber))
print(sol2)
