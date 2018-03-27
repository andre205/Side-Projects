import random
import math

#number of times simulation is run
simcount = 100000

#YOUR STATS
attack = 99
strength = 99
defense = 99
hp = 99
strengthbonus = 86
slashbonus = 90
slashdefensebonus = 0

strengthbonusd = 40
slashbonusd = 40

#OPPONENT STATS
oattack = 99
ostrength = 99
odefense = 99
ohp = 99
ostrengthbonus = 86
oslashbonus = 90
oslashdefensebonus = 0

ostrengthbonusd = 40
oslashbonusd = 40

#CAULCULATED VALUES
maxattackroll = (8 + 3 + attack)+(slashbonus+64)
maxattackrolld = (8 + attack)+(slashbonusd+64)
maxdefenseroll = (8 + 3 + defense)+(slashdefensebonus+64)
maxdefenserolld = (8 + defense)+(slashdefensebonus+64)

omaxattackroll = (8 + 3 + oattack)+(oslashbonus+64)
omaxattackrolld = (8 + oattack)+(oslashbonusd+64)
omaxdefenseroll = (8 + 3 + odefense)+(oslashdefensebonus+64)
omaxdefenserolld = (8 + odefense)+(oslashdefensebonus+64)

accuracy = (1-(omaxdefenseroll+2)/(2*(maxattackroll+1)))
oaccuracy = (1-(maxdefenseroll+2)/(2*(omaxattackroll+1)))

accuracyd = 1.25*(1-(omaxdefenserolld+2)/(2*(maxattackrolld+1)))
oaccuracyd = 1.25*(1-(maxdefenserolld+2)/(2*(omaxattackrolld+1)))

maxhit = math.floor((.5+(strength+8)*(strengthbonus+64)/640))
omaxhit = math.floor((.5+(ostrength+8)*(ostrengthbonus+64)/640))

maxhitd = math.floor((.5+(strength+8+3)*(strengthbonusd+64)/640))
omaxhitd = math.floor((.5+(ostrength+8+3)*(ostrengthbonusd+64)/640))

avg_hit = (maxhit/2)*accuracy
oavg_hit = (omaxhit/2)*oaccuracy


#SIMULATION VALUES
totaldmg = 0
ototaldmg = 0
wincount = 0

doublehits = 4
odoublehits = 4

dead = False
odead = False

dagtotal = 0
whiptotal = 0

print(str(accuracyd))

# #print(str(accuracyd))
# #print(str(oaccuracyd))

for i in range(simcount):
    totaldmg = 0
    ototaldmg = 0

    doublehits = 4
    odoublehits = 4

    dead = False
    odead = False

    #flip for first hit
    t = .25
    if t < .5:
        #we hit first
        while (not dead and not odead):
            #our hit
            #use dagger hits first
            if doublehits > 0:
                dmg =  math.floor(1.15*random.randint(0,maxhitd))
                r = random.random()
                if r < accuracyd:
                    totaldmg += dmg
                    dagtotal += dmg
                    #print("we dagger " + str(dmg))
                    # if totaldmg > ohp:
                    #     odead = True
                #else:
                    #print("we miss")

                dmg =math.floor(1.15* random.randint(0,maxhitd))

                r = random.random()
                if r < accuracyd:
                    totaldmg += dmg
                    dagtotal += dmg
                    #print("we dagger " +str(dmg))
                    if totaldmg > ohp:
                        odead = True
                #else:
                    #print("we miss")

                doublehits -= 1
            #whip hits
            else:
                dmg = random.randint(0,maxhit)
                r = random.random()
                if r < accuracy:
                    totaldmg += dmg
                    whiptotal += dmg
                    #print("we whip " + str(dmg))
                    if totaldmg > ohp:
                        odead = True
                #else:
                    #print("we miss")


            #if opponent didn't die they get a hit
            if not odead:
                if odoublehits > 0:
                    odmg = math.floor(1.15*random.randint(0,omaxhitd))

                    r = random.random()
                    if r < oaccuracyd:
                        ototaldmg += odmg
                        #print("they dagger " + str(odmg))
                        # if ototaldmg > hp:
                        #     dead = True
                    #else:
                        #print("they miss")

                    odmg = math.floor(1.15*random.randint(0,omaxhitd))

                    r = random.random()
                    if r < oaccuracyd:
                        ototaldmg += odmg
                        #print("they dagger " + str(odmg))
                        if ototaldmg > hp:
                            dead = True
                    #else:
                        #print("they miss")

                    odoublehits -= 1
                else:
                    odmg = random.randint(0,omaxhit)
                    r = random.random()
                    if r < oaccuracy:
                        ototaldmg += odmg
                        #print("they whip "  + str(odmg))
                        if ototaldmg > hp:
                            dead = True
                    #else:
                        #print("they miss")

        #opponent dead = win
        if odead:
            wincount += 1


    else:
        while (not dead and not odead):
            if odoublehits > 0:
                odmg = math.floor(1.15*random.randint(0,omaxhitd))


                r = random.random()
                if r < oaccuracyd:
                    ototaldmg += odmg
                    # if ototaldmg > hp:
                    #     dead = True

                odmg = math.floor(1.15*random.randint(0,omaxhitd))

                r = random.random()
                if r < oaccuracyd:
                    ototaldmg += odmg
                    if ototaldmg > hp:
                        dead = True

                odoublehits -= 1
            else:
                odmg = random.randint(0,omaxhit)
                r = random.random()
                if r < oaccuracy:
                    ototaldmg += odmg
                    if ototaldmg > hp:
                        dead = True

            if not dead:
                if doublehits > 0:
                    dmg = math.floor(1.15*random.randint(0,maxhitd))

                    r = random.random()
                    if r < accuracyd:
                        totaldmg += dmg
                        # if totaldmg > ohp:
                        #     odead = True

                    dmg = math.floor(1.15*random.randint(0,maxhitd))

                    r = random.random()
                    if r < accuracyd:
                        totaldmg += dmg
                        if totaldmg > ohp:
                            odead = True

                    doublehits -= 1
                else:
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

print("dag total " + str(dagtotal))
print("whip total " + str(whiptotal))

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
