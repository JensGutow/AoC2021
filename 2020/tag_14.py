import time

class program():
    def __init__(self):
        self.rom = {} # addr -> value 
        self.mask_1 = 0
        self.mask_0 = 0
        self.mask_x = 0

    def translate_mask(self, mask, c):
        return int("".join(["1" if s==c else "0" for s in mask]),2)
    
    def get_sum(self):
        sum = 0
        for s in self.rom.values():
            sum += s
        return sum

    def set_mask(self, mask):
        self.mask_1 = self.translate_mask(mask, "1")
        self.mask_0 = self.translate_mask(mask, "0")
        self.mask_x = self.translate_mask(mask, "X")

class program1(program):
    def __init__(self):
        super().__init__() 

    def set_rom(self, adr, new_value):
        value = new_value & self.mask_x
        value |= self.mask_1
        value &= (~self.mask_0)
        self.rom[adr] =  value

class program2(program):
    def __init__(self):
        super().__init__() 

    def set_rom(self, adr, value):
        adr_n = self.mask_1 | (self.mask_0 & adr)
        adr_set = set()
        adr_set.add(adr_n)
        for i in range(36):
            if self.mask_x & (1<<i):
                set_temp = set()
                for item in adr_set:
                    set_temp.add(item | (1<<i))
                adr_set = adr_set.union(set_temp)
        for adr in adr_set:
            self.rom[adr] = value

class puzzle():
    def __init__(self,file_name):
        self.prog1 = program1()
        self.prog2 = program2()
        with open(file_name) as f:
            for zeile in f:
                if zeile.startswith("mask"):
                    mask = zeile.split()[2]
                    self.prog1.set_mask(mask)
                    self.prog2.set_mask(mask)
                if zeile.startswith("mem"):
                    adr, value = zeile[4:].replace("[","").replace("]","").replace(" ","").strip().split("=")
                    self.prog1.set_rom(int(adr), int(value))
                    self.prog2.set_rom(int(adr), int(value))

    def löse1(self):
        return self.prog1.get_sum()

    def löse2(self):
        return self.prog2.get_sum()
                
print("Einlesen/Objekterzeugung/Speicher aufbauen")
start =time.perf_counter()
p = puzzle("tag_14.txt")
print(time.perf_counter() - start)

print("Task 1")
start =time.perf_counter()
print(p.löse1())
print(time.perf_counter() - start)

print("Task 2")
start =time.perf_counter()
print(p.löse2())
print(time.perf_counter() - start)