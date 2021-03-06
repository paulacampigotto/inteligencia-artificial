import pygame
from pygame.locals import *
from pprint import pprint
from random import choices
from random import randint
from math import ceil
from threading import Thread
import timeit
import math

size = 50
radius = 1
kPick = 0.1
kDrop = 0.3
it = 1000000

deadAnts = 400
aliveAnts = 90
aliveAntsList = []
cells1 = [[() for i in range(size)] for i in range(size)]
data = []

pygame.init()
win = pygame.display.set_mode((size*10,size*10))
pygame.display.set_caption("Ant Clustering")


def screen():
    while True:
        pygame.time.delay(100)


def display():
    global cells1
    dispose(deadAnts,False, data)
    dispose(aliveAnts,True,[])

    for i in range(1,it+1):
        #print(i)
        for ant in aliveAntsList:
            if(i==it//2 or i== it//4 or i==1 or i==it or i==3*it//4):
                win.fill((255,255,255))
                for k in range(size):
                    for j in range(size):
                        if(cells1[k][j] != ()):
                            if(cells1[k][j][2] == 1):
                                pygame.draw.rect(win, (145,193,255), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 2):
                                pygame.draw.rect(win, (255,145,218), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 3):
                                pygame.draw.rect(win, (147,255,145), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 4):
                                pygame.draw.rect(win, (255,210,97), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 5):
                                pygame.draw.rect(win, (66,135,245), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 6):
                                pygame.draw.rect(win, (197,66,245), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 7):
                                pygame.draw.rect(win, (245,66,126), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 8):
                                pygame.draw.rect(win, (25,224,227), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 9):
                                pygame.draw.rect(win, (147,255,145), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 10):
                                pygame.draw.rect(win, (118,245,226), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 11):
                                pygame.draw.rect(win, (101,186,26), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 12):
                                pygame.draw.rect(win, (255,251,143), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 13):
                                pygame.draw.rect(win, (255,147,38), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 14):
                                pygame.draw.rect(win, (247,33,0), (k*10, j*10, 10,10))
                            elif(cells1[k][j][2] == 15):
                                pygame.draw.rect(win, (161,16,158), (k*10, j*10, 10,10))
                            else:
                                pygame.draw.rect(win, (0,0,0), (k*10, j*10, 10,10))
                                print(type(cells1[k][j][2]))
                if(i!=it):
                    for _ant in aliveAntsList:
                        pygame.draw.rect(win, (0,0,0), (_ant.position[0]*10, _ant.position[1]*10, 10,10))
                pygame.display.update()
            ant.live()
        print('Working... {:.2f} % iteration {}'.format(100*i/it, i), end='\r')

    stop = timeit.default_timer()

    print('Time: ', stop - start)
    print('Alive ants: ',aliveAnts)
    print('Dead ants: ', deadAnts)
    print('Cells: ' ,size*size)
    print('Radius: ',radius)
    print('kPick: ',kPick)
    print('kDrop: ',kDrop)
    print('Iterations: ', it)

def probPick(x,y):
    global size, radius, kPick,alpha
    distance=0
    itemsAround = 0
    for i in range(-1*radius,radius+1):
        for j in range(-1*radius,radius+1):
            if (i==0 and j==0) or x+i<0 or y+j<0 or x+i>=size or y+j>=size:
                continue
            if cells1[x+i][y+j] != ():
                distance = math.sqrt( ( (cells1[x][y][0] - cells1[x+i][y+j][0]) ** 2) + ( (cells1[x][y][1] - cells1[x+i][y+j][1]) ** 2 ) )
                if(distance <=4):
                    itemsAround+=1
    return (kPick/(kPick + itemsAround)) ** 2 # Função P do artigo

def probDrop(x,y,item):
    global size, radius, kDrop,alpha
    distance=0
    itemsAround = 0
    for i in range(-1*radius,radius+1):
        for j in range(-1*radius,radius+1):
            if (i==0 and j==0) or x+i<0 or y+j<0 or x+i>=size or y+j>=size:
                continue
            if cells1[x+i][y+j] != ():
                distance = math.sqrt( ( (item[0] - cells1[x+i][y+j][0]) ** 2) + ( (item[1] - cells1[x+i][y+j][1]) ** 2 ) )
            if(distance <= 4):
                itemsAround+=1
    return ((itemsAround/(kDrop+itemsAround)) ** 2) # Função P do artigo

def emptyCell(position):
    return cells1[position[0]][position[1]] == ()

class AliveAnt:
    def __init__(self, position):
        self.item = ()
        self.position = position

    def live(self):
        global cells1
        self.move()
        if emptyCell(self.position) and self.item != ():
            probability = probDrop(self.position[0], self.position[1], self.item)
            choice = choices([1,0], [probability, 1-probability])
            if choice == [1]: #drop
                cells1[self.position[0]][self.position[1]] = self.item
                self.item = ()
        elif not emptyCell(self.position) and self.item == ():
            probability = probPick(self.position[0], self.position[1])
            choice = choices([1,0], [probability, 1-probability])
            if (choice == [1]): #pick
                self.item = cells1[self.position[0]][self.position[1]]
                cells1[self.position[0]][self.position[1]] = ()

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

def dispose(n, alive, data):
    global aliveAntsList
    cont = 0
    if not alive: n = min(n, len(data))
    while cont < n:
        x = randint(0,size-1)
        y = randint(0,size-1)
        if alive:
            aliveAntsList += [AliveAnt((x,y))]
            cont+=1
            continue
        if cells1[x][y] == ():
            cont+=1
            cells1[x][y] = data[cont-1]


def readFile():
    global data
    file = open('values15.txt','r')
    lines = file.readlines()
    data = []
    for i in lines:
        k = i.replace(',','.').split('\t')
        if len(k) < 3: continue
        x = k[0]
        y = k[1]
        z = k[2]
        if(x.startswith('-')):
            x = x.split('-')[1]
            x = float(x) * -1
        else: x = float(x)
        if(y.startswith('-')):
            y = y.split('-')[1]
            y = float(y) * -1
        else: y = float(y)
        z = int(z)
        data.append((x,y,z))

readFile()

start = timeit.default_timer()
Thread(target=display).start()
Thread(target=screen).start()
