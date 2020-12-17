import time
from numpy import lcm, uint64

class puzzle():
    def __init__(self,file_name):
        with open(file_name) as f:
            p = f.read().strip().split("\n")
        self.start_time = int(p[0])
        ids_raw = p[1].strip().split(",")
        self.ids = [int(id) for id in ids_raw if id != "x"]
        self.ids2 = [(dt,int(id)) for dt, id in enumerate(ids_raw) if id != "x"]
        
    def löse1(self):
        wartezeit = [id - self.start_time % id for id in self.ids]
        id =  wartezeit.index(min(wartezeit))
        return self.ids[id] * wartezeit[id]
    
    def löse2(self):
        kgv_old = kgv = uint64(1)
        id = dt = time = uint64(0)
        for dt, id in self.ids2:
            dt = dt % id #  SollWartezeit > BusID == "ZyklusZeit des Busses" 
            kgv_old = kgv
            kgv = lcm(kgv, uint64(id)) #least common multiple from numpy (10 times faster as native *)
            for _ in range(id):
                if ((id - time) % id) == dt: break
                time += kgv_old     
        return time

p = puzzle("tag_13.txt")
print("Task 1")
start =time.perf_counter()
print(p.löse1())
print(time.perf_counter() - start)

print("Task 2")
start =time.perf_counter()
print(p.löse2())
print(time.perf_counter() - start)