'''
SpanningUSA
Kruskal's algorithm with Union-Find-Datastructure and path compression
Created on 08.09.2013

@author: Theresa
'''

import sys
import re
import time

# Timers
totalTimeS = 0
totalTimeE = 0
importTimeS = 0
importTimeE = 0
kruskalTimeS = 0
kruskalTimeE = 0

# Read parameters
if (len(sys.argv) != 2):
   print "USAGE:\tspanningUSA.py <inputfile>"
   print ""
   print "PARAMETERS"
   print "<inputfile>\tFilename of inputfile"
   exit()

# Read inputfile
def loadFile (inputFilename):
    inputfile = open(inputFilename, 'r')
    cities = []
    for line in inputfile:
        if (line.find("--") == -1):
            cities.append(line.strip("\n").strip())
        else:        
            route = re.split('--|\[', line, flags=re.IGNORECASE)  
            # structure: (distance,city1,city2)      
            routes.append((int(route[2].strip("]\n")),route[0].strip(),route[1].strip()))
    
    # Initialize for Union-Find-Datastructure with path compression
    for city in cities:
        parentNode[city] = city
        treeHeight[city] = 0
    
# Functions for Union-Find-Datastructure with path compression
def find(city):
    if parentNode[city] != city:
        parentNode[city] = find(parentNode[city])
    return parentNode[city]

def union(root1, root2):
    if (root1 != root2):
        if (treeHeight[root1] > treeHeight[root2]):
            parentNode[root2] = root1
        else:
            parentNode[root1] = root2
            # For path compression
            if (treeHeight[root1] == treeHeight[root2]):
                treeHeight[root2] += 1

#Kruskal algorithm   
def kruskal (routes):
    totalDistance = 0;
    routes.sort()
    for route in routes:
        distance, city1, city2 = route
        root1 = find(city1)
        root2 = find(city2)
        if (root1 != root2):
            union(root1, root2)
            totalDistance += distance
    return totalDistance
    
# Start
totalTimeS = time.time()

routes = list()
parentNode = dict()
treeHeight = dict()

importTimeS = time.time()
loadFile(sys.argv[1])
importTimeE = time.time()

kruskalTimeS = time.time()
totalDistance = kruskal(routes)
kruskalTimeE = time.time()

totalTimeE = time.time()

# Output
print "Result: " + str(totalDistance)
print "\n--------------------------------------------------\nTimers:" 
print " - Total runtime: " + str(totalTimeE - totalTimeS) + " secs.\n"
print " - Import data runtime: " + str(importTimeE - importTimeS)  + " secs.\n"
print " - Kruskal runtime: " + str(kruskalTimeE - kruskalTimeS) + " secs.\n"
print "--------------------------------------------------"

    