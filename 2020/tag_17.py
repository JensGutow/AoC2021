import time
from itertools import product

class gitter():
    def __init__(self, file, dim=3):
        self.g = {}
        self.dim = dim
        self.read_file(file)
        self.richtungen = list(product([-1,0,1], repeat=self.dim))
        self.richtungen.remove(tuple([0]*self.dim))

    def aktive_zellen(self):
        return list(self.g.values()).count(1)

    def aktive_nachbarn_an_pos(self, pos):
        n = 0
        for r in self.richtungen:
            such_pos = self.add_pos(pos, r)
            n += self.g.get(such_pos, 0)
        return n

    @staticmethod
    def add_pos(pos_a, pos_b):
        return tuple(map(sum,(zip(pos_a, pos_b))))

    def iteration(self):
        new_g = {}
        positionen = set(self.g.keys())
        for k in self.g.keys():
            for r in self.richtungen:
                new_pos =  self.add_pos(k,r) 
                positionen.add(new_pos)
        for pos in positionen:
            aktiveZellen = self.aktive_nachbarn_an_pos(pos)
            if  (aktiveZellen == 3) or (self.g.get(pos,0) and (aktiveZellen == 2)):
                new_g[pos] = 1
        self.g = new_g

    def read_file(self, file):
        pos = [0]*self.dim
        with open(file) as f:
            for y, zeile in enumerate(f):
                zeile = zeile.strip()
                for x, c in enumerate(zeile):
                    pos[0] = x
                    pos[1] = y
                    if c=="#":
                        self.g[tuple(pos)] = 1

def löse(file, dim):
    g = gitter(file, dim)
    for i in range(6):
        g.iteration()
        print(i, g.aktive_zellen())
    return g.aktive_zellen()

print("Task 1")
start = time.perf_counter()
print(löse("tag_17.txt",3), time.perf_counter() - start)

print("Task 2")
start = time.perf_counter()
print(löse("tag_17.txt",4), time.perf_counter() - start)