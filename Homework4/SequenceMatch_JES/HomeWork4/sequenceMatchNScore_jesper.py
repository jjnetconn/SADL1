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
    startTime = time.time()
    _buffer = []
    _gnomeName = ''

    with open(dataFile, 'r') as f:
        for line in f:
            if(line.startswith('>')):
                _gnomeName = line.strip('>').strip('\n').split(' ')[0]
            elif(not(line is ' ')):
                if((line.endswith('\n')) and not(line.startswith('>'))):
                    _buffer.append(line.strip('\n'))
                #print _buffer
                if(len(_buffer) > 2):
                    gnomes[_gnomeName] = ''.join(_buffer)
                    _buffer = []
                    
    endTime = time.time()
    print "--- importing Gnomes time: " + str(endTime - startTime)

def getScore(charX, charY):
    dicXchar = blosum62[charX]
    for dicti in dicXchar:
        if(dicti.has_key(charY)):
            return dicti.values()[0]

def alignment(x,y):
    startTime = time.time()
    M = zeros( (len(y)+1,len(x)+1) )
    d = float(getScore(x[0],'*'))
    
    for j in range(len(y)+1): 
        M[j][0] = d*j
    for i in range(len(x)+1): 
        M[0][i] = d*i
    
    for j in range(1,len(y)+1):
        for i in range(1,len(x)+1):
            a = float(getScore(x[i-1],y[j-1]))
            M[j][i] = max(a + M[j-1][i-1], d + M[j][i-1], d + M[j-1][i])
    endTime = time.time()
    print "--- Sequence alignment time is: " + str(endTime - startTime)
    
    print M

    return M[len(y)][len(x)]
    
#def devideConquerAlignemnt(x,y):
#    P= []
#    m = len(x)
#    n = len(y)
    
#    if((m <= 2) or (n <= 2)):
#        return alignment(x,y)
#    q = min(spaceEfficientAlignent(x,y), backwardSpaceEfficientAlignment(x,y))
    
importBlosum("data/BLOSUM62.txt")
#importInData("data/Toy_FASTAs.in")
importInData("data/HbB_FASTAs.in")
print "Alignment score: " + str(alignment(gnomes['Human'],gnomes['Gorilla']))