import time
import re
from anytree import Node, RenderTree

def parse_line(line):
    #pale chartreuse bags contain 3 faded orange bags.
    line.replace(".", "")
    inx = line.index("bags contain")
    key = line[:inx-1].strip()
    content = line[inx + len("bags contain"):].split(",")

drab gold bags contain 5 dark aqua bags.")

def get_puzzle(file_name):
    p = [] 
    with open(file_name) as f:
        for line in f:
            p.append[parse_line(line)]
    return p

def solve_1_2(puzzle):
    pass

p = get_puzzle("tag_07.txt")
start = time.perf_counter()
#results = solve_1_2(p)
dt_ms =  (time.perf_counter() - start) * 1000
#print("Task 1", results[0], "Task 2", results[1], "time needed [ms]: {0:.1f}".format(dt_ms))