'''
Created on 27.09.2013

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

# Usage
def printUsage():
    print "USAGE:\tFlowBehindEnemyLines.py <inputfile> <outputfile>"
    print ""
    print "PARAMETERS"
    print "<inputfile>\tFilename of inputfile"
    print "<outputfile>\tFilename of outputfile"
    
# Parsing Input
def parseInputfile(filename):
    numberPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    inputfile = open(filename, 'r')
    
    numOfNodes = int(inputfile.readline().strip())
    nodes = {}
    for n in range(numOfNodes):
        nodes[n] = inputfile.readline().strip()
    
    numOfArcs = int(inputfile.readline().strip())
    arcs = {}
    for n in range(numOfArcs):
        railway = re.findall(numberPattern,inputfile.readline().strip())  
        if (railway[0] in arcs.keys()):
            dest = arcs[railway[0]]
            dest[railway[1]] = railway[2]
        else:
            arcs[railway[0]] = {railway[1]:railway[2]}
            
    return [nodes,arcs]

# ToDo
def algorithm():
    return 0


#Programm
if ((len(sys.argv) != 2)):
    printUsage()
    exit()
else:
    inputfile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    input = parseInputfile(inputfile)
    print input[0]
    print input[1]