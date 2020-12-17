import time

def get_puzzle(file_name):
    d = {}
    z = 0
    with open(file_name) as f:
        for zeile in f:
            for s, c in enumerate(zeile.strip()):    
                d[z,s] = c   
            z += 1 
    return d

def get_number_occ_seats(d):
    return list(d.values()).count("#")

def get_number_occ_neighbors1(d, z, s):
    deltas = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    n = 0
    for dx,dy in deltas:
        if d.get((z+dx, s+dy),".") == "#":
            n += 1
    return n

def get_number_occ_neighbors2(d, z, s):
    deltas = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    n = 0
    for dx,dy in deltas:
        i = 1
        while True:
            c = d.get((z + (dx*i), s + (dy*i)),"E")
            if c in "EL": break
            if c == "#":
                n += 1
                break
            i+=1
    return n

def iteration1(d):
    result = {}
    c_new = ""
    for (x,y), c in d.items():
        n_occ = get_number_occ_neighbors1(d, x, y)
        if c == "#" and n_occ >= 4: result[x,y] ="L"
        elif c=="L" and n_occ == 0: result[x,y] = "#"
        else: result[x,y] = c
    return result

def iteration2(d):
    result = {}
    c_new = ""
    for (x,y), c in d.items():
        n_occ = get_number_occ_neighbors2(d, x, y)
        if c == "#" and n_occ >= 5: result[x,y] ="L"
        elif c=="L" and n_occ == 0: result[x,y] = "#"
        else: result[x,y] = c
    return result

def task(p, it_fct):
    its = 0
    abbruch = False
    n_occ_seats = get_number_occ_seats(p)
    while not abbruch:
        p = it_fct(p)
        n_occ_seats_new = get_number_occ_seats(p)
        #print(its, n_occ_seats_new)
        if n_occ_seats_new != n_occ_seats:
            its +=1
            n_occ_seats = n_occ_seats_new
        else:
            abbruch = True
    return n_occ_seats

p = get_puzzle("tag_11.txt")
p2 = p.copy()

print("Task 1")
start =time.perf_counter()
n_occ_seats = task(p,iteration1)
print(time.perf_counter() - start)
print(n_occ_seats)

print("Task 2")
p = p2
start =time.perf_counter()
n_occ_seats = task(p,iteration2)
print(time.perf_counter() - start)
print(n_occ_seats)