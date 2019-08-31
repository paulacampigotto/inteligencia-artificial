#from Tkinter import *
from pprint import pprint
from random import choices
from random import randint
from math import ceil


size = 20
radius = 1
deadAnts = ceil(size*size * .4)
aliveAnts = ceil(size*size * .05)
aliveAntsList = []
cells1 = [[0 for i in range(size)] for i in range(size)]
cells2 = [[0 for i in range(size)] for i in range(size)]

def display():
    global cells1, cells2
    dispose(cells1,deadAnts)
    dispose(cells2,aliveAnts)
    pprint(cells1)
    for i in range(100):
        for j in aliveAntsList:
            j.live()
            if(aliveAntsList.index(j)==0): print(j.position)


def prob(x,y):
    global size, radius, cells1
    itemsAround = 0
    for i in range(-1*radius,2*radius):
        for j in range(-1*radius,2*radius):
            if (i==0 and j==0) or x+i<0 or y+j<0 or x+i>=size or y+j>=size:
                continue
            if cells1[x+i][y+j] == 1: itemsAround+=1
    return (itemsAround+1)/10 # cuidado

def emptyCell(position):
    global cells1
    return cells1[position[0]][position[1]] == 0

class AliveAnt:
    def __init__(self, position):
        self.hasItem = False
        self.position = position
        self.memory = ()

    def live(self):
        global cells1
        self.move()
        probability = prob(self.position[0], self.position[1])
        if emptyCell(self.position) and self.hasItem:
            choice = choices([1,0], [probability, 1-probability])
            if choice==1: #drop
                cells1[self.position[0]][self.position[1]] = 1
                self.hasItem = False
                self.memory = self.position
        elif not emptyCell(self.position) and not self.hasItem:
            choice = choices([1,0], [1-probability, probability])
            if choice==1: #pick                                   ****
                cells1[self.position[0]][self.position[1]] = 0
                self.hasItem = True

    def move1(self, direction):
        if direction == 1:
            self.move2(self.position[0]+1, self.position[1])
        elif direction == 2:
            self.move2(self.position[0], self.position[1]+1)
        elif direction == 3:
            self.move2(self.position[0]+1, self.position[1]+1)
        elif direction == 4:
            self.move2(self.position[0]-1, self.position[1])
        elif direction == 5:
            self.move2(self.position[0], self.position[1]-1)
        elif direction == 6:
            self.move2(self.position[0]-1, self.position[1]-1)
        elif direction == 7:
            self.move2(self.position[0]-1, self.position[1]+1)
        elif direction == 8:
            self.move2(self.position[0]+1, self.position[1]-1)

    def move2(self,x,y):
        global size, cells2
        if x>=0 and x<size and y>=0 and y<size:
            self.position = (x,y)
            cells2[x][y] = 1
        else:
            self.move1(randint(1,8))

    def move(self):
        global cells2
        cells2[self.position[0]][self.position[1]]=0
        if self.memory == () or not self.hasItem:
            self.move1(randint(1,8))
        else:
            x=0
            y=0
            if self.memory[0] > self.position[0]:
                x+=1
            elif self.memory[0] < self.position[0]:
                x-=1
            if self.memory[1] > self.position[1]:
                y+=1
            elif self.memory[1] < self.position[1]:
                y-=1
            self.move2(x,y)
        cells2[self.position[0]][self.position[1]]=1

def dispose(cells, n):
    global cells2, aliveAntsList
    cont = 0
    while cont < n:
        x = randint(0,size-1)
        y = randint(0,size-1)
        if cells[x][y] == 0:
            cont+=1
            cells[x][y] = 1
            if cells == cells2: aliveAntsList += [AliveAnt((x,y))]


display()
pprint(cells1)
