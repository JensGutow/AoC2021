import itertools
import time

def get_puzzle(file_name):
    pre_Length = 5
    p = []
    with open(file_name) as f:
        p = [int(i) for i in f.read().split()]   
    return p

def check(text, p_len, i):
    check = [sum(x) for x in itertools.combinations(set(text[i-p_len: i]),2)]
    return text[i] in check

text = get_puzzle("tag_09.txt")

start = time.perf_counter()
p_len = 25
last = current = 0
for i in range(p_len, len(text)):
    if not check(text, p_len, i): break
print(i, text[i], time.perf_counter() - start)


start = time.perf_counter()
th = text[i]
i0 = i1 = 0
s = 2 * text[i0]

check = False
result = None

for i0 in range(len(text)):
    if result: break
    for i1 in range(i0+1, len(text)):
        s = sum(text[i0:i1])
        if s > th: 
            break
        if s == th:
            seq = text[i0:i1]
            min_ = min(seq)
            max_ = max(seq)
            
            result = min_ + max_
            print (result)
            break

print (result, time.perf_counter() - start)

