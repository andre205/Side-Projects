wr = .52

y = 100

ny = y*1000
ly = ny * .5
uy = ny * 2

for i in range(int(ly),int(uy)):
    x = i/1000

    v = (x+y)*wr
    if abs(x-v) < .001:
        print(str(i/1000) + ": " + str((x+y)*.52) + "   x=  " + str(((x+y)*.52)/y) + "y")
