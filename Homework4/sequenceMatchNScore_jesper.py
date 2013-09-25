
import time

#Datafields
blosum62 = {} #Type dict
vertIndex = [] #Type list
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
    print "blosum62 import time: "
    print endTime - startTime
    print blosum62

                 
importBlosum("data/BLOSUM62.in")
