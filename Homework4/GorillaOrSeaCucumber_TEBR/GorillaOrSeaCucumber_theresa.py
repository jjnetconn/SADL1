'''
Created on 23.09.2013

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
    print "USAGE:\tGorillaOrSeaCucumber.py <inputfile> <scoreMatrixfile> <outputfile>"
    print ""
    print "PARAMETERS"
    print "<inputfile>\tFilename of inputfile"
    print "<scoreMatrixfile>\tFilename of scoreMatrixfile"
    print "<outputfile>\tFilename of outputfile"

def parseScoreMatrix(filename):
    scoreMatrixFile = open(filename, 'r')
    proteinLinePattern = '^[\ ]([\ ]{2}[A-Z\*])*$'
    scoreLinePattern = '^[A-Z\*]+([\ ]{1,2}[\-]?[0-9])*'
    singleProteinPattern = '([A-Z\*])'
    numberPattern = '[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    proteins = None
    scoreMatrix = {}
    for line in scoreMatrixFile:
        #print line
        if (re.search(proteinLinePattern,line) != None):
            proteins = re.findall(singleProteinPattern,line)
            #print "Proteins: " + str(proteins)
        if (re.search(scoreLinePattern,line) != None):
            if (proteins == None):
                print "ERROR: Proteins not known"
                exit()
            else:                
                protein = re.findall(singleProteinPattern,line)
                #print "Protein: " + str(protein[0])
                scores = re.findall(numberPattern,line)
                #print "Scores: " + str(scores)
                if (len(scores) != len(proteins)):
                    print "ERROR: Matrix is corrupt"
                proteinScores = {}
                for num in range(0,len(scores)):
                    proteinScores[proteins[num]] = int(scores[num])
                #print "ProteinScores: " + str(proteinScores)
                scoreMatrix[protein[0]] = proteinScores
            #print "ScoreMatrix: " + str(scoreMatrix)
    return scoreMatrix

def parseInputFile(filename):
    inputFile = open(filename, 'r')
    proteinStructures = {}
    creaturePattern = '[^\>][\w\-]*'
    for line in inputFile:
        if (line.startswith(">")):
            creature = re.findall(creaturePattern,line)[0]
            #print "Creature: " +  str(creature)
            proteinStructures[creature] = ""
        else:
            proteins = re.findall("([A-Z]*)",line.strip())
            #print "Proteins: " + str(proteins)
            proteinStructures[creature] += str(proteins[0])
    return proteinStructures

def Alignment(X,Y):
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        A = [[0 for i in range(len(X)+1)] for j in range(len(Y)+1)]
        for i in range(len(X)+1):
            A[0][i] = scoreMatrix[X[i-1].upper()]["*"]*i
        for j in range(len(Y)+1):
            A[j][0] = scoreMatrix[Y[j-1].upper()]["*"]*j
        print A
    # Minimum alignment cost
        for j in range(1,len(Y)+1):
            for i in range(1,len(X)+1):
                A[j][i] = max(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]+A[j-1][i-1],
                            scoreMatrix[X[i-1].upper()]["*"]+A[j-1][i],
                            scoreMatrix["*"][Y[j-1].upper()]+A[j][i-1])
    else:
        return 0
    return A[len(Y)][len(X)]

def SpaceEfficientAlignment(X,Y):
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        B = [[0 for i in range(len(X)+1)] for j in range(2)]
        for i in range(len(X)+1):
            B[0][i] = scoreMatrix[X[i-1].upper()]["*"]*i
    # Minimum alignment cost
        for j in range(1,len(Y)+1):
            B[1][0] = scoreMatrix[Y[j-1].upper()]["*"]*j
            #print B
            for i in range(1,len(X)+1):
                B[1][i] = max(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]+B[0][i-1],
                            scoreMatrix[X[i-1].upper()]["*"]+B[1][i-1],
                            scoreMatrix["*"][Y[j-1].upper()]+B[0][i])
            for i in range(0,len(X)+1):
                B[0][i] = B[1][i]
    else:
        return 0
    return B[0][len(X)]


def BackwardAlignment(X,Y):
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        A = [[0 for i in range(len(X)+1)] for j in range(len(Y)+1)]
        for i in range(len(X),-1,-1):
            A[len(Y)][len(X)-i] = scoreMatrix[X[len(X)-i-1].upper()]["*"]*i
        for j in range(len(Y),-1,-1):
            A[len(Y)-j][len(X)] = scoreMatrix[Y[len(Y)-j-1].upper()]["*"]*j
    # Minimum alignment cost
        for j in range(len(Y)-1,-1,-1):
            for i in range(len(X)-1,-1,-1):
                A[j][i] = max(scoreMatrix[X[i].upper()][Y[j].upper()]+A[j+1][i+1],
                            scoreMatrix[X[i].upper()]["*"]+A[j+1][i],
                            scoreMatrix["*"][Y[j].upper()]+A[j][i+1])
    else:
        return 0
    return A[0][0]

# Not working
def BackwardSpaceEfficientAlignment(X,Y):
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        B = [[0 for i in range(len(X)+1)] for j in range(2)]
        for i in range(len(X),-1,-1):
            B[0][len(X)-i] = scoreMatrix[X[len(X)-i-1].upper()]["*"]*i
        print B
    # Minimum alignment cost
        for j in range(len(Y)-1,-1,-1):
            B[1][len(X)] = scoreMatrix[Y[j].upper()]["*"]*(j)
            print "B: " + str(B)
            for i in range(len(X)-1,-1,-1):
                #print "i: " + str(i)
                #print B
                B[1][i] = max(scoreMatrix[X[i].upper()][Y[j].upper()]+B[0][i+1],
                            scoreMatrix[X[i].upper()]["*"]+B[1][i+1],
                            scoreMatrix["*"][Y[j].upper()]+B[0][i])
                #print B
            for i in range(len(X),-1,-1):
                B[0][i] = B[1][i]
    else:
        return 0
    return B[1][1]

#Not finished
#def DivideAndConquerAlignment(X,Y):
#    # To-Do
#    if (len(X) <= 2 or len(Y) <= 2):
#        return Alignment(X,Y)
#    SpaceEfficientAlignment(X,Y[1:len(Y)/2])
#    return 0

if ((len(sys.argv) != 4)):
    printUsage()
    exit()
else:
    scoreMatrixFile = [os.path.join(os.path.dirname(__file__), sys.argv[2])][0]
    scoreMatrix = parseScoreMatrix(scoreMatrixFile)
    print scoreMatrix
    
    inputFile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    proteinStructures = parseInputFile(inputFile)
    print proteinStructures
    
    # Output
    '''
    results = {}
    creatures = proteinStructures.keys()
    for c1 in range(len(creatures)):
        for c2 in range(len(creatures)):
        #print proteinStructures[creatures[c]]
        #print proteinStructures[creatures[c+1]]
            if (c1 != c2):
                if ((str(creatures[c1]) + "--" + str(creatures[c2])) not in results and (str(creatures[c2]) + "--" + str(creatures[c1])) not in results):
                    result = SpaceEfficientAlignment(proteinStructures[creatures[c1]],proteinStructures[creatures[c2]])
                    results[str(creatures[c2]) + "--" + str(creatures[c1])] = str(result)
                    results[str(creatures[c1]) + "--" + str(creatures[c2])] = str(result)                   
    
    # Compare results
    filename = [os.path.join(os.path.dirname(__file__), sys.argv[3])][0]
    for result in results:
        line = result + ": " + results[result]
        if line[:-4] in open(filename).read():
            if line in open(filename).read():
                print line + "\t\t--> OK"
            else:
                print line + "\t\t--> ERROR"
    
    '''
    print BackwardSpaceEfficientAlignment("KQRK","KAK")
    print SpaceEfficientAlignment("KQRK","KAK")
    print BackwardSpaceEfficientAlignment("KAK","KQRK")
    print BackwardAlignment("KQRIKAAKABK","KAK")
    print BackwardAlignment("KAK","KQRIKAAKABK")
    print BackwardAlignment("KQRK","KQRIKAAKABK")
    print BackwardAlignment("KQRIKAAKABK","KQRK")
    #'''
    