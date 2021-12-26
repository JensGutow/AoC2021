import re
from copy import deepcopy

def read_puzzle(datei):
    with open(datei) as f:
        return [line.strip().replace("."," ") for line in f.readlines()]

def cucumber_step_by_line(line, c):
    l = len(line)
    line = line + line
    line = re.sub(c + " ", " " + c, line)
    line = line[l] + line[1:l]
    return line

def transpose(str_arr):
    str_arr =  list(zip(*str_arr))
    str_arr = list(map("".join, str_arr))
    str_arr = [item for item in str_arr]
    return str_arr

def cucumber_step(arr):
    arr = [cucumber_step_by_line(line, ">" ) for line in arr]
    arr = transpose(arr)
    arr = [cucumber_step_by_line(line, "v") for line in arr]
    arr = transpose(arr)
    return arr

def solve(puzzle):
    p2 = None
    p1 = puzzle
    n = 0
    while (p1 != p2):
        n += 1
        p2 = deepcopy(p1)
        p1 = cucumber_step(p2)
    return n

puzzle = read_puzzle('Tag_25.txt')
assert puzzle == transpose(transpose(puzzle)), "transpose"

n = solve(puzzle)
print("part1 : ", n)
