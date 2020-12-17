import time
def get_puzzle(file_name):
    l = []
    with open(file_name) as f:
        for line in f:
            l.append(int("0b" + line.strip().replace("F","0").replace("B","1").replace("L","0").replace("R","1"), 2))
    return l

start = time.perf_counter()
l = get_puzzle("tag_05.txt")
l.sort()
print(l[-1],   time.perf_counter() - start)

start = time.perf_counter()
i = int(l[-1] - (sum(l) - ((l[0] + l[-1] - 1)*len(l)/2)))
print(i,i2,time.perf_counter() - start)