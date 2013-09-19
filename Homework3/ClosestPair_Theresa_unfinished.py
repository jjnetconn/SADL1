'''
Created on 15.09.2013

@author: Theresa
'''

import sys
import re
import time
import os
import math
from operator import itemgetter

# Timers
totalTimeS = 0
totalTimeE = 0
importTimeS = 0
importTimeE = 0
algorithmTimeS = 0
algorithmTimeE = 0

# --- Input
def printUsage():
    print "USAGE:\tClosestPir.py <inputfile> | -out <inputFilename>"
    print ""
    print "PARAMETERS"
    print "<inputfile>\tFilename of inputfile"
    print "<outputfile>\tFilename of inputFilename (result file)"

def readInputfile(inputFilename):
    inputfile = open(inputFilename, 'r')
    numberPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?';
    for line in inputfile:
        match = re.match('(\w+)\s+(' + numberPattern + ')\s+(' + numberPattern + ')', line.strip())
        if (match != None):
            #print '\n' + match.string + '---------------'
            values = re.findall(numberPattern, match.string)
            #print 'Values ' + str(values)
            if ((len(values) >= 2) and (len(values) <= 3)):
                P.append([float(values[len(values)-2]),float(values[len(values)-1]), match.string.split(" ")[0]])
            else:
                print "ERROR: Unexpected input"
    
def getFilesWithResult(inputFilename):
    inputfile = open(inputFilename, 'r')
    numberPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?';
    files = {}
    for line in inputfile:
        match = re.match('([\w./]+:)\s+(' + numberPattern + ')\s+(' + numberPattern + ')', line)
        if (match != None):
            values = re.findall('([\w./]+[^:\s]*)', match.string)
            files[values[0]] = [values[1],values[2]]
    return files



# --- Algorithm

def square(x):
    return x*x
    
def distance(p,q): 
    return math.sqrt(square(p[0]-q[0])+square(p[1]-q[1]))

def calculateClosestPair(P):
    Px = sorted(P, key=itemgetter(0))
    Py = sorted(P, key=itemgetter(1))
    return closestPairRec(Px,Py)
  
def getClosestPair(P):
    if (len(P) == 1):
        closestPair = [(P[0], P[0]),0]
    else:
        shortestPath = distance(P[0],P[1])
        closestPair = [(P[0],P[1]),shortestPath]
        i = 0
        while (i < len(P)-1):
            if (distance(P[i],P[i+1]) < shortestPath):
                shortestPath = distance(P[i],P[i+1])
                closestPair = [(P[i],P[i+1]),shortestPath]   
            i += 1
    return closestPair
    
def closestPairRec(Px,Py):
    if (len(Px) <= 3):
        closestPair = getClosestPair(Px)
        return closestPair
    else:    
        Qx = Px[:len(Px)/2]
        Qy = Py[:len(Py)/2]
        Rx = Px[len(Px)/2:]
        Ry = Py[len(Py)/2:]
        #print "Qx: " + str(Qx)
        #print "Rx: " + str(Rx)
        #print "Qy: " + str(Qy)
        #print "Ry: " + str(Ry)
        closestPairQ = closestPairRec(Qx, Qy)
        closestPairR = closestPairRec(Rx, Ry)
        
        #print "closestPairQ: " + str(closestPairQ)
        #print "closestPairR: " + str(closestPairR)
        
        d = min(closestPairQ[1],closestPairR[1])
        #print "Delta: " + str(d)
        L = Qx[-1]
        #print "Split-Line: " + str(L)
        #print "Py: " + str(Py)
        S = [x for x in Py if (math.fabs(int(L[0])-int(x[0])) < d)]
        #print "S: " + str(S)
        
        '''
        for i in range(len(S)):
            for j in range(1,8):
                if i+j < len(S):
                    tempD = distance(S[i],S[i+j])
                    if (tempD < d):
                        d = tempD
                        closestPairS = [(S[i],S[i+1]),tempD]
                        #print closestPairS[0]
                        return closestPairS[0]
        '''      
                    
        if(len(S) > 1):
            s_count = 0
            s_min = distance(S[0],S[1])
            closestPairS = [(S[0],S[1]),s_min]
            for s in S:
                n_count = 1
                while s_count+n_count < len(S) and n_count < 16:
                    n = S[s_count+n_count]
                    s_next = distance(s,n)
                    if(s_next < s_min):
                        s_min = s_next
                        closestPairS = [(s,n),s_min]
                    n_count += 1
                s_count += 1
            if(closestPairS[1] < d):
                return closestPairS
    
        if (closestPairQ[1] <= closestPairR[1]):
            return closestPairQ
        else:
            return closestPairR
        
    
# Read parameters and input files
if ((len(sys.argv) < 2) or (len(sys.argv) > 3)):
    printUsage()
    exit()
filepaths = []
if (len(sys.argv) == 2):
    filepaths = [os.path.join(os.path.dirname(__file__), sys.argv[1])]
elif ((len(sys.argv) == 3) and (sys.argv[1] == "-out")):
    filepath = os.path.join(os.path.dirname(__file__), sys.argv[2])
    files = getFilesWithResult(filepath)
    for filename in files.keys():
        filepaths.append(os.path.join(os.path.dirname(__file__), filename))
else:
    printUsage()
    exit()
    
for filepath in filepaths:
    print filepath
    P = []
    readInputfile(filepath)  
    #print "P: " + str(P)
    if (len(P) == 0):
        print "NO POINTS"
    else:
        #print "Closest Pair: " + str(calculateClosestPair(P)[0])
        print str(len(P)) + " " + str(calculateClosestPair(P)[1])