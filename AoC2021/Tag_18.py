import functools

def read_puzzle(datei):
    s = None
    with open(datei) as f:
        return [eval(line.split("\n")[0]) for line in f.read().split("\n")]   


class Number():
    debug = False
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

    def GetPrecSucc2_worker(self,node, prec, succ, nodeFound = False):
        if not node: return False, None, None, nodeFound
        result = False
        if self.left: 
            result, prec, succ, nodeFound =  self.left.GetPrecSucc2_worker(node, prec, succ, nodeFound)
            if result : return result, prec, succ, nodeFound

        if self == node: 
            nodeFound = True
        else:
            if (not self in (node, node.left,node.right)) and (self.c != None):
                if nodeFound:
                    succ = self
                    result = True
                    return  result, prec, succ, nodeFound
                else:
                    prec = self

        if self.right: 
            result, prec, succ, nodeFound = self.right.GetPrecSucc2_worker(node,prec, succ, nodeFound)
        
        return result, prec, succ, nodeFound


    def GetAtomicPecSucc2(self, node):
        root = self.GetRoot()
        succ = prec = None
        _, prec, succ, _ =  root.GetPrecSucc2_worker(node, prec, succ)
        return prec, succ
                
    def __repr__(self) -> str:
        if (self.c != None): return str(self.c)
        left = self.left.__repr__()
        right =self.right.__repr__()
        return "[" + left + "," + right + "]"

    def clear_child(self):
        self.right = self.left = None
        self.c = 0        

    def is_atomic(self) -> bool:
        return (self.left.c != None) and (self.right.c != None)

    def split(self) -> bool:
        result = False
        if self.left:
            result = self.left.split()
        if not result:
            if self.c != None:
                if self.c >= 10:
                    a = self.c//2
                    b = self.c - a
                    self.left = Number("", self, a)
                    self.right = Number("", self, b)
                    self.c = None
                    result =  True
            else:
                if self.right:
                    result = self.right.split()
        return result

    def explode(self, depth ) -> bool:
        if self.c != None: return False  # its only a int
        
        exploded = False
        if self.left:
            exploded = self.left.explode(depth+1)
        if not exploded:
            if self.is_atomic() and depth > 4:           
                prec = succ = None
                prec, succ = self.GetAtomicPecSucc2(self)
                if prec: prec.c += self.left.c
                if succ: succ.c += self.right.c
                succ = prec = 0
                self.clear_child()
                exploded =  True
            else:
                if self.right:
                    exploded = self.right.explode(depth+1)
        return exploded

    def reduce(self):
        reduced = True
        if Number.debug: print("REDUCE:", self)
        while(reduced):
            exploded = self.explode(1)
            if exploded and Number.debug:
                print("After explode:", self)

            if not exploded:
                reduced = self.split()
                if reduced and Number.debug:
                    print("After split  :", self)
                
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
 
def test():
    explodeTestVector = [
        [
            [[[[[9,8],1],2],3],4],
             [[[[0,9],2],3],4]
        ],
        [
            [7,[6,[5,[4,[3,2]]]]] ,
            [7,[6,[5,[7,0]]]] 
        ],
        [
            [[6,[5,[4,[3,2]]]],1],
            [[6,[5,[7,0]]],3]
        ],
        [
            [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] 
        ],
        [
            [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
        ],
        [
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[7,0]]]]
        ]
    ]
    print("EXploding Tests")
    for test in explodeTestVector:
        n1 = Number(test[0], None)    
        n2 = Number(test[1], None)    
        n1.explode(1)
        assert n1.__repr__() == n2.__repr__()

    splitTestVector = [ 
        [
            [[[[0,7],4],[15,[0,13]]],[1,1]], [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
        ],
        [
            [[[[0,7],4],[[7,8],[0,13]]],[1,1]], [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
        ],
    ]

    print("Split Tests")
    for test in splitTestVector:
        n1 = Number(test[0], None)    
        n2 = Number(test[1], None)    
        n1.split()
        assert n1.__repr__() == n2.__repr__()

    addTestVector = [
       [
           [[1,1],[2,2],[3,3],[4,4]],    
           [[[[1,1],[2,2]],[3,3]],[4,4]],
           False
       ],
        [
           [[1,1],[2,2],[3,3],[4,4],[5,5]],
            [[[[3,0],[5,3]],[4,4]],[5,5]],
            False
       ],
       [
           [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]],   
         [[[[5,0],[7,4]],[5,5]],[6,6]],
         False
       ],
       [ 
           [ 
                [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]], 
                [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
           ],
           [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
           True
       ]
   ]

    print("Test Add")
    for i, test in enumerate(addTestVector):
        Number.debug = test[2]
        sum_setpoint = Number(test[1], None)
        summanden = test[0]
        sum = Number(summanden[0], None)
        for summand in summanden[1:]:
            sum = sum.add(Number(summand, None))
        criteria = sum.__repr__() == sum_setpoint.__repr__()
        print("test", i, criteria)
        if not criteria:
            print("sum setpoint:", sum_setpoint)
            print("sum         :", sum)
        #assert sum.__repr__() == sum_setpoint.__repr__()
        






# puzzle = read_puzzle('Tag_18_Bsp.txt')

# solve(puzzle)
test()

t1 = Number([[[[6,7],[6,7]],[[0,7],[8,9]]],[[[[6,6],0],[6,16]],[[0,8],[8,0]]]], None)
sollwert = Number([[[[6,7],[6,7]],[[0,7],[8,15]]],[[[0,6],[6,16]],[[0,8],[8,0]]]], None)
#wrong result:    [[[[6,7],[6,7]],[[0,7],[8,9]]],[[[0,6],[6,16]],[[0,8],[8,0]]]]
Number.debug = False
t1.reduce()
print(t1)




    
    
    
    

