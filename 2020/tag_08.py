import time

def get_puzzle(file_name):
    p = []
    with open(file_name) as f:
        for line in f:
            cmd, offs = line.strip().split()
            p.append([cmd, int(offs)])
    return p

def solve_1(puzzle):
    inx = 0
    sum = 0
    check = []
    while  (inx>=0) and (inx < len(puzzle)) and (inx not in check):
        check.append(inx)
        cmd, value = puzzle[inx]
        if cmd == "nop":
            inx += 1
        elif cmd == "acc":
            inx += 1
            sum += value
        else:
            inx += value
    return sum, inx >= len(puzzle)

def solve_2(puzzle):
    inx = 0
    is_finite = False
    old_cmd = ""
    while not(is_finite): 
        inx_offs = next((i for i,x in enumerate(puzzle[inx:]) if x[0] !=  "acc"),-1)
        if inx_offs>=0:
            inx += inx_offs
            #print(inx)
            old_cmd = puzzle[inx][0]
            puzzle[inx][0] = "jump" if old_cmd == "nop" else "nop"
            i = inx
            sum , is_finite = solve_1(puzzle)
            puzzle[inx][0] = old_cmd
            inx +=1
        if (inx<0) or (inx>=len(puzzle)):
            is_finite = True
    return sum, is_finite    

p = get_puzzle("tag_08.txt")
start = time.perf_counter()
result, is_finite = solve_1(p)
dt_ms =  (time.perf_counter() - start) * 1000
print("L1:", result, dt_ms)

start = time.perf_counter()
result, is_finite = solve_2(p)
dt_ms =  (time.perf_counter() - start) * 1000
print("L2:", result, dt_ms)

