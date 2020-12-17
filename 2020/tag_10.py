import itertools
import time

def get_puzzle(file_name):
    p = []
    with open(file_name) as f:
        p = [int(i) for i in f.read().split()] 
        p.append(0)
        p.append(max(p)+3)
        p.sort()
    return p

def count_def(l, diff):
    c = 0
    for i in range(len(l)-1):
        d = l[i+1]-l[i]
        if d==diff:
            c += 1
    return c

p = get_puzzle("tag_10.txt")
#task 1
start =time.perf_counter()
d1 = count_def(p,1)
d3 = count_def(p,3)
print((d1) *(d3))
print(time.perf_counter() - start)

#task 2
def dp(i, volts, dict_):
    if i==len(volts)-1:
        return 1
    if i in dict_:
        return dict_[i]
    ans = 0
    for j in range(i+1, len(volts)):
        if volts[j] - volts[i] <= 3:
            ans += dp(j,volts, dict_)
    dict_[i] = ans
    return ans

start =time.perf_counter()
print(dp(0, p, {}))
print(time.perf_counter() - start)