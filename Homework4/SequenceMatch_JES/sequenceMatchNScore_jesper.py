#import numpy
from numpy import *
import time

#Datafields
blosum62 = {} #Type dict
gnomes = {}
_inData = []
charList = []

i = 0
j = 0

def importBlosum(dataFile):
    startTime = time.time()
    #print blosum_file
    global i
    global _inData
    global j
    with open(dataFile, 'r') as f:
        for line in f:
            _inData = line.split('\r')
            #print _inData
        for line in _inData:
            if(not(line.startswith('#'))):
                if(line.startswith(' ')):
                    tmpLine = line.lstrip(' ')
                    charList = ' '.join(tmpLine.split()).split(' ')
                    for item in charList:
                        blosum62.update({item:{}})
                    _tmpArr = []
                elif(not(line.startswith('  '))):
                    line = ' '.join(line.split())
                    _tmpArr = line.split(' ')[1:]
                    #print _tmpArr
                    #print charList[i]
                    _tmpLst = []
                    j=0
                    for itm in charList:
                        _tmpLst.append({itm[0]:_tmpArr[j]})
                        j = j+1
                    blosum62[charList[i]] = _tmpLst
                    i=i+1
                            
    endTime = time.time()
    print "--- blosum62 import time: " + str(endTime - startTime)

def importInData(dataFile):
    global gnomes
    #startTime = time.time()
    _tmpLine = ''
    _tmp2Line = ''
    with open(dataFile, 'r') as f:
        for line in f:

            if(line.startswith('>')):
                _tmpLine = line.strip('>').strip('\n').split(' ')[0]
            elif(not(line == ' ')):
                _tmp2Line = _tmp2Line + line.strip('\R').strip('\n')
                _genLine = line.join(line.split()).split('\r')
                #print str(_genLine) + " : EOL"
            gnomes[_tmpLine] = _tmp2Line

def getScore(charX, charY):
    dicXchar = blosum62[charX]
    for dicti in dicXchar:
        if(dicti.has_key(charY)):
            return dicti.values()[0]

def aligenment(x,y):
    M = zeros( (len(y)+1,len(x)+1) )
    distance = float(getScore(x[0],'*'))
    
    for j in range(len(y)+1): 
        M[j][0] = distance*j
    for i in range(len(x)+1): 
        M[0][i] = distance*i
    
    for j in range(1,len(y)+1):
        for i in range(1,len(x)+1):
            alpha = float(getScore(x[i-1],y[j-1]))
            M[j][i] = max(alpha + M[j-1][i-1], distance + M[j][i-1], distance + M[j-1][i])

    return M[len(y)][len(x)]
    
importBlosum("data/BLOSUM62.txt")
importInData("data/Toy_FASTAs.in")
#importInData("data/HbB_FASTAs.in")
print aligenment(gnomes['Bandersnatch'], gnomes['Snark'])