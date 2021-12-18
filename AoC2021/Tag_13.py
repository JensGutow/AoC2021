def read_puzzle(datei):
  with open(datei) as f:
    text = f.read()
    dots, folds = text.split("\n\n")
    dots =   [[int(dot) for dot in line.split(",")] for line in dots.split("\n") ] 
    folds1 = [line.strip().split("=") for line in folds.strip().split("\n")]
    folds=[]
    for fold_dir, coord in folds1:
      folds.append(["x" if "x" in fold_dir else "y", int(coord)])
    return dots, folds

l1 = lambda val, comp: val if val <= comp else 2*comp-val
lx = lambda dot, comp: (l1(dot[0], comp[1]), dot[1])
ly = lambda dot, comp: (dot[0], l1(dot[1], comp[1]))

def fold(dots, fold):
  f_fold = lx if fold[0]=="x" else ly
  s = {f_fold(dot, fold) for dot in dots}
  return s

def report_result(s):
  t = list(zip(*s)) #transpose
  minx = min(t[0])
  maxx = max(t[0])
  miny = min(t[1])
  maxy = max(t[1])
  print("M A T R I X")
  for y in range(miny, maxy+1):
    row=""
    for x in range(minx,maxx+1):
      row = row + ("#" if (x,y) in s else " ")
    print(row)

def löse(dots, folds):
  for fold_ in folds:
    dot1 = fold(dots, fold_)
    dots = list(dot1)
  report_result(dots)

dots, folds = read_puzzle('Tag_13.txt')
löse(dots, folds)

'''
 M A T R I X
  ## ###  ####  ##  #  #  ##  #  # ### 
   # #  #    # #  # #  # #  # #  # #  #
   # #  #   #  #    #  # #  # #  # #  #
   # ###   #   #    #  # #### #  # ### 
#  # #    #    #  # #  # #  # #  # # # 
 ##  #    ####  ##   ##  #  #  ##  #  #
 '''