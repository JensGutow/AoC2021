def read_puzzle(datei):
  with open(datei) as f:
    lines = f.readlines()
    print(lines)

def solve(puzzle):
  flashes = 0
  part2 = None
  for cycle in range(10000):
    #     # 1) inc energy level by 1
    for key in puzzle:
      puzzle[key] += 1

    flashes_per_cycle = 0
    while True:
      pos_to_flash = [key for key,value in puzzle.items() if value > 9]
      flashes_per_cycle = len(pos_to_flash)
      if not pos_to_flash:
        break
      for x,y in pos_to_flash:
        puzzle[(x,y)] = 0
      for x,y in pos_to_flash:
        for pos in ((x+1, y), (x-1, y), (x, y-1), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)):
          if pos in puzzle.keys() and puzzle[pos]>0:
            puzzle[pos] += 1
      if cycle < 100:
        flashes += flashes_per_cycle

    if sum(puzzle.values()) == 0 and not(part2):
      part2 = cycle + 1
      break

  return flashes, part2
 
puzzle = read_puzzle('Tag_11.txt')
print(solve(puzzle))