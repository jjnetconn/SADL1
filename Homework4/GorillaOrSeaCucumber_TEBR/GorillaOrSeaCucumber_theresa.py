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

def printMatrix(matrix,X,Y):
    result = " \t\t"
    for letter in X:
        result += str(letter) + "\t\t"
    result += "\n"
    i = 0
    for row in matrix:
        result += str(Y[i]) + "\t\t"
        for column in row:
            result += str(column) + "\t\t"
        result += "\n"
        i += 1
    print "_____ " + X + "--" + Y + " _____"
    print result

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

def AlignmentCosts(X,Y,printOption):
    if (printOption): print "--------------------------\nALIGNMENT\n--------------------------"
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        A = [[0 for i in range(len(X)+1)] for j in range(len(Y)+1)]
        for i in range(len(X)+1):
            A[0][i] = scoreMatrix[X[i-1].upper()]["*"]*i
        for j in range(len(Y)+1):
            A[j][0] = scoreMatrix[Y[j-1].upper()]["*"]*j
        if (printOption): printMatrix(A,"-"+X,"-"+Y)
    # Minimum alignment cost
        for j in range(1,len(Y)+1):
            for i in range(1,len(X)+1):
                if (printOption): 
                    print "MAX of: "
                    print " -- " + str(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]) + " + " + str(A[j-1][i-1])
                    print " -- " + str(scoreMatrix[X[i-1].upper()]["*"]) + " + " + str(A[j-1][i])
                    print " -- " + str(scoreMatrix["*"][Y[j-1].upper()]) + " + " + str(A[j][i-1])
                A[j][i] = max(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]+A[j-1][i-1],
                            scoreMatrix[X[i-1].upper()]["*"]+A[j-1][i],
                            scoreMatrix["*"][Y[j-1].upper()]+A[j][i-1])
                if (printOption): printMatrix(A,"-"+X,"-"+Y)
    else:
        return 0
    return A[len(Y)][len(X)]

def AlignmentCostsWithStructure(X,Y,printOption):
    if (printOption): print "--------------------------\nALIGNMENT2\n--------------------------"
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        A = [[[0,""] for i in range(len(X)+1)] for j in range(len(Y)+1)]
        for i in range(len(X)+1):
            A[0][i][0] = scoreMatrix[X[i-1].upper()]["*"]*i
            A[0][i][1] = ""
        for j in range(len(Y)+1):
            A[j][0][0] = scoreMatrix[Y[j-1].upper()]["*"]*j
            A[j][0][1] = ""
        if (printOption): printMatrix(A,"-"+X,"-"+Y)
    # Minimum alignment cost
        for j in range(1,len(Y)+1):
            for i in range(1,len(X)+1):
                if (printOption): 
                    print "MAX of: "
                    print " -- " + str(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]) + " + " + str(A[j-1][i-1][0])
                    print " -- " + str(scoreMatrix[X[i-1].upper()]["*"]) + " + " + str(A[j-1][i][0])
                    print " -- " + str(scoreMatrix["*"][Y[j-1].upper()]) + " + " + str(A[j][i-1][0])
                
                maximum = scoreMatrix[X[i-1].upper()][Y[j-1].upper()]+A[j-1][i-1][0]
                value = "d"
                if (maximum < scoreMatrix[X[i-1].upper()]["*"]+A[j-1][i][0]):
                    maximum = scoreMatrix[X[i-1].upper()]["*"]+A[j-1][i][0]
                    value = "u"
                if (maximum < scoreMatrix["*"][Y[j-1].upper()]+A[j][i-1][0]):
                    maximum = scoreMatrix["*"][Y[j-1].upper()]+A[j][i-1][0]
                    value = "l"

                A[j][i][0] = maximum
                A[j][i][1] = value

                if (printOption): printMatrix(A,"-"+X,"-"+Y)
    else:
        return 0
    return A

def BackwardAlignmentCosts(X,Y,printOption):
    if (printOption): print "--------------------------\nBACKWARD ALIGNMENT\n--------------------------"
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        A = [[0 for i in range(len(X)+1)] for j in range(len(Y)+1)]
        for i in range(len(X),-1,-1):
            A[len(Y)][len(X)-i] = scoreMatrix[X[len(X)-i-1].upper()]["*"]*i
        for j in range(len(Y),-1,-1):
            A[len(Y)-j][len(X)] = scoreMatrix[Y[len(Y)-j-1].upper()]["*"]*j
        if (printOption): printMatrix(A,X+"-",Y+"-")
    # Minimum alignment cost
        for j in range(len(Y)-1,-1,-1):
            for i in range(len(X)-1,-1,-1):
                if (printOption): 
                    print "MAX of: "
                    print " -- " + str(scoreMatrix[X[i].upper()][Y[j].upper()]) + " + " + str(A[j+1][i+1])
                    print " -- " + str(scoreMatrix[X[i].upper()]["*"]) + " + " + str(A[j+1][i])
                    print " -- " + str(scoreMatrix["*"][Y[j].upper()]) + " + " + str(A[j][i+1])
                A[j][i] = max(scoreMatrix[X[i].upper()][Y[j].upper()]+A[j+1][i+1],
                            scoreMatrix[X[i].upper()]["*"]+A[j+1][i],
                            scoreMatrix["*"][Y[j].upper()]+A[j][i+1])
                if (printOption): printMatrix(A,X+"-",Y+"-")
    else:
        return 0
    return A[0][0]

def SpaceEfficientAlignmentCosts(X,Y,printOption):
    if (printOption): print "--------------------------\nSPACE EFFICIENT ALIGNMENT\n--------------------------"
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        B = [[0 for i in range(len(X)+1)] for j in range(2)]
        for i in range(len(X)+1):
            B[0][i] = scoreMatrix[X[i-1].upper()]["*"]*i
    # Minimum alignment cost
        for j in range(1,len(Y)+1):
            B[1][0] = scoreMatrix[Y[j-1].upper()]["*"]*j
            if (printOption): printMatrix(B,"-"+X,"-"+str(Y[0]))
            for i in range(1,len(X)+1):
                if (printOption): 
                    print "MAX of: "
                    print " -- " + str(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]) + " + " + str(B[0][i-1])
                    print " -- " + str(scoreMatrix[X[i-1].upper()]["*"]) + " + " + str(B[1][i-1])
                    print " -- " + str(scoreMatrix["*"][Y[j-1].upper()]) + " + " + str(B[0][i])
                B[1][i] = max(scoreMatrix[X[i-1].upper()][Y[j-1].upper()]+B[0][i-1],
                            scoreMatrix[X[i-1].upper()]["*"]+B[1][i-1],
                            scoreMatrix["*"][Y[j-1].upper()]+B[0][i])
                if (printOption): printMatrix(B,"-"+X,"-"+str(Y[j-1]))
            for i in range(0,len(X)+1):
                B[0][i] = B[1][i]
    else:
        return 0
    return B[0][len(X)]

def BackwardSpaceEfficientAlignmentCosts(X,Y,printOption):
    if (printOption): print "--------------------------\nBACKWARD SPACE EFFICIENT ALIGNMENT\n--------------------------"
    # Initialize
    if ((len(Y) > 0) and (len(X) > 0)):
        B = [[0 for i in range(len(X)+1)] for j in range(2)]
        for i in range(len(X),-1,-1):
            B[0][len(X)-i] = scoreMatrix[X[len(X)-i-1].upper()]["*"]*i
    # Minimum alignment cost
        for j in range(len(Y)-1,-1,-1):
            B[1][len(X)] = scoreMatrix[Y[len(Y)-j-1].upper()]["*"]*(len(Y)-j)
            if (printOption): printMatrix(B,"-"+X,"-"+str(Y[0]))
            for i in range(len(X)-1,-1,-1):
                if (printOption): 
                    print "MAX of: "
                    print " -- " + str(scoreMatrix[X[i].upper()][Y[j].upper()]) + " + " + str(B[0][i+1])
                    print " -- " + str(scoreMatrix[X[i].upper()]["*"]) + " + " + str(B[1][i+1])
                    print " -- " + str(scoreMatrix["*"][Y[j].upper()]) + " + " + str(B[0][i])
                B[1][i] = max(scoreMatrix[X[i].upper()][Y[j].upper()]+B[0][i+1],
                            scoreMatrix[X[i].upper()]["*"]+B[1][i+1],
                            scoreMatrix["*"][Y[j].upper()]+B[0][i])
                if (printOption): printMatrix(B,"-"+X,"-"+str(Y[j]))
            for i in range(len(X),-1,-1):
                B[0][i] = B[1][i]
    else:
        return 0
    return B[0][0]

#Not finished
def DivideAndConquerAlignmentCosts(X,Y):
    # To-Do
    if (len(X) <= 2 or len(Y) <= 2):
        return Alignment(X,Y)

    P = []
    min1 = SpaceEfficientAlignment(X,Y[1:len(Y)/2],0)
    min2 = BackwardSpaceEfficientAlignment(X,Y[len(Y)/2+1:len(Y)-1])

    DivideAndConquerAlignment(X[1:q],Y[1:len(Y)/2])
    DivideAndConquerAlignment(x[q+1:len(Y)],Y[len(Y)/2+1:len(Y)-1])

    return 

def ConstructAlignment(A,X,Y,twist):
    m = len(X)
    n = len(Y)
    stringX = ""
    stringY = ""
    while (m > 0 and n > 0):
        if (A[n][m][1] == "d"):
            stringX = X[m-1] + stringX
            stringY = Y[n-1] + stringY
            m -= 1
            n -= 1
        elif (A[n][m][1] == "u"):
            stringX = "-" + stringX
            stringY = Y[n-1] + stringY
            n -= 1
        elif (A[n][m][1] == "l"):
            stringX = X[m-1] + stringX
            stringY = "-" + stringY
            m -= 1
    if (n > 0):
        stringY = Y[0:n]+ stringY
        stringX = "-"*n + stringX
    if (m > 0):
        stringX = X[0:m]+ stringX
        stringY = "-"*m + stringY

    if (twist):
        return stringY + "\n" + stringX
    else:
        return stringX + "\n" + stringY



if ((len(sys.argv) != 4)):
    printUsage()
    exit()
else:
    scoreMatrixFile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    scoreMatrix = parseScoreMatrix(scoreMatrixFile)
    #print scoreMatrix
    
    inputFile = [os.path.join(os.path.dirname(__file__), sys.argv[2])][0]
    proteinStructures = parseInputFile(inputFile)
    #print proteinStructures
    
    # Output
    results = {}
    creatures = proteinStructures.keys()
    for c1 in range(len(creatures)):
        for c2 in range(len(creatures)):
            if (c1 != c2):
                if ((str(creatures[c1]) + "--" + str(creatures[c2])) not in results and (str(creatures[c2]) + "--" + str(creatures[c1])) not in results):
                    X = proteinStructures[creatures[c1]].strip()
                    Y = proteinStructures[creatures[c2]].strip()
                    alignmentCostsWithStructure = AlignmentCostsWithStructure(X,Y,0)
                    results[str(creatures[c1]) + "--" + str(creatures[c2])] = [alignmentCostsWithStructure[len(Y)][len(X)][0],ConstructAlignment(alignmentCostsWithStructure,X,Y,0)]
                    results[str(creatures[c2]) + "--" + str(creatures[c1])] = [alignmentCostsWithStructure[len(Y)][len(X)][0],ConstructAlignment(alignmentCostsWithStructure,X,Y,1)]

    # Compare results
    filename = [os.path.join(os.path.dirname(__file__), sys.argv[3])][0]
    for result in results:
        line = result + ": " + str(results[result][0]) + "\n" + str(results[result][1])
        if line.split(":")[0]+":" in open(filename).read():
            if line in open(filename).read():
                print line + "\n--> OK\n"
            else:
                print line + "\n--> ERROR\n"
    
'''
    Y = "KQRIKAAKABK"
    X = "KQRK"
    alignmentCostsWithStructure = AlignmentCostsWithStructure(X,Y,0)
    print str(alignmentCostsWithStructure[len(Y)][len(X)][0])
    alignments = ConstructAlignment(alignmentCostsWithStructure,X,Y)


    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KQRK","KAK",0)) + "\n================="
    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KAK","KQRK",0)) + "\n================="
    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KQRIKAAKABK","KAK",0)) + "\n================="
    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KAK","KQRIKAAKABK",0)) + "\n================="
    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KQRK","KQRIKAAKABK",0)) + "\n================="
    #print "=================\nResult: " + str(BackwardSpaceEfficientAlignment("KQRIKAAKABK","KQRK",0)) + "\n================="
'''
    