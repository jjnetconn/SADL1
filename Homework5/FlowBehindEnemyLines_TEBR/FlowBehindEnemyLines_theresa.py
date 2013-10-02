'''
Created on 27.09.2013

@author: Theresa
'''

import sys
import re
import time
import os

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
            arcs[int(railway[1])][int(railway[0])] = sys.maxint
        else:
            arcs[int(railway[0])][int(railway[1])] = int(railway[2])
            arcs[int(railway[1])][int(railway[0])] = int(railway[2])
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

#Calculates the MaxFlow and MinCut
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
    minCut = getMinCut(G,s,residualG)
    return [maxFlow,minCut]

#Find all reachable vertices from s and mark these as true
def DepthFirstSearch(G,s,visited):
    visited[s] = 1
    for i in range(len(G)):
        if (G[s][i]!=0 and visited[i]==0):
            DepthFirstSearch(G, i, visited);
 
#Calculates the MinCut:
# Detect all reachable and non-reachable nodes in the residual graph from s
# All edges in the original graph that are from a reachable node to non-reachable node in the residual graph
def getMinCut(G,s,residualG):
    visited = {}
    for node in range(len(G)):
        visited[node] = 0
    DepthFirstSearch(residualG, s, visited)
    result = []
    for i in range(len(G)):
        for j in range(len(G)):
            if ((visited[i]==1) and (visited[j]==0) and (G[i][j]!=0)):
                result.append([str(i),str(j)])
    return result

#Program
totalTimeS = time.time()
if ((len(sys.argv) != 2)):
    printUsage()
    exit()
else:
    importTimeS = time.time()
    inputfile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    input = parseInputfile(inputfile)
    nodes = input[0]
    edges = input[1]
    importTimeE = time.time()
    #print "NODES:" + str(nodes)
    #print "EDGES:"
    #printMatrix(edges)
    algorithmTimeS = time.time()
    result = FordFulkerson(input[1],0,len(input[0])-1)
    algorithmTimeE = time.time()
    print "MaxFlow: " + str(result[0])
    print "MinCut: "
    minCut = result[1]
    for i in range(len(minCut)):
        print str(nodes[int(minCut[i][0])]) + " - " + str(nodes[int(minCut[i][1])])

totalTimeE = time.time()
print "\n--------------------------------------------------\nTimers:" 
print " - Total runtime: " + str(totalTimeE - totalTimeS) + " secs.\n"
print " - Import data runtime: " + str(importTimeE - importTimeS)  + " secs.\n"
print " - Algorithm runtime: " + str(algorithmTimeE - algorithmTimeS) + " secs.\n"
print "--------------------------------------------------"