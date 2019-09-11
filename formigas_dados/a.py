from random import random, randint
import pygame
import pandas as pd
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 000, 255)

values = [0, 255, 128]
colors = []
for r in values:
    for g in values:
        for b in values[:2]:
            colors.append((r, g, b))

N = 30
n_ants = 20
alpha = 1.5 #1.3
sigma = 1.7 #2
life = 100
moves = 10

MARGIN = 2
WIDTH = 600 / N - MARGIN
HEIGHT = 600 / N - MARGIN
WINDOW_SIZE = [600, 600]

vision_range = 1
dead_ants = []
alive_ants = []
items = []

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.carrying = {}
        self.life = life
        alive_ants[self.x][self.y] += 1


    def move(self, size):
        if self.life <= 0 and self.carrying == {}:
            alive_ants[self.x][self.y] -= 1
        else:
            self.x = (self.x + randint(-1,1)) % size
            self.y = (self.y + randint(-1,1)) % size

            if self.carrying == {} and dead_ants[self.x][self.y] != {}:

                foi = f(self.x, self.y, dead_ants[self.x][self.y])

                if foi <= 1:
                    p = 1
                else:
                    p = 1 / float(foi**2)

                if random() < p:
                    self.carrying = dead_ants[self.x][self.y]
                    dead_ants[self.x][self.y] = {}
                    self.life = life
                else:
                    self.life-=1

            elif self.carrying != {} and dead_ants[self.x][self.y] == {}:

                foi = f(self.x, self.y, self.carrying)

                if foi >= 1:
                    p = 1
                else:
                    p = foi**4

                if random() < p:
                    dead_ants[self.x][self.y] = self.carrying
                    self.carrying = {}
                    self.life = life
                else:
                    self.life-=1

            else:
                self.life-=1

def f(x, y, comparing):
    xmin = x-vision_range
    xmax = x+vision_range+1
    ymin = y-vision_range
    ymax = y+vision_range+1

    foi = 0
    for row in dead_ants[xmin : xmax]:
        for item in row[ymin : ymax]:
            if item != dead_ants[x][y] and item != {}:
                foi += max(1 - dissimilarity(item, comparing) / float(alpha), 0)

    return (foi / float(sigma**2))

def dissimilarity(a, b):
    return np.sqrt((a['pl']-b['pl'])**2 + (a['pw']-b['pw'])**2 +
                   (a['sl']-b['sl'])**2 + (a['sw']-b['sw'])**2)


def generate_grid(size, fill):
    return [[fill for _ in range(size)] for _ in range(size)]

def spreads_itens(dead_ants, items):
    i = 0
    j = 0
    for item in items:
        while(dead_ants[i][j] != {}):
            i = int(random() * len(dead_ants))
            j = int(random() * len(dead_ants))
        dead_ants[i][j] = item
    return dead_ants


df = pd.read_csv('iris.csv', names=['pl', 'pw', 'sl', 'sw', 'specie'])
print(df.dtypes)
items = df.to_dict('index').values()

classes = {'Iris-virginica': 1,
           'Iris-setosa': 2,
           'Iris-versicolor': 3}

alive_ants = generate_grid(N, 0)
dead_ants = spreads_itens(generate_grid(N, {}), items)
ants = [Ant(N) for _ in range(n_ants)]

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Ant Clustering")
done = False
clock = pygame.time.Clock()

screen.fill(BLACK)

count = 0
while(not done):
    for ant in ants:
        alive_ants[ant.x][ant.y] -= 1
        ant.move(N)
        alive_ants[ant.x][ant.y] += 1
    count += 1

    if(count % moves == 0):
        for row in range(N):
            for column in range(N):
                color = BLACK
                if dead_ants[row][column] != {}:
                    specie = dead_ants[row][column]['specie']
                    class_n = classes[specie]
                    color = colors[int(class_n)]
                if alive_ants[row][column] > 0:
                    color = WHITE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        clock.tick(120)
    pygame.display.flip()

pygame.quit()
