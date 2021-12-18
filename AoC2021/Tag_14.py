
from typing import DefaultDict, Counter
from copy import deepcopy

def read_puzzle(datei):
  with open(datei) as f:
    pol, rules = f.read().strip().split("\n\n")
    rules = {r[0].strip() : r[1].strip() for r in [rule.split("->") for rule in rules.split("\n")]}
  return pol, rules

def löse(pol, rules, n):
  P = DefaultDict(int)
  C = Counter()
  for c in pol:
    C.update(c)
  for i,c in enumerate(pol[:-1]):
    P[c+pol[i+1]] = 1
  
  for _ in range(n):
    P_temp = DefaultDict(int)
    P_copy = deepcopy(P)
    for p_key, p_item in P_copy.items():
      c = rules[p_key]
      C[c] += p_item
      del P[p_key]
      P_temp[p_key[0] + c] += p_item
      P_temp[c + p_key[1]] += p_item
    for key, item in P_temp.items():
      P[key] += item
  v = max(C.values()) - min(C.values())
  return v
        
puzzle = read_puzzle('Tag_14.txt')
print("part1:", löse(*puzzle, 10))
print("part2:", löse(*puzzle, 40))