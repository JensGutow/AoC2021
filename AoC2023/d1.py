import re
def read_puzzle(file):
    return open(file).read().splitlines()

def solve(puzzle, part1):
    nrs = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    nrs_repl = []
    for i, nr in enumerate(nrs):
        nrs_repl.append([nr, nr+str(i+1)+nr])
    
    sum = 0
    for line in puzzle:
        if not part1:
            for a,b in nrs_repl:
                line = line.replace(a,b)
        nrs = re.findall("[\d]", line)
        sum += int(nrs[0])*10 + int(nrs[-1])
    return sum


puzzle = read_puzzle('d1.txt')

print("Task 1", solve(puzzle, True))
print("Task 2", solve(puzzle, False))