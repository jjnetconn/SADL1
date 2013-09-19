#Closest paris - Devide & Conquer

import sys
import time
import math
import os

#Helpers 
infinity = float('inf')

#Data types
fileList = []
P = []


def loadDataDir(datadir):
  global fileList
  os.chdir(datadir)
  for files in os.listdir("."):
      if files.endswith(".tsp"):
          fileList.append(files)

def loadInputData(inputfile):
  global P

  for line in inputfile:
    
    _tmp1 = line.replace("   ", " ")
    _tmp2 = _tmp1.replace("  ", " ")
    if(_tmp2 is "EOF\n" or "EOF " or "EOF"):
      print "EOF"
    elif(not(_tmp2.split(' ')[0].isupper() or _tmp2.split(' ')[1].isupper())):
      tmpArr = _tmp2.split(' ')
      if(len(tmpArr) < 3):
        P.append((float(tmpArr[2]),float(tmpArr[3].rstrip("\n")),tmpArr[1]))
      else:
        P.append((float(tmpArr[1]),float(tmpArr[2].rstrip("\n")),tmpArr[0]))

#Algorithme
def distance(pX,pY):
  return math.sqrt(math.fabs(pX[0]-pY[0])**2 + math.fabs(pX[1]-pY[1])**2)


def closest_pair(p):
  pX = sorted(p, key=lambda x:p[0])
  pY = sorted(p, key=lambda x:p[1])
  return closest_pair_recurse(pX,pY)


def closest_pair_recurse(pX, pY):
  if(len(pX) < 3):
    if(len(pX) < 2): return pX[0],(10000000,10000000,'infinity')
    else: return pX[0],pX[1]
  
  splitter = len(pX)/2
  qx,qy = pX[:splitter],pY[:splitter]
  rx,ry = pX[splitter:],pY[splitter:]

  q0,q1 = closest_pair_rec(qx,qy)
  r0,r1 = closest_pair_rec(rx,ry)
  
  delta = min(distance(q0,q1),distance(r0,r1))
  x_max = qx[len(qx)-1]

  within_delta = lambda p : math.fabs(x_max[0]-p[0]) < delta
  sy = filter(within_delta, pY)

  closest0,closest1 = r0,r1
  if(distance(q0,q1) < distance(r0,r1)):
    closest0,closest1 = q0,q1

  if(len(sy) > 1):
    s_count = 0
    s_min = distance(sy[0],sy[1])
    s0,s1 = sy[0],sy[1]
    for s in sy:
      n_count = 1
      while s_count+n_count < len(sy) and n_count < 16:
        n = sy[s_count+n_count]
        s_next = distance(s,n)
        if(s_next < s_min):
          s_min = s_next
          s0,s1 = s,n
        n_count += 1
      s_count += 1
    if(distance(s0,s1) < distance(closest0,closest1)):
      closest0,closest1 = s0,s1
  
  return closest0,closest1


#Runtime

# Read parameters
if ((len(sys.argv) < 2) or (len(sys.argv) > 4)):
   print "USAGE:  closestPair_Jesper.pY -f <datadir/file> [<testfile>]"
   print ""
   print "  PARAMETERS"
   print "      -f for single file"
   print "      -d for dir"
   print "  <inputfile> Filename of inputfile"
   print "  <testfile>    Filename of expected outputfile"
   exit()


if sys.argv[1] is "f":
    #call load and parse file
    inputfile = open(sys.argv[2], 'r')
    loadInputData(inputfile)

if sys.argv[1] is "d":
    #call load list from datadir and loop through files
    loadDataDir(sys.argv[2])
    for inFile in fileList:
      P=[]
      print "opening file:"
      print inFile
      inputfile = open(inFile, 'r')
      loadInputData(inputfile)
      c0,c1 = closest_pair(P)
      print c0,c1
      print "With distance: " + str(distance(c0,c1))

c0,c1 = closest_pair(P)
print c0,c1
print "With distance: " + str(distance(c0,c1))