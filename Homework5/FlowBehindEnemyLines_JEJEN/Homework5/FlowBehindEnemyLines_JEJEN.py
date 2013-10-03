# Author
#Jesper - jejen

import sys
import time
import re

#Data fields
nodes = {}
edges = []

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


def BFSearch(G,s,t):
    visited = {}
    
    for node in range(len(G)):
        visited[node] = 0
    
    queue = []
    
    queue.append(s)
    visited[s] = 1
    path = {s:-1}
    
    while (len(queue) > 0):
        activeNode = queue.pop()
        
        for node in visited.keys():
            if (visited[node] == 0 and G[activeNode][node]):
                queue.append(node)
                path[node] = activeNode
                visited[node] = 1
                
    if (visited[t] == 1):
        return path 
    else:
        return None

def DFSearch(G,s,visited):
    visited[s] = 1
    for i in range(len(G)):
        if (G[s][i]!=0 and visited[i]==0):
            DFSearch(G, i, visited)

def GetMinCut(G,s,residualG):
    visited = {}
    for node in range(len(G)):
        visited[node] = 0
    DFSearch(residualG, s, visited)
    result = []
    for i in range(len(G)):
        for j in range(len(G)):
            if ((visited[i]==1) and (visited[j]==0) and (G[i][j]!=0)):
                result.append([str(i),str(j)])
    return result

def FordFulkerson(G,s,t):
    
    residualG = [[0 for i in range(len(G))] for j in range(len(G))]
    for row in range(len(G)):
        for column in range(len(G)):
            residualG[row][column] = G[row][column]
    
    path = BFSearch(residualG,s,t)
    maxFlow = 0
    
    while (path != None):
        
        bottleneck = sys.maxint
        node = t
        
        while (node != s):
            activeNode = path[node]
            bottleneck = min(bottleneck,residualG[activeNode][node])
            node = activeNode 
               
        node = t
        while (node != s):
            activeNode = path[node]
            residualG[activeNode][node] -= bottleneck
            residualG[node][activeNode] += bottleneck
            node = activeNode
            
        maxFlow += bottleneck     
        path = BFSearch(residualG,s,t)
    minCut = GetMinCut(G,s,residualG)
    return [maxFlow,minCut]    
 
#Program

totalTimeS = time.time()

dataFile = 'rail.txt'

importTimeS = time.time()
inDataSet = importData(dataFile)
importTimeE = time.time()

nodes = inDataSet[0]
edges = inDataSet[1]

algorithmTimeS = time.time()
result = FordFulkerson(edges,0,len(inDataSet[0])-1)
algorithmTimeE = time.time()
totalTimeE = time.time()

#Print result and timers
print "Running FordFulkerson - NetWorkFlow Algorithm \n"
print "Max Flow: " + str(result[0])
print "Minimal cut's are between nodes:\n"
for i in range(len(result[1])):
    print str(nodes[int(result[1][i][0])]) + " -- " + str(nodes[int(result[1][i][1])])

print "\nProgram Runtime Stats:"
print "Total time : " + str(totalTimeE - totalTimeS)
print "Import time : " + str(importTimeE - importTimeS)
print "Algorithm time : " + str(algorithmTimeE - algorithmTimeS)
