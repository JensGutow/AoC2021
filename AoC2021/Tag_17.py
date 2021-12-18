#target area: x=20..30, y=-10..-5
#target area: x=155..215, y=-132..-72

X_MIN = 155
X_MAX = 215
Y_MIN = -132
Y_MAX = -72

# X_MIN = 20
# X_MAX = 30
# Y_MIN = -10
# Y_MAX = -5

x = None
y = None
x_high = None
y_high = None
high_max = -10000
menge = []
n = 0
for x_ in range(1,X_MAX+1):
    for y_ in range(-1000,5000):
        if x_==30 and y_==-6:
            x_ = 30
        x,y = 0,0
        dx = x_
        dy = y_
        high_max_local = -10000
        while True:
            if y > high_max_local: high_max_local = y
            if y < Y_MIN or x > X_MAX: 
                break
            if y <= Y_MAX and x >= X_MIN:
                menge.append((x_,y_))
                n += 1
                #print(n, x_, y_)
                if  high_max_local > high_max: 
                    high_max = high_max_local
                    x_high = x_
                    y_high = y_
                break
            elif dx == 0 and x < X_MIN:
                break
            y += dy
            x += dx
            if dx < 0: dx += 1
            if dx > 0: dx += -1
            dy -= 1
            #print(x,y)
            
print("part1:",  x_high, y_high, high_max)
print("part2:", len(menge))
