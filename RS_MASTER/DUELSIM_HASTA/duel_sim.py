import random
import math

#number of times simulation is run
simcount = 1000000

#YOUR STATS
attack = 99
strength = 99
defense = 99
hp = 99
strengthbonus = 86
slashbonus = 90
slashdefensebonus = 13



#OPPONENT STATS
oattack = 99
ostrength = 99
odefense = 99
ohp = 99
ostrengthbonus = 86
oslashbonus = 90
oslashdefensebonus = 0


#CAULCULATED VALUES
maxattackroll = (8 + 3 +attack)+(slashbonus+64)
maxdefenseroll = (8 + 3 + defense)+(slashdefensebonus+64)

omaxattackroll = (8 + 3 + oattack)+(oslashbonus+64)
omaxdefenseroll = (8 + 3 + odefense)+(oslashdefensebonus+64)

accuracy = (1-(omaxdefenseroll+2)/(2*(maxattackroll+1)))
oaccuracy = (1-(maxdefenseroll+2)/(2*(omaxattackroll+1)))

maxhit = math.floor((.5+(strength+8)*(strengthbonus+64)/640))
omaxhit = math.floor((.5+(ostrength+8)*(ostrengthbonus+64)/640))


avg_hit = (maxhit/2)*accuracy
oavg_hit = (omaxhit/2)*oaccuracy


#SIMULATION VALUES
totaldmg = 0
ototaldmg = 0
wincount = 0

dead = False
odead = False

for i in range(simcount):
    totaldmg = 0
    ototaldmg = 0

    dead = False
    odead = False

    #flip for first hit
    t = .75
    if t < .5:
        #we hit first
        while (not dead and not odead):
            #our hit
            dmg = random.randint(0,maxhit)
            r = random.random()
            if r < accuracy:
                totaldmg += dmg
                if totaldmg > ohp:
                    odead = True

            #if opponent didn't die they get a hit
            if not odead:
                odmg = random.randint(0,omaxhit)
                r = random.random()
                if r < oaccuracy:
                    ototaldmg += odmg
                    if ototaldmg > hp:
                        dead = True
        #opponent dead = win
        if odead:
            wincount += 1


    else:
        while (not dead and not odead):

            odmg = random.randint(0,omaxhit)

            r = random.random()
            if r < oaccuracy:
                ototaldmg += odmg
                if ototaldmg > hp:
                    dead = True

            if not dead:
                dmg = random.randint(0,maxhit)
                r = random.random()
                if r < accuracy:
                    totaldmg += dmg
                    if totaldmg > ohp:
                        odead = True

        if odead:
            wincount += 1


print(str(simcount) + " iterations complete.")
print("WIN %: " + str((wincount/simcount)*100))

y = 100
wr = (wincount/simcount)
ny = 100*1000
ly = ny * .75
uy = ny * 1.5

for i in range(int(ly),int(uy)):
    x = i/1000

    v = (x+y)*wr
    if abs(x-v) < .001:
        print("Fair x: " + str(((x+y)*wr)/y))
        break
        #print(str(i/1000) + ": " + str((x+y)*.52) + "   x=  " + str(((x+y)*.52)/y) + "y")

#x = input()
