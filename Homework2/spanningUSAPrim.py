#SpanningUSA
#Prims algorithm using heap que
#author: Jesper

from collections import defaultdict
from heapq import *
import sys
import time
import re

#Datafields
nodes = []
edges = []
minimalSpanTree = []
totalDistance = 0

# Timers
totalTimeS = 0
totalTimeE = 0
importTimeS = 0
importTimeE = 0
mstTimeS = 0
mstTimeE = 0

# Read parameters
totalTimeS = time.time()

if (len(sys.argv) < 2):
   print "USAGE:	spanningUSAPrim.py <inputfile>"
   print ""
   print "	PARAMETERS"
   print "	<inputfile>	Filename of inputfile"
   exit()


def loadFile (inputFilename):
    inputfile = open(inputFilename, 'r')
    #tmpCities = []
    for line in inputfile:
        if (line.find("--") == -1):
            nodes.append(line.strip("\n").strip())
        else:        
            nextEdge = re.split('--|\[', line, flags=re.IGNORECASE)  
            # structure: (city1,city2,distance)      
            edges.append((int(nextEdge[2].strip("]\n")),nextEdge[0].strip(),nextEdge[1].strip()))


#Theory in use
#s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
#d = defaultdict(list)
#for k, v in s:
    #d[k].append(v)

#d.items()
#[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]


def prim( nodes, edges):
	global totalDistance
	nConn = defaultdict ( list )
	for node1,node2,distance in edges:
		nConn[node1].append((node1, node2, distance))
		nConn[node2].append((node2, node1, distance))

	minSpanTree = []
	nUsed = set( nodes[0] )

	#Defineing edges for curent node
	validEdges = nConn[ nodes[0] ][:]

	#Transform "validEdges" to a priority que using heapify()
	heapify(validEdges)

	while validEdges:
		node1, distance, node2 = heappop( validEdges )
		
		#Debug print
		#print str(node1) + " " + str(node2) + " " + str(distance)
		
		if node2 not in nUsed:
			nUsed.add( node2 )
			minSpanTree.append( (node1, node2, distance) )
			
			#"Double" check if city is mapped
			for element in nConn[node2]:
				if element[1] not in nUsed:
					heappush( validEdges, element )

			totalDistance += int(distance)
	
	return minSpanTree

importTimeS = time.time()
loadFile(sys.argv[1])
importTimeE = time.time()

mstTimeS = time.time()
#Running Prins minimal spanning tree
minimalSpanTree = prim( nodes, edges )
mstTimeE = time.time()

totalTimeE = time.time()

#Debug print result
#print minimalSpanTree

#Print mst to file
f1=open(sys.argv[1].split('.')[0] + "_Jesper.out", 'w+')
for item in minimalSpanTree:
   print>>f1, item

print "--------------- RESULTS: -----------------"
print "Total distance: " + str(totalDistance) + " Miles\n\n"
print "Import runtime: " + str((importTimeE-importTimeS)) + " sec.\n"
print "Prim runtime: " + str((mstTimeE-mstTimeS)) + " sec.\n"
print "Total runtime: " + str((totalTimeE-totalTimeS)) + " sec.\n"