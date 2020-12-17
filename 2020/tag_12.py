import time
from math import sin, cos, pi, radians

def get_puzzle(file_name):
    p = []
    with open(file_name) as f:
        for zeile in f:
            p.append([zeile[0], int(zeile[1:])])
    return p


class turtle():
    DIRS = list("NESW")
    ACTIONS = list("NESWLRF")
    def __init__(self, x=0, y=0, dir=90, kind=0):
        self.dir = dir
        self.x = x
        self.y = y
        self.kind = kind
    
    def rotate(self, dir_offset):
        if self.kind != 0:
            #"drehe" den vektor x,y umd den winkel
            w = dir_offset // 90
            if w<0:
                w+=4
            sin_alpha, cos_alpha  = [[0,1],[1,0],[0,-1],[-1,0]][ [0,1,2,3].index(abs(w))]
            x = cos_alpha * self.x + sin_alpha * self.y
            y = - sin_alpha * self.x + cos_alpha * self.y
            self.x = x
            self.y = y
        else:
            self.dir = (self.dir + dir_offset) % 360
            if self.dir < 0: self.dir + 360

    def move(self, cmd, value):
        if cmd in self.DIRS:
            dx,dy = [[0,1],[1,0],[0,-1],[-1,0]][self.DIRS.index(cmd)]
            self.x += dx * value
            self.y += dy * value

    def forward(self, value):
        dx, dy = {0:[0,1],90:[1,0],180:[0,-1],270:[-1,0]}[self.dir]
        self.x += dx * value
        self.y += dy * value

    def get_distance(self, x=0,y=0):
        return abs(x - self.x) + abs(y - self.y)

    def action(self, cmd, value):
        if   cmd == "R":         
            self.rotate(value)
        elif cmd == "L":         
            self.rotate(-value)
        elif cmd in self.DIRS:  
            self.move(cmd, value)
        else: 
            self.forward(value)

    def __str__(self):
        return "pos:[" + str(self.x) + "," +  str(self.y) +")  dir(grad):" + str(self.dir) + " distance:" +str(self.get_distance())

class ship():
    def __init__(self):
        self.wp = turtle(10,1,0,1)
        self.x = 0
        self.y = 0
    
    def action(self, cmd, value):
        if cmd == "F":
            self.x += value * self.wp.x
            self.y += value * self.wp.y
        else:
            self.wp.action(cmd, value)

    def get_distance(self):
        return abs(self.x) + abs(self.y)

    def __str__(self):
        s = "pos: (" + str(self.x)+ " " + str(self.y) + ") WP: " + self.wp.__str__() + " "
        return s

p = get_puzzle("tag_12.txt")
s = turtle()
print("-------\ntask1-------")
for cmd,value in p:
    s.action(cmd, value)
print(s.get_distance())

print("-------\ntask2-------")
s = ship()
print(s)
print("start")
for cmd,value in p:
    s.action(cmd, value)
    print(cmd, value, "->",s)
print(s.get_distance())