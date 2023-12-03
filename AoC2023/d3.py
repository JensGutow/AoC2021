import re

def read_puzzle(file):
    return open(file).read().splitlines()
    
def solve1(puzzle):
    symbols = set()
    gears = set()
    numbers = dict()
    for i, line in enumerate(puzzle):
        it_nr = re.finditer("\d+", line)
        it_symb = re.finditer("[^0-9^.]", line)
        it_gear = re.finditer("[*]", line)
        for it in it_symb:
            symbols.add((i, it.start()))
        for it in it_gear:
            gears.add((i, it.start()))
        for it in it_nr:
            first = it.start()
            last = it.end()
            number = int(it.string[first:last])
            possible_pos = set()
            for i_ix in range(i-1,i+2):
                for j_ix in range(first-1, last+1):
                    possible_pos.add((i_ix, j_ix))
            numbers[(i,first, number)] = possible_pos
    sum = 0
    for nr_key, nr_set in numbers.items():
        if symbols.intersection(nr_set):
            sum += nr_key[2]

    gear_ratio = 0
    tested = set()
    for gear in gears:
        for nr_key, nr_set in numbers.items():
            if not gear in nr_set: continue
            for nr_key_2, nr_set_2 in numbers.items():
                if nr_key_2 == nr_key: continue
                if not gear in nr_set_2: continue
                if (nr_key[2], nr_key_2[2]) in tested: continue
                gear_ratio += nr_key[2] * nr_key_2[2]
                tested.add((nr_key[2], nr_key_2[2]))
                tested.add((nr_key_2[2], nr_key[2]))

    return sum, gear_ratio


puzzle = read_puzzle('d3.txt')

print("Task 1", solve1(puzzle))
#print("Task 2", solve1(puzzle))