import matplotlib.pyplot as plt
from random import randint, uniform
from math import exp
import re

def initial(s):
    global initial_s
    initial_s = s[:]
    for i in range(len(s)):
        initial_s[i] = randint(0,1)

def neighbor(s):
    new_sol = s[:]
    for i in range(len(new_sol)):
        aux = randint(1,20)
        if aux == 1:
            new_sol[i] = abs(s[i]-1)
    return new_sol

def run_sa(T0, TN, N, SAmax):
    global initial_s, formula
    s = initial_s[:]
    best = s[:]
    conv = []
    IterT = 0
    T = T0
    A = (T0-TN)*N/(N-1)
    B = T0 - A
    i = 0
    while T > TN:
        while IterT < SAmax:
            IterT += 1
            n = neighbor(s)
            delta = evaluate(n) - evaluate(s)
            if delta > 0:
                s = n[:]
                if evaluate(n) > evaluate(best):
                    best = n[:]
            else:
                try:
                    if uniform(0,1) < exp(delta/T):
                        s = n[:]
                except OverflowError:
                    s = n[:]
            print("{:.2f} %".format(100 * (IterT/SAmax * 1/N + i/N)), end='\r')
        conv += [(T, evaluate(s))]
        i += 1
        T = A/(i+1) + B
        IterT = 0
    print("100.00 %")
    return conv

def evaluate(s):
    res = 0
    for i in formula:
        _res = 0
        for j in i:
            if j < 0:
                _res += s[-j - 1]==0
            else:
                _res += s[j - 1]==1
            if _res > 0:
                res += 1
                break
    return res

def make_formula(filename, n_var):
    global formula
    initial([0 for _ in range(n_var)])
    f = open(filename, "r")
    contents = re.compile("[ ]*[0][ ]*\n").split(f.read())
    formula = []
    for i in contents:
        cl = list(map(int, i.split()))
        if len(cl) > 0:
            formula += [cl]

def plot(conv, decimal_places):
    global formula
    plt.axhline(y=len(formula), color='red', linestyle='dashed', linewidth=0.8)
    plt.plot([i[1] for i in conv], color='blue', linewidth=0.8)
    plt.xlabel("temperatura")
    #plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    x_values = []
    x_ticks = []
    for i in range(0, len(conv), len(conv)//10):
        x_values += [i]
        x_ticks += [round(conv[i][0], decimal_places)]
    plt.xticks(x_values, x_ticks)
    plt.ylabel("no. de cláusulas satisfeitas")
    plt.show()

make_formula("uf20-01.cnf", 20)
plot(run_sa(40,.0001,40,10000), 4)

make_formula("uf100-01.cnf", 100)
plot(run_sa(1000,.0001,100,10000), 4)

make_formula("uf250-01.cnf", 250)
plot(run_sa(1000,.0001,100,10000), 4)
