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
    global initial_s
    s = initial_s[:]
    best = s[:]
    conv = [evaluate(best)]
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
                    if uniform(0,1) < exp(-delta/T):
                        s = n[:]
                except OverflowError:
                    s = n[:]
            print("{:.2f} %".format(100 * (IterT/SAmax * 1/N + i/N)), end='\r')
        conv += [evaluate(best)]
        i += 1
        T = A/(i+1) + B
        IterT = 0
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

make_formula("uf20-01.cnf", 20)
plt.plot(run_sa(30,.0001,30,10000))
plt.show()

make_formula("uf100-01.cnf", 100)
plt.plot(run_sa(30,.0001,30,10000))
plt.show()

make_formula("uf250-01.cnf", 250)
plt.plot(run_sa(30,.0001,30,10000))
plt.show()
