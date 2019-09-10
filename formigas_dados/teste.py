import math

def readFile():
    global data
    file = open('values.txt','r')
    lines = file.readlines()
    data = []
    for i in lines:
        k = i.split(',')
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
maior = 0
for i in range(len(data)):
    for j in range(len(data)):
        if(data[i][2] == data[j][2]):
            distance = math.sqrt( ( (data[i][0] - data[j][0]) ** 2) + ( (data[i][1] - data[j][1]) ** 2 ) )
            if(distance > maior):
                maior = distance
                print(data[i],data[j], "d= ", maior)
print(maior)
