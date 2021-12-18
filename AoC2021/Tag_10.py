from  queue import LifoQueue, Queue

def read_puzzle(datei):
  with open(datei) as f:
    return [line.strip() for line in f]

PAIRS = {"(":")", "[":"]", "{":"}", "<":">"}
COSTS = {")":3, "]":57, "}":1197, ">":25137, "(":1, "[":2, "{":3, "<":4}

def syntax_error_score(line, part1):
      q = LifoQueue()
      for c  in line:
        if c in PAIRS.keys():
          q.put(c)
        else:
          if q.empty() or PAIRS[q.get()] != c:
            return COSTS[c] if part1 else 0
      if part1:
        return 0
      else:
        q2 = []
        while not(q.empty()):
          q2.append(q.get())
        cost2=0
        for c in q2:
          cost2 = 5*cost2 + COSTS[c]
        return cost2
              

def solve(puzzle, part1):
  costs = 0
  costs2 = []
  for i,line in enumerate(puzzle):
    cost = syntax_error_score(line, part1)
    if part1:
      costs += cost
    else:
      if cost:
        costs2.append(cost)
  if part1:
    return costs
  else:
    costs2.sort()
    middle = int((len(costs2) - 1)/2)
    return costs2[middle]
       

puzzle = read_puzzle('Tag_10.txt')
print("lösung1:", solve(puzzle, True))
print("lösung2:", solve(puzzle, False))