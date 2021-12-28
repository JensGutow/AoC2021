from copy import deepcopy
from collections import Counter, defaultdict
import re
from functools import reduce
import operator #  flatten a lists with  reduce(operator.concat, l)

class Cube:
  def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax) -> None:
      assert xmin <= xmax
      assert ymin <= ymax
      assert zmin <= zmax

      self.coords = [(xmin, xmax), (ymin, ymax) ,(zmin, zmax)]

  def __hash__(self):
    return hash(tuple(self.coords))
  
  def __eq__(self, other):
    return self.__hash__() == other.__hash__()

  def intersection(self, other):
    test = [ (max(item[0]) < min(item[1])) or (min(item[0]) > max(item[1])) for item in  list(zip(self.coords, other.coords))]
    has_intersection = not any(test)
    if not has_intersection: return None
    cube_coords = [(max(i[0][0], i[1][0]), min(i[0][1], i[1][1]))  for i in  list(zip(self.coords, other.coords))]
    cube_coords = reduce(operator.concat, cube_coords) # Flatten the list
    cube = Cube(*cube_coords)
    return cube
  
  def getVolume(self):
        v = 1
        for c in self.coords:
          dV = (c[1] - c[0] + 1)
          assert dV >= 0
          v *= dV
        return v

  def __str__(self) -> str:
    s = ""
    for c in self.coords:
          s += "(" + str(c[0]) + ", " + str(c[1]) +") "
    return s

  def __repr__(self):
    return self.__str__()

  

def parse_cube(line:str, limitCoords):
    swtich, line = line.split(" ")
    coords = [int(i) for i in re.findall("-?\d+", line)]
    if limitCoords and  ((min(coords) < -50) or (max(coords) > 50)):
      c = None
    else:
      c = (swtich=="on", Cube(*coords))
    return c

def read_puzzle(datei, part1):
  with open(datei) as f:
    return [cube for cube in  [parse_cube(line.strip(), part1) for line in f.readlines()] if cube != None]

''''
on x=10..12,y=10..12,z=10..12
off x=9..11,y=9..11,z=9..11
'''

def getTotalVolume(OnCubes):
  v = 0
  for switch_cube, n in OnCubes.items():
    v += n * switch_cube.getVolume()
  return v

def solve(switches_and_cubes):
  OnCubes = Counter()
  
  for switch_cube in switches_and_cubes:
    #print("\ncurrent cube:(swtich, coords, V)", switch_cube, switch_cube[1].getVolume())
    current_switch, current_cube = switch_cube
 
    # ermittle alle Durchschnitte aller bisher bekannten "On"-Wurfel mit dem aktuellen Cube der Eingabe
    # A = ist ein "ON" Cube aus dem Directory OnCubes (iterator), B ist aktueller Cube aus Input
    # V(A + B)  = V(A) + V(B) - V(A intersecion B) - relevant, wenn B ist ein ON-cube
    # V(A - B)  = V(A)        - V(A intersecion B) - relevant, wenn B ist in OFF-cube
    onCubes_temp = Counter()
    for onCube in OnCubes:
      intersection = onCube.intersection(current_cube)
      if not intersection: continue
      assert intersection == current_cube.intersection(onCube)
      onCubes_temp[intersection] -= OnCubes[onCube]
      #print("Intersection found with:", onCube)
      #print("Intersection=", intersection, " V=", intersection.getVolume(), " V_total:", getTotalVolume(OnCubes,  R))

    # wenn aktueller Cube vom Type "on" -> Zaehle dieses Volumen EINMAL dazu
    if current_switch:
        onCubes_temp[current_cube] += 1
        #print("add curent cube to dict, V:", current_cube.getVolume(), " V_total:", getTotalVolume(OnCubes,  R))

    for c in onCubes_temp:
        OnCubes[c] += onCubes_temp[c]
  return getTotalVolume(OnCubes)
  
def test():
  coords_intersection = [5,9,-1,9,-12,3]

  no_interssection = [
    [4,5,-1,9,-12,3],
    [5,9,-3,-1,-12,3],
    [4,5,-1,9,-20,-12],
    [9,10,-1,9,-12,3],
    [5,9,9,10,3,4]
  ]
  c_i = Cube(*coords_intersection)
  c_no_i = [Cube(*c) for c in no_interssection]

  for c in c_no_i:
    assert(c.intersection(c_i)  == None)

  is_bigger = [
      [4,9,-1,9,-12,3],
      [5,9,-2,9,-12,3],
      [5,9,-1,9,-13,3],
      [5,10,-1,9,-12,3],
      [5,9,-1,10,-12,3],
      [5,9,-1,9,-12,4]
    ]
  c_no_i = [Cube(*c) for c in is_bigger]
  for c in c_no_i:
        assert(c.intersection(c_i)  == c_i)


  

cubes = read_puzzle('Tag_22.txt', True)
print("Part1:", solve(cubes))

cubes = read_puzzle('Tag_22.txt', False)
print("Parat2:",solve(cubes))

#test()