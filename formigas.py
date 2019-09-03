import pygame
from pygame.locals import *
from pprint import pprint
from random import choices
from random import randint
from math import ceil
import threading




size = 50
radius = 1
kPick = 0.01
kDrop = 0.2

deadAnts = ceil(size*size * .1)
aliveAnts = ceil(size*size * .05)
aliveAntsList = []
cells1 = [[0 for i in range(size)] for i in range(size)]

pygame.init()
win = pygame.display.set_mode((size*10,size*10))
pygame.display.set_caption("Ant Clustering")

def screen():
    while True:
        pygame.time.delay(100)

def display():
    global cells1
    dispose(deadAnts,False)
    dispose(aliveAnts,True)
    for i in range(size):
        for j in range(size):
            if(cells1[i][j] == 0):
                print(" ", end="")
            else: print("X", end="")
        print()
    print("-"*size)
    #pprint(cells1)
    for i in range(100000):
        for j in aliveAntsList:
            j.live()
            pygame.draw.circle(win, (0 ,0,255), (j.position[0]*10, j.position[1]*10), 3)
            pygame.display.update()
            if(cells1[j.position[0]][j.position[1]] == 1):
                pygame.draw.circle(win, (255,0,0), (j.position[0]*10, j.position[1]*10), 3)
                pygame.display.update()
            else:
                pygame.draw.circle(win, (0,0,0), (j.position[0]*10, j.position[1]*10), 3)
                pygame.display.update()

            #print(str(aliveAntsList.index(j)) + ':'+ str(j.position), end=" "
        #print("\n")
    
    for i in range(size):
        for j in range(size):
            if(cells1[i][j] == 0):
                print(" ", end="")
            else: print("X", end="")
        print()

def probPick(x,y):
    global size, radius, kPick
    itemsAround = 0
    for i in range(-1*radius,2*radius):
        for j in range(-1*radius,1*radius):
            if (i==0 and j==0) or x+i<0 or y+j<0 or x+i>=size or y+j>=size:
                continue
            if cells1[x+i][y+j] == 1: itemsAround+=1
    return (kPick/(kPick + itemsAround)) ** 2 # Função P do artigo

def probDrop(x,y):
    global size, radius, kDrop
    itemsAround = 0
    for i in range(-1*radius,2*radius):
        for j in range(-1*radius,1*radius):
            if (i==0 and j==0) or x+i<0 or y+j<0 or x+i>=size or y+j>=size:
                continue
            if cells1[x+i][y+j] == 1: itemsAround+=1
    return (itemsAround/(kDrop+itemsAround)) ** 2 # Função P do artigo

def emptyCell(position):
    return cells1[position[0]][position[1]] == 0

class AliveAnt:
    def __init__(self, position):
        self.hasItem = False
        self.position = position

    def live(self):
        global cells1
        self.move()
        if emptyCell(self.position) and self.hasItem:
            probability = probDrop(self.position[0], self.position[1])
            choice = choices([1,0], [probability, 1-probability])
            if choice == [1]: #drop
                cells1[self.position[0]][self.position[1]] = 1
                pygame.draw.circle(win, (255,0,0), (self.position[0]*10, self.position[1]*10), 3)
                pygame.display.update()
                self.hasItem = False
        elif not emptyCell(self.position) and not self.hasItem:
            probability = probPick(self.position[0], self.position[1])
            choice = choices([1,0], [probability, 1-probability])
            if (choice == [1]): #pick
                cells1[self.position[0]][self.position[1]] = 0
                pygame.draw.circle(win, (0,0,0), (self.position[0]*10, self.position[1]*10), 3)
                pygame.display.update()
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
        global size
        if x>=0 and x<size and y>=0 and y<size:
            self.position = (x,y)
        else:
            self.move1(randint(1,9))

    def move(self):
        self.move1(randint(1,9))

def dispose(n, alive):
    global aliveAntsList
    cont = 0
    while cont < n:
        x = randint(0,size-1)
        y = randint(0,size-1)
        if alive:
            aliveAntsList += [AliveAnt((x,y))]
            cont+=1
            continue
        if cells1[x][y] == 0:
            cont+=1
            cells1[x][y] = 1
            pygame.draw.circle(win, (255,0,0), (x*10, y*10), 3)
            pygame.display.update()


t = threading.Thread(target=display)
t2 = threading.Thread(target=screen)
t.start()
t2.start()
