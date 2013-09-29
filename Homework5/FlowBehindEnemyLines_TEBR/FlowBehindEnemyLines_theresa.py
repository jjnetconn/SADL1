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
    
def printMatrix(matrix):
    result = "---"*len(matrix) + "\n"
    for row in matrix:
        result += str(row) + "\n"
    result += "---"*len(matrix)
    print result

# Parsing Input
def parseInputfile(filename):
    numberPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    inputfile = open(filename, 'r')
    
    numOfNodes = int(inputfile.readline().strip())
    nodes = {}
    for n in range(numOfNodes):
        nodes[n] = inputfile.readline().strip()
    
    numOfArcs = int(inputfile.readline().strip())
    arcs = [[0 for i in range(numOfNodes)] for j in range(numOfNodes)]
    for n in range(numOfArcs):
        railway = re.findall(numberPattern,inputfile.readline().strip())  
        if (int(railway[2]) == -1):
            arcs[int(railway[0])][int(railway[1])] = sys.maxint
        else:
            arcs[int(railway[0])][int(railway[1])] = int(railway[2])
    return [nodes,arcs]


# Finding augmenting path in residual graph
def BreadthFirstSearch(G,s,t):
    #Visited nodes
    visited = {}
    for node in range(len(G)):
        visited[node] = 0
    #print visited
    
    #queue
    queue = []
    
    #enqueue source and mark source as visited
    queue.append(s)
    visited[s] = 1
    path = {s:-1}
    
    #BFS loop
    while (len(queue) > 0):
        currentNode = queue.pop()
        #print currentNode
        for node in visited.keys():
            if (visited[node] == 0 and G[currentNode][node]):
                queue.append(node)
                #print "queue: " + str(queue)
                path[node] = currentNode
                visited[node] = 1
                
    if (visited[t] == 1):
        return path 
    else:
        return None

# ToDo
def FordFulkerson(G,s,t):
    #create residual graph
    residualG = [[0 for i in range(len(G))] for j in range(len(G))]
    for row in range(len(G)):
        for column in range(len(G)):
            residualG[row][column] = G[row][column]
    
    path = BreadthFirstSearch(residualG,s,t)
    maxFlow = 0
    
    while (path != None):
        #Find bottleneck in path of residual graph
        bottleneck = sys.maxint
        node = t
        #print "Path: " + str(path)
        while (node != s):
            currentNode = path[node]
            bottleneck = min(bottleneck,residualG[currentNode][node])
            node = currentNode 
        #print "Bottleneck: " + str(bottleneck)
        
        #update residual capacities of the edges and reverse edges along the path
        node = t
        while (node != s):
            currentNode = path[node]
            residualG[currentNode][node] -= bottleneck
            residualG[node][currentNode] += bottleneck
            node = currentNode
            
        #sum the bottlenecks
        maxFlow += bottleneck     
        path = BreadthFirstSearch(residualG,s,t)

    return maxFlow

#Programm
if ((len(sys.argv) != 2)):
    printUsage()
    exit()
else:
    inputfile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    input = parseInputfile(inputfile)
    print "NODES:" + str(input[0])
    print "ARCS:"
    printMatrix(input[1])
    
    print "RESULT: " + str(FordFulkerson(input[1],0,len(input[0])-1))