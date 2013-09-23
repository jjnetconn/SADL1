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
                for num in range(0,len(scores)-1):
                    proteinScores[proteins[num]] = scores[num]
                #print "ProteinScores: " + str(proteinScores)
                scoreMatrix[protein[0]] = proteinScores
            #print "ScoreMatrix: " + str(scoreMatrix)
    return scoreMatrix

def parseInputFile(filename):
    inputFile = open(filename, 'r')
    proteinStructures = {}
    creaturePattern = '[^\>][\w\-]*'
    for line in inputFile:
        #print line
        if (line.startswith(">")):
            creature = re.findall(creaturePattern,line)[0]
            #print "Creature: " +  str(creature)
        else:
            proteins = re.findall("([A-Z])",line.strip())
            #print "Proteins: " + str(proteins)
            proteinStructures[creature] = proteins
    return proteinStructures
    

# Read parameters and input files

def algorithm():
    # To-Do
    return 0

if ((len(sys.argv) != 4)):
    printUsage()
    exit()
else:
    scoreMatrixFile = [os.path.join(os.path.dirname(__file__), sys.argv[2])][0]
    #print scoreMatrixFile
    scoreMatrix = parseScoreMatrix(scoreMatrixFile)
    print scoreMatrix
    
    inputFile = [os.path.join(os.path.dirname(__file__), sys.argv[1])][0]
    #print inputFile
    proteinStructures = parseInputFile(inputFile)
    print proteinStructures
    
    algorithm()