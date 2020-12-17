import time

def löse(p, max):
    d = {} #value -> last_index
    for i,item in enumerate(p[:-1]):
        d[item] = i
    last = p[-1]
    for index in range(len(p) - 1, max - 1):
        new = index - d.get(last, index)
        d[last] = index
        last = new
    return last

p = [7,14,0,17,11,1,2]
print("Task 1")
start = time.perf_counter()
print(löse(p,2020), time.perf_counter() - start)

print("Task 2")
start = time.perf_counter()
print(löse(p,30000000), time.perf_counter() - start)