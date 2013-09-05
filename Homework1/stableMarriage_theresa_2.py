import sys
import time

# Initialize
debugMode = False # Set to true to switch on debug mode
n = 0
allPersons = {} #dict
menPrefs = {} #dict
womenPrefs = {} #dict

# Functions
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

start_time = time.clock()

# Read inputfile
inputFilename = sys.argv[1]
inputfile = open(inputFilename, 'r')
for line in inputfile:
	if ((line.startswith("n=")) and (isInt(line.partition("=")[2]))):
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
				menPrefs[int(line.split(": ")[0])] = prefs
			else:
				# Read women prefs (inverse)
				for prefStr in prefsStr:
					prefs[int(prefStr)] = index
					index += 1
				womenPrefs[int(line.split(": ")[0])] = prefs
		else:
			# Read all persons
			allPersons[int(line.strip().split(" ")[0])] = line.strip().split(" ")[1]

# Reading results
if (debugMode): print "All persons: " + str(allPersons) + "\nMen Preferences: " + str(menPrefs) + "\nWomen Preferences: " + str(womenPrefs)

#Validations
if (n == 0):
	print "ERROR: Bad data - n can't be empty"
	exit()
if (len(allPersons)/n != 2):
	print 'ERROR: Bad data - There is no equal number of man and woman'
	exit()
if (len(menPrefs) + len(womenPrefs) != len(allPersons)):
	print 'ERROR: Bad data - Not every person has a preference list'
	exit()

# Gale-Shapley Algorithm
freeMen = menPrefs.keys() #stack
wife = {man: -1 for man in freeMen} #dict
husband = {woman: -1 for woman in womenPrefs.keys()} #dict
proposals = {man: 0 for man in freeMen} #dict

while (len(freeMen) > 0):
	if (debugMode): print "------------------------------\nProposals of " + str(allPersons[freeMen[0]]) + ": " + str(proposals[freeMen[0]])
	if (proposals[freeMen[0]] < n):
		woman = menPrefs[freeMen[0]][proposals[freeMen[0]]+1]
		proposals[freeMen[0]] += 1
		if (debugMode): print str(allPersons[freeMen[0]]) + " proposes to " + str(allPersons[woman])
		if (husband[woman] == -1):
			if (debugMode): print str(allPersons[woman]) + " says yes"
			husband[woman] = freeMen[0]
			wife[freeMen[0]] = woman
			if (debugMode): print str(allPersons[freeMen[0]]) + " is not free anymore"
			freeMen.pop(0)
		elif (womenPrefs[woman][freeMen[0]] < womenPrefs[woman][husband[woman]]):
			if (debugMode): print str(allPersons[woman]) + " thinks " + str(allPersons[freeMen[0]]) + " is better than " + str(allPersons[husband[woman]])
			freeMen.append(husband[woman])
			if (debugMode): print str(allPersons[husband[woman]]) + " is free again"
			husband[woman] = freeMen[0]
			wife[freeMen[0]] = woman
			if (debugMode): print str(allPersons[freeMen[0]]) + " is not free anymore"
			freeMen.pop(0)
		else:
			if (debugMode): print str(allPersons[woman]) + " rejects " + str(allPersons[freeMen[0]])
	else:
		freeMen.pop(0)

elapsed_time = time.clock() - start_time

# Output
if (debugMode): print "=============================="
result = ""
for man in menPrefs.keys():
	result += allPersons[man] + " -- " + allPersons[wife[man]] + "\n"
print result

print "\nTime: " + str(elapsed_time) + "\n"

# Test output
if (len(sys.argv) == 3):
	testFilename = sys.argv[2]
	testFile = open(testFilename, 'r')
	if (testFile.read() == result):
		print "==============================\nOK\n=============================="
	else:
		print "==============================\nNOT OK\n=============================="