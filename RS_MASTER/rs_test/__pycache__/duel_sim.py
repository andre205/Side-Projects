from urlparse import urlparse
import random
import math

acct_name = "chowderhead"
s = urlparse('http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + acct_name)



simcount = 10000

#OUR STATS
attack = 99
strength = 99
defense = 99
hp = 99
strengthbonus = 86
slashbonus = 90
slashdefensebonus = 0

maxattackroll = (8 + 3 + attack)+(slashbonus+64)
defenseroll = (8 + 3 + defense)+(slashdefensebonus+64)



#OPPONENT STATS
oattack = 99
ostrength = 99
odefense = 99
ohp = 99
ostrengthbonus = 86
oslashbonus = 90
oslashdefensebonus = 0

omaxattackroll = (8 + 3 + oattack)+(oslashbonus+64)
odefenseroll = (8 + 3 + odefense)+(oslashdefensebonus+64)

#ACC
accuracy = (1-(omaxdefenseroll+2)/(2*(maxattackroll+1)))
oaccuracy = (1-(maxdefenseroll+2)/(2*(omaxattackroll+1)))

#MAXHIT
maxhit = math.floor((.5+(strength+8)*(strengthbonus+64)/640))
omaxhit = math.floor((.5+(ostrength+8)*(ostrengthbonus+64)/640))

#DUEL len
duellen = (ohp/(maxhit/2*accuracy))
oduellen = (hp/(omaxhit/2*oaccuracy))


print("accuracy " + accuracy)
print("maxhit " + maxhit )
print("duellen " + duellen)

for i in range(simcount):



    random.randint(1,101)
