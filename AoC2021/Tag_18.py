import functools

def read_puzzle(datei):
    s = None
    with open(datei) as f:
        return [eval(line.split("\n")[0]) for line in f.read().split("\n")]   


class Number():
    def __init__(self, initList : list, parent, c=None) -> None:
        self.c = self.left = self.right = self.parent = None
        if c != None:
            self.parent = parent
            self.c = c
        else:
            left, right = initList
            self.parent = parent
            
            left_c = left if isinstance(left, int) else None
            self.left = Number(left, self, left_c)

            right_c = right if isinstance(right, int) else None
            self.right = Number(right, self, right_c)

    def GetRoot(self):
        while self.parent:
            self = self.parent
        return self

    def GetSeals(self, node, seals):
        if node.left: 
            self.GetSeals(node.left, seals)
        if node.c != None: 
            seals.append(node)
        if node.right: 
            self.GetSeals(node.right, seals)

    def GetPrecSucc(self, node):
        root = self.GetRoot()
        prec = succ =  None
        nodeFound = False
        seals = []
        self.GetSeals(root, seals)
        for seal in seals:
            if seal not in [node.left, node.right]:
                if not nodeFound:
                    prec = seal
                else:
                    succ = seal
                    break
            else: 
                nodeFound = True
        return prec, succ
                
    def __repr__(self) -> str:
        if (self.c != None): return str(self.c)
        left = self.left.__repr__()
        right =self.right.__repr__()
        return "[" + left + "," + right + "]"

    def clear_child(self, number):
        self.right = self.left = None
        self.c = 0        

    def is_atomic(self) -> bool:
        return (self.left.c != None) and (self.right.c != None)

    def split(self) -> bool:
        result = False
        if self.c != None:
            if self.c >= 10:
                a = self.c//2
                b = self.c-a
                self.left = Number("", self, a)
                self.right = Number("", self, b)
                self.c = None
                result =  True
        else:
            result = self.left.split()
            if not result:
                result = self.right.split()
        return result

    def explode(self, depth ) -> bool:
        if self.c != None: return False  # its only a int
        
        exploded = False
        if self.is_atomic() and depth > 4:
            prec, succ = self.GetPrecSucc(self)
            if prec: prec.c += self.left.c
            if succ: succ.c += self.right.c
            self.clear_child(self)
            exploded =  True
        else:
            exploded =  self.left.explode( depth+1)
            if not exploded:
                exploded = self.right.explode(depth+1)
        return exploded

    def reduce(self):
        reduced = True
        while(reduced):
            if not self.explode(1):
                reduced = self.split()
                
    def add(self, other):
        s = Number([0,0],None)
        s.left = self
        s.right = other
        s.c = None
        self.left.parent = s
        self.right.parent = s
        s.reduce()
        return s

    def magnitude(self):
        if self.c != None: return self.c
        else: return 3* self.left.magnitude() + 2*self.right.magnitude()

ROOT = None  

def solve(puzzle):
    # n1 = Number([1,[2,[3,[9,[5,6]]]]], None)
    # print(n1)
    # n1.reduce()
    # print(n1)
    # return

    # n1 = Number([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]], None)
    # n1.reduce()
    # print(n1)
    # print()

    # a = Number([[[[4,3],4],4],[7,[[8,4],9]]], None)
    # b = Number([1,1], None)
    # c = a.add(b)
    # print("a",a)
    # print("b",b)
    # print("c",c)

    numbers = [Number(nr, None) for nr in puzzle]
    n = numbers[0]
    print("n[0]:", n)
    for i,nr in enumerate(numbers[1:]):
        print("  ", n)
        print("+ ", nr)
        n = n.add(nr)
        print("= ", n,"\n")



    


puzzle = read_puzzle('Tag_18_Bsp.txt')

solve(puzzle)
