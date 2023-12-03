import re
from collections import defaultdict
import math

def read_puzzle(file):
    return open(file).read().splitlines()

def solve1(puzzle):
    sum = 0
    power = 0
    sollwerte = {"red":12, "green":13, "blue":14}
    for line in puzzle:
        d = defaultdict(int)
        id = re.findall("\d+:", line)
        id = int(id[0][:-1])
        cubes = re.findall("\d+ [a-z]+", line)
        for cube in cubes:
            infos = cube.split(" ")
            nr = int(infos[0])
            color = infos[1]
            d[color] = max(d[color], nr)
        if(all([d[color] <= sollwerte[color] for color in d.keys()])):
            sum += id
        power += math.prod(d.values())
        
    return sum,power


puzzle = read_puzzle('d2.txt')

print("Task 1, Task2", solve1(puzzle))
