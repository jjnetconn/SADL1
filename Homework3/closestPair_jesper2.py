#Closest paris - Devide & Conquer

import sys
import time
import math
import os

#Data types
fileList = []
P = []
dist = float(0.00)

def distance(pX,pY):
  return math.sqrt(math.fabs(pX[0]-pY[0])**2 + math.fabs(pX[1]-pY[1])**2)

def test_input_file(inputf_name,input_dist):
  global P
  P=[]
  inputf = open(inputf_name, 'r')
  for line in inputf:
    line = " ".join(line.split())
    if(not(line.split(' ')[0].isupper()) and not(line == "") and len(line.split(' ')) == 3):
      #print "About to split this line...: " + line
      P.append((float(line.split(' ')[1]),float(line.split(' ')[2].rstrip("\n")),line.split(' ')[0]))

  calc_dist = round(float(dist),2)
  correct_dist = round(float(input_dist),2)
  correct = 'ERROR'
  if(calc_dist == correct_dist): correct = 'OK'
  print "Testing input file: " + inputf_name + " - found: " + str(calc_dist) + " correct: " + str(correct_dist) + " -> " + correct


def closestpair(L):
  def square(x): return x*x
  def sqdist(p,q): 
    global dist
    dist = float(0.00)
    dist = square(p[0]-q[0])+square(p[1]-q[1])
    return dist
  
  best = [sqdist(L[0],L[1]), (L[0],L[1])]
  
  # check whether pair (p,q) forms a closer pair than one seen already
  def testpair(p,q):
    d = sqdist(p,q)
    if d < best[0]:
      best[0] = d
      best[1] = p,q
      
  # merge two sorted lists by y-coordinate
  def merge(A,B):
    i = 0
    j = 0
    while i < len(A) or j < len(B):
      if j >= len(B) or (i < len(A) and A[i][1] <= B[j][1]):
        yield A[i]
        i += 1
      else:
        yield B[j]
        j += 1

  # Find closest pair recursively; returns all points sorted by y coordinate
  def recur(L):
    if len(L) < 2:
      return L
    split = len(L)/2
    splitx = L[split][0]
    L = list(merge(recur(L[:split]), recur(L[split:])))

    # Find possible closest pair across split line
    # Note: this is not quite the same as the algorithm described in class, because
    # we use the global minimum distance found so far (best[0]), instead of
    # the best distance found within the recursive calls made by this call to recur().
    # This change reduces the size of E, speeding up the algorithm a little.
    #
    E = [p for p in L if abs(p[0]-splitx) < best[0]]
    for i in range(len(E)):
      for j in range(1,8):
        if i+j < len(E):
          testpair(E[i],E[i+j])
    return L
  
  L.sort()
  recur(L)
  return best[1]

#Runtime
inputfile_name = sys.argv[1]
inputfile = open(inputfile_name, 'r')
for line in inputfile:
  filename = line.split(' ')[0].rstrip(':')
  dist = line.split(' ')[2].rstrip('\n')
  test_input_file(filename,dist)
  #win = closestpair(P)
#print win
#print distance(win[0],win[1])
