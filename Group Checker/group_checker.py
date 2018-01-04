#Tyler Andrews Group Checker
import itertools

#Verify that length of each row is equal to number of columns
def check_nxn(G):
  for i in range(len(G)):
    if (len(G[i]) != len(G)):
      return False
  return True

#old version of associativity with multiplication
def is_associative_triple_old(x, y, z):
    if (x*y)*z == x*(y*z):
        return True
    return False

#check (xy)z == x(yz) from group table
def is_associative_triple(G, x, y, z):
  temp1 = G[x][y]
  temp2 = G[y][z]
  if (G[temp1][z] != G[x][temp2]):
    return False
  return True

#Check associativity for each triplet in each row
def is_associative(G):
  for i in range(len(G)):
    xyz = itertools.product(G[i], repeat=3)
    for triple in xyz:
      #print(triple)
      #if not is_associative_triple(*triple):
      #  return False
      if not is_associative_triple(G, *triple):
          return False
  return True

#early version of checking for duplicate elements
def check_num_elements(G):
  l = len(G)
  for i in range(0,l):
    elements = []
    for j in range(0,l):
      if (G[i][j] not in elements):
        elements.append(G[i][j])
    if (len(elements) != l):
      return "Wrong number of elements"
  return "All good"

#look for row with form [0,1,...,n-1]
#return row index of identity element (which is also the corresponding integer)
def find_identity(G):
  for i in range(len(G)-1):
    if( all(G[i][j] == j for j in range(len(G)-1)) ):
      return i
  return "No identity"

#verify that identity exists in each row and column
def check_inverses(G,i):
  for j in range(len(G)):
    if (i not in G[j]):
      return False
  #create temp array that holds all values of a column
  elem = []
  for j in range(len(G)):
    for k in range(len(G)):
      elem.append(G[k][j])
    if (i not in elem):
      return False
    elem = []
  return True

#Zn for modular addition
def Z(n): return [[(x+y)%n for y in range(n)] for x in range(n)]

#Zn for modular multiplication (omitting 0th row)
def Zm(n): return [[(x*y)%n for y in range(1,n)] for x in range(1,n)]

#symmetric difference?   unused
def P(n): return [[x for y in range(2**n)] for x in range(2**n)]

def print_table(G):
  if(check_nxn(G)):
    #top row has form:   function | 0 1 2 ... n-1
    print("+ | ",end='')
    for i in range(len(G)):
      print(i,end=' ')
    print()

    for i in range(len(G)*2+3):
      print('-',end='')
    print()

    #rows have form, n | values ...
    for i in range(len(G)):
      print(i, end='')
      print(" | ",end='')
      for j in range(len(G)):
          print(G[i][j],end=' ')
      print()

  else:
    print("Table is not nxn")
    return False

#table starting at 1 with modular multiplication
def print_table_m(G):
  if(check_nxn(G)):
    #top row has form:   function | 1 2 ... n-1
    print("* | ",end='')
    for i in range(1, len(G)+1):
      print(i,end=' ')
    print()

    for i in range(len(G)*2+3):
      print('-',end='')
    print()

    for i in range(1,len(G)+1):
      print(i, end='')
      print(" | ",end='')
      for j in range(1,len(G)+1):
          print(G[i-1][j-1],end=' ')
      print()

  else:
    print("Table is not nxn")
    return False

#print custom table for group G, with operation op, and identity row id_row
def print_custom_table(G,op,id_row):
  #top row has form:   function | 0 1 2 ... n-1
  print(op,"| ",end='')
  for i in range(len(G)):
    print(G[id_row][i],end=' ')
  print()

  for i in range(len(G)*4+3):
    print('-',end='')
  print()

  #rows have form, n | values ...
  for i in range(len(G)):
    print(G[id_row][i], end='')
    print(" | ",end='')
    for j in range(len(G)):
        print(G[i][j],end=' ')
    print()

#find identity, check inverses, check associativity
def is_group(G):
  e = find_identity(G)
  if e == "No identity":
    print(e)
    return False
  else:
    print("Identity = ", e)
  return check_inverses(G, e) and is_associative(G)

#is sg a subgroup of g
#check if groups, check identities are equal, check g contains sg (compare elements of first row)
def is_subgroup(sg,g):
  if (is_group(sg) and is_group(g)):
    h1 = sg[0]
    g1 = g[0]
    if (find_identity(sg)==find_identity(g)):
      for i in range(len(h1)):
        if (h1[i] not in g1):
          return False
      return True
    else:
      return False

def print_if_group(b):
  if(b):
    print("Is a group")
  else:
    print("Is not a group")

def print_if_subgroup(b):
  if(b):
    print("Is a subgroup")
  else:
    print("Is not a subgroup")

############################

H = [[2,0,1],[0,1,2],[1,2,0]]

K4 = [[0,1,2,3],
      [1,0,3,2],
      [2,3,0,1],
      [3,2,1,0]]

G_3 = [['e','a','b'],
       ['a','b','e'],
       ['b','e','a']]

Pabc = [['null','bc  ','ac  ','ab  ','c   ','b   ','a   ','abc '],
        ['bc  ','null','ab  ','ac  ','b   ','c   ','abc ','a   '],
        ['ac  ','ab  ','null','bc  ','a   ','abc ','c   ','b   '],
        ['ab  ','ac  ','bc  ','null','abc ','a   ','b   ','c   '],
        ['c   ','b   ','a   ','abc ','null','bc  ','ac  ','ab  '],
        ['b   ','c   ','abc ','a   ','bc  ','null','ab  ','ac  '],
        ['a   ','abc ','c   ','b   ','ac  ','ab  ','null','bc  '],
        ['abc ','a   ','b   ','c   ','ab  ','ac  ','bc  ','null']]

############################

print("Group checking")
print("H")
print_if_group(is_group(H))
print()

print("K4")
print_if_group(is_group(K4))
print()

print("Z10")
print_if_group(is_group(Z(10)))
print()

############################

print("Tables")
print("Z10 with addition")
print_table(Z(10))
print()

print("Z10 with multiplication (0th row omitted)")
print_table_m(Zm(10))
print()

print("Pabc")
print_custom_table(Pabc,'o   ',7)
print()

print("Any group with 3 elements")
print_custom_table(G_3,'*',0)
print()

print("K4")
print_custom_table(K4,'*',0)
print()

############################
print("Subgroup checking")
print("Z5 subgroup of Z10?")
print_if_subgroup(is_subgroup(Z(5),Z(10)))
print()
print("H subgroup of K4?")
print_if_subgroup(is_subgroup(H,K4))
