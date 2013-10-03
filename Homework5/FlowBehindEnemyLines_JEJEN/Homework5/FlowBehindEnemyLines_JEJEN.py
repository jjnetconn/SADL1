# Author
#Jesper - jejen

import sys
import time
import os
import math
import re
from operator import itemgetter


#Data fields
nodes = {}
arch = []
#Place holder - Timers



def importData(inFile):
    
    regExPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    nodes = {}
    
    with open(inFile, 'r') as f:
        
        nNodes = int(f.readline().strip())
        
        for n in range(nNodes):
            nodes[n] = f.readline().strip()
        
        nArch = int(f.readline().strip())
        
        arch = [[0 for i in range(nNodes)] for j in range(nNodes)]
        
        for n in range(nArch):
            railTrack = re.findall(regExPattern,f.readline().strip())
            if (int(railTrack[2]) == -1):
                arch[int(railTrack[0])][int(railTrack[1])] = sys.maxint
                arch[int(railTrack[1])][int(railTrack[0])] = sys.maxint
            else:
                arch[int(railTrack[0])][int(railTrack[1])] = int(railTrack[2])
                arch[int(railTrack[1])][int(railTrack[0])] = int(railTrack[2])
        return[nodes, arch]
        
print importData('rail.txt')