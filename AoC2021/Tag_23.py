from collections import defaultdict
from math import inf
from typing import DefaultDict
from queue import PriorityQueue
from copy import deepcopy
from functools import reduce

example='''
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''

end='''
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
'''


part1='''
#############
#...........#
###D#A#C#A###
  #D#C#B#B#
  #########
'''


class itemClass():
    HellwayPos = 0
    xMin = 0
    Rooms = {"A":2, "B":4, "C":6, "D":8}
    def __init__(self, name:str, pos) -> None:
        self.pos = pos
        self.name = name.upper()
    
    def setHellwayPos(pos):
        itemClass.HellwayPos = pos

    def setMinX(xMin):
        itemClass.xMin = xMin #offset for Rooms

    def set_pos(self, pos):
        self.pos = pos

    def set_pos(self, pos):
        self.pos = pos

    def is_in_hallway(self):
        return self.pos[1] == itemClass.HellwayPos

    def is_in_own_room(self):
        return not self.is_in_hallway() and self.Rooms[self.name] + itemClass.xMin == self.pos[0]

    def is_in_foreign_room(self):
        return not self.is_in_hallway() and not self.is_in_own_room()

    def __lt__(self, other):
        return True

    def distance(self, other) -> int:
        return abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])

    def __repr__(self) -> str:
        return "Item pos:" + str(self.pos) + " Name:" + self.name

class burrow():
    COSTS = {"A":1, "B":10, "C":100, "D":1000}
    def __init__(self, inputStr) -> None:
        grid_1 = {}
        grid_1 = {(x,y):c for y, line in enumerate(inputStr.split("\n")) for x,c in enumerate(line) if c not in  " #"}
        minY = min( list(zip(*grid_1.keys()))[1])
        minX = min( list(zip(*grid_1.keys()))[0])
        itemClass.setHellwayPos(minY)
        itemClass.setMinX(minX)
        self.items = []
        self.grid = DefaultDict(set)
        for item in grid_1.items():
            pos, c = item
            #print(pos, c)
            x,y = pos
            for dPos in [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]:
                if dPos in grid_1.keys():
                    self.grid[pos].add(dPos)
                    self.grid[dPos].add(pos)
            if c  not in ".#":
                self.items.append(itemClass(c, pos))
        #print(self.items)
    
    def __lt__(self, other):
        return True
    
    def rules_fulfilled(self, item:itemClass, newPos):
        newItem = itemClass(item.name, newPos)
        # Flur -> Flur: verboten
        if item.is_in_hallway() and newItem.is_in_hallway(): 
            #print("Flur -> Flur: false")
            return False

        # Raum -> Flur : im Flur  mindestens eine Position bewegt
        if not(item.is_in_hallway()) and newItem.is_in_hallway() and abs(newItem.pos[0] - item.pos[0]) < 1 : 
            #print("Raum -> Flur: dx == 0 : false")
            return False

        # Bewegung nur im aktuellen  Raum verboten (nachshauen, ob das so stimmt - evtl. diese Regel löschen) -> die wird NICHT gefordert
        if not(item.is_in_hallway()) and not(newItem.is_in_hallway()) and item.pos[0] == newItem.pos[0] : return False

        # nicht-eigene Räume sind als Ziel verboten
        if newItem.is_in_foreign_room() : 
            #print("Ziel fremder Raum:  false")
            return False

        # es bleibt zu prüfen, wenn Ziel eigener Raum ist, dass kein fremder drinn ist
        result = True
        if newItem.is_in_own_room():
            newItemX = newItem.pos[0]
            for i in self.items:
                if i.is_in_foreign_room() and (i.pos[0] == newItemX):
                    result = False
                    break
            if not result:
                #print("Ziel ist eigener Raum - aber mit Fremden: False")
                pass
        return result

    def get_nbs_by_pos_and_grid(self, visited,item, costs_per_step, pos, nbs ):
        # "Schritt für Schritt" -> wenn Kollistion mit Wand oder anderem Item -> Abbruch
        # an einer Kreuzung -> gehe rekursive alle Wege
        # vermeide schon unersuchte Positionen (visited)
        # an einer leeren Position (Kandidat für Ziel der Bewegung): Prüfe, ob alle Regeln erfüllt sind -> ja: neues Element in die Warteschlange
        #print("from:",item, " to:",pos)
        # untersuchter Raum  wird "gesperrt"
        visited.add(pos)
        item_pos = {}
        item_pos = {item.pos for item in self.items}        
        assert(pos in self.grid.keys())
        if pos in item_pos:
            #kollision mit Flusskrebs
            #print("kollision")
            return
        steps = abs(pos[0] - item.pos[0]) + abs(pos[1] - item.pos[1])
        costs = steps * costs_per_step
        nbs_item = (costs, (item,pos))
        
        if self.rules_fulfilled(item, pos):
            #print("rules are fulfilled")
            nbs.append(nbs_item)

        # gehe nun rekursiv um einen Schritt weiter weiter
        next_pos_set = (set(self.grid[pos]) - visited)
        for next_pos in next_pos_set:
            self.get_nbs_by_pos_and_grid(visited, item, costs_per_step, next_pos, nbs)
  
    def get_nbs_by_item(self, item, nbs:list) :
        for pos in set(self.grid[item.pos]):
            visited = set()
            visited.add(item.pos)
            # gehe alle direktaen Nachbaren vom Item durch, gehe nicht über item
            self.get_nbs_by_pos_and_grid(visited,item, self.COSTS[item.name], pos, nbs )


    def get_nbs(self) -> PriorityQueue:
        nbs =  []
        for item in self.items:
            self.get_nbs_by_item(item, nbs)
        return nbs

    def is_end(self):
        return all(list(map(itemClass.is_in_own_room, [i for i in self.items])))

    def __repr__(self) -> str:
        id = {}
        for item in self.items:
            id[item.pos] = item
        maxX = maxY = 0
        minX = minY = inf
        for pos in self.grid.keys():
            x,y = pos
            maxX = max(maxX, x)
            maxY = max(maxY, y)
            minX = min(minX, x)
            minY = min(minY, y)
        out = [" " * (maxX - minX + 1) + "\n" for _ in range((maxY-minY + 1))]
        for pos in self.grid.keys():
            x,y = pos
            c = "." if pos not in id.keys() else id[pos].name 
            out[y-minY] = out[y-minY][:max(x-1,0)] + c + out[y-minY][min(x+1,maxX):1+maxX]
        return reduce(lambda x,y:x+"\n"+y, out)

def copy_and_update_burrow(b, item, pos):
    b_next = deepcopy(b)
    for i in b_next.items:
        if i.name == item.name and i.pos == item.pos:
            i.pos = pos
            break
    return b_next

def Dijkstra (start, debug=False):
    visited = set()
    D = {}
    start_print = start.__repr__()
    D[start_print] = (None, 0)
    pq = PriorityQueue()
    pq.put((0, start_print))
    R = {}
    R[start_print] =  start
    i = 0
    
    while not pq.empty():
        cost_b, b = pq.get()
        b = R[b]
        if b.is_end():
            return D, b, cost_b

        i += 1
        if i>100:
            i = 0
            print("-> next burrow state:")
            print(b, "\n")
            print("neighbar states")
            nbs = b.get_nbs()
            for nb in nbs:
                print(nb)

        for nb_next in b.get_nbs():
            cost_next, (item_next, pos_next) = nb_next
            b_next = copy_and_update_burrow(b, item_next, pos_next)
            if b_next.__repr__() in visited : 
               continue
            k = cost_next + cost_b
            b_next_hash = b_next.__repr__()
            if not b_next_hash in D.keys():
                R[b_next_hash] = b_next
                D[b_next_hash] = (b, k)
                pq.put((k, b_next_hash))
            else:
                if k < D[b_next_hash][1]:
                    D[b_next_hash] = (b, k)
                    pq.put((k, b_next_hash))

test1 = '''
.......B...
  B C . D
  A D C A
'''
# Burrow_Flur = burrow(test1)
# print(Burrow_Flur)
# nbs = Burrow_Flur.get_nbs()
# for nb in nbs:
#     print(nb) 

# Burrow_end = burrow(end)
# print("Burrow_end", Burrow_end.is_end())

Burrow = burrow(example)
print(Burrow)
result = Dijkstra(Burrow)
print(result[1])
print(result[2])
print(result[0])

