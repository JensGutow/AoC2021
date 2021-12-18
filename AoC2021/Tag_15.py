from queue import PriorityQueue
from math import inf, sqrt

def read_puzzle(datei):
  with open(datei) as f:
    return {(x,y):int(c)  for y,line in enumerate(f.read().split('\n'))  for x,c in enumerate(line.strip())}

class Item():
  def __init__(self, pre, costs) -> None:
      self.pre = pre
      self.costs = costs

def Dijkstra (grid, start, end, debug=False):
  visited = set()
  grid[start] = 0
  D = {item:Item(None, inf) for item in grid}
  D[start] = Item(None, 0)

  pq = PriorityQueue()
  pq.put((grid[start], start))

  while not pq.empty():
    cost, (x,y) = pq.get()
    visited.add((x,y))
    if debug: print("item aus Stapel: (kosten, x,y)", cost, x,y, " Anzahl visited:",len(visited))
    for (dx,dy) in [(1,0),(0,-1),(-1,0), (0,1)]:
      nb = (x+dx, y+dy)
      if nb not in grid.keys() : continue
      if nb in visited : continue
      if debug: print("  Nachbar: (cost, x,y)", grid[nb],nb)
      k = cost + grid[nb]
      if debug: print("  neue gesamt kosten", k)
      if k < D[nb].costs:
        D[nb].costs = k
        D[nb].pre = (x,y)
        pq.put((k, nb))
        if debug: print(f"  udpate D[{nb}] = costs({k}), pre({x,y}))")
  return D[end].costs

def solve(grid, part2):
  
  if part2:
    BigGrid = {}
    DIM = int(0.4 + sqrt(len(grid)))
    for y in range(5*DIM):
      for x in range(5*DIM):
        x_ = x % DIM
        y_ = y % DIM
        k = grid[(x_,y_)] + x//DIM + y//DIM
        BigGrid[(x,y)] = k if k < 10 else k%9
    grid = BigGrid
  DIM = int(0.4 + sqrt(len(grid)))
  START = (0,0)
  END = (DIM-1,DIM-1)
  risk = Dijkstra(grid, START, END)
  return risk 
     
puzzle = read_puzzle('Tag_15.txt')
print("part1" ,solve(puzzle, part2=False))
print("part2" ,solve(puzzle, part2=True))