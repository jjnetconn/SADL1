import sys
import time
import copy
#Enable Debugging
doDebug = False

# Vars
n = 0
allPers = {} #dict
menPref = {} #dict
womenPref = {} #dict
freeMen = "" #stack
wife = {} #dict
husband = {} #dict
proposals = {} #dict
result = ""

# Timers
totalTimeS = 0
totalTimeE = 0
importTimeS = 0
importTimeE = 0
matchTimeS = 0
matchTimeE = 0

# using time.clock() due to dev on Windows
totalTimeS = time.time()

# Helping functions
def isInt(i):
    try: 
        int(i)
        return True
    except ValueError:
        return False

# Read parameters
if ((len(sys.argv) < 2) or (len(sys.argv) > 4)):
   print "USAGE:	stableMarriage.py <inputfile> [<testfile>]"
   print ""
   print "	PARAMETERS"
   print "	<inputfile>	Filename of inputfile"
   print "	<testfile>		Filename of expected outputfile"
   exit()

#FileLoader and parser Function
def loadFile(fileName): 
	with open(fileName, 'r') as f:
		for line in f:
			if ((line.startswith("n=")) and (isInt(line.partition("=")[2]))):
				#Assigning globals
				global n
				n = int(line.partition("=")[2])
			elif ((line) and (not line.startswith("#")) and (isInt(line[0])) and (n != 0)):
				if (line.find(":") != -1):
					prefsStr = line.strip().split(": ")[1].split(" ")
					prefs = {}
					index = 1			
					if (int(line.split(": ")[0])%2 == 1):
						# Read men prefs
						for prefStr in prefsStr:
							prefs[index] = int(prefStr)
							index += 1
						menPref[int(line.split(": ")[0])] = prefs
					else:
						# Read women prefs (inverse)
						for prefStr in prefsStr:
							prefs[int(prefStr)] = index
							index += 1
						womenPref[int(line.split(": ")[0])] = prefs
				else:
					# Read all persons
					allPers[int(line.strip().split(" ")[0])] = line.strip().split(" ")[1]

# Matchmaker function using - Gale-Sharpley Algorithme
def matchMaker():
	#Assigning globals
	global freeMen, wife, husband, proposals
	
	freeMen = menPref.keys() #stack
	wife = {man: -1 for man in freeMen} #dict
	husband = {woman: -1 for woman in womenPref.keys()} #dict
	proposals = {man: 0 for man in freeMen} #dict

	while (len(freeMen) > 0):
		if (doDebug): print "------------------------------\nProposals of " + str(allPers[freeMen[0]]) + ": " + str(proposals[freeMen[0]])
		if (proposals[freeMen[0]] < n):
			woman = menPref[freeMen[0]][proposals[freeMen[0]]+1]
			proposals[freeMen[0]] += 1
			if (doDebug): print str(allPers[freeMen[0]]) + " proposes to " + str(allPers[woman])
			if (husband[woman] == -1):
				if (doDebug): print str(allPers[woman]) + " says yes"
				husband[woman] = freeMen[0]
				wife[freeMen[0]] = woman
				if (doDebug): print str(allPers[freeMen[0]]) + " is not free anymore"
				freeMen.pop(0)
			elif (womenPref[woman][freeMen[0]] < womenPref[woman][husband[woman]]):
				if (doDebug): print str(allPers[woman]) + " thinks " + str(allPers[freeMen[0]]) + " is better than " + str(allPers[husband[woman]])
				freeMen.append(husband[woman])
				if (doDebug): print str(allPers[husband[woman]]) + " is free again"
				husband[woman] = freeMen[0]
				wife[freeMen[0]] = woman
				if (doDebug): print str(allPers[freeMen[0]]) + " is not free anymore"
				freeMen.pop(0)
			else:
				if (doDebug): print str(allPers[woman]) + " rejects " + str(allPers[freeMen[0]])
		else:
			freeMen.pop(0)
	# Output
	if (doDebug): print "-----------------------------"
	result = ""
	for man in menPref.keys():
		result += allPers[man] + " -- " + allPers[wife[man]] + "\n"
	return result

importTimeS = time.time()

loadFile(sys.argv[1])

importTimeE = time.time()


# Reading results
if (doDebug): print "All persons: " + str(allPers) + "\nMen Preferences: " + str(menPref) + "\nWomen Preferences: " + str(womenPref)

matchTimeS = time.time()

result = matchMaker()

matchTimeE = time.time()

print "\n--- Results: \n" + result + "\n"

# Test output
if (len(sys.argv) == 3):
	testFilename = sys.argv[2]
	testFile = open(testFilename, 'r')
	if (testFile.read() == result):
		print "------------------------------\nOK: Match is stable\n------------------------------"
	else:
		print "------------------------------\nNOT OK: Match is unstable\n------------------------------"

totalTimeE = time.time()
print "\n--- Timers:" 

print " - Total runtime: " + str(totalTimeE - totalTimeS) + " secs.\n"
print " - Import data runtime: " + str(importTimeE - importTimeS)  + " secs.\n"
print " - Matchmaker runtime: " + str(matchTimeE - matchTimeS) + " secs.\n"
print "\n - Results are saved in: " + sys.argv[1].split('.')[0] + "_Jesper.out"

f1=open(sys.argv[1].split('.')[0] + "_Jesper.out", 'w+')
f1.write(result)