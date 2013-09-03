import sys

# Initialize
debugMode = True # Set to true to switch on debug mode
n = 0
allPersons = [] #array
menPrefs = [] #array
womenPrefs = [] #array

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

# Read inputfile
inputFilename = sys.argv[1]
inputfile = open(inputFilename, 'r')
for line in inputfile:
	if ((line.startswith("n=")) and (isInt(line.partition("=")[2]))):
		n = int(line.partition("=")[2])
		allPersons = [''] * 2 * n
		menPrefs = [[0] * n] * n
		womenPrefs = [[0] * n] * n
	elif ((line) and (not line.startswith("#")) and (isInt(line[0])) and (n != 0)):
		if (line.find(":") != -1):
			prefsStr = line.strip().split(": ")[1].split(" ")
			prefs = [0] * n
			index = 0			
			if (int(line.split(": ")[0])%2 == 1):
				# Read men prefs
				for prefStr in prefsStr:
					prefs[index] = (int(prefStr)-1)/2
					index += 1
				menPrefs[(int(line.split(": ")[0])-1)/2] = prefs
			else:
				# Read women prefs (inverse)
				for prefStr in prefsStr:
					prefs[(int(prefStr)-1)/2] = index
					index += 1
				womenPrefs[(int(line.split(": ")[0])-1)/2] = prefs
		else:
			# Read all persons
			allPersons[int(line.strip().split(" ")[0])-1] = line.strip().split(" ")[1].replace("\n","")

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
freeMen = range(n) #stack
wife = [-1] * n #array
husband = [-1] * n #array
proposals = [0] * n #array
while (len(freeMen) > 0):
	if (debugMode): print "------------------------------\nProposals of " + str(allPersons[freeMen[0]*2]) + ": " + str(proposals[freeMen[0]])
	if (proposals[freeMen[0]] < n):
		woman = menPrefs[freeMen[0]][proposals[freeMen[0]]]
		proposals[freeMen[0]] += 1
		if (debugMode): print str(allPersons[freeMen[0]*2]) + " proposes to " + str(allPersons[woman*2+1])
		if (husband[woman] == -1):
			if (debugMode): print str(allPersons[woman*2+1]) + " says yes"
			husband[woman] = freeMen[0]
			wife[freeMen[0]] = woman
			if (debugMode): print str(allPersons[freeMen[0]*2]) + " is not free anymore"
			freeMen.pop(0)
		elif (womenPrefs[woman][freeMen[0]] < womenPrefs[woman][husband[woman]]):
			if (debugMode): print str(allPersons[woman*2+1]) + " thinks " + str(allPersons[freeMen[0]*2]) + " is better than " + str(allPersons[husband[woman]*2])
			freeMen.append(husband[woman])
			if (debugMode): print str(allPersons[husband[woman]*2]) + " is free again"
			husband[woman] = freeMen[0]
			wife[freeMen[0]] = woman
			if (debugMode): print str(allPersons[freeMen[0]*2]) + " is not free anymore"
			freeMen.pop(0)
		else:
			if (debugMode): print str(allPersons[woman*2+1]) + " rejects " + str(allPersons[freeMen[0]*2])
	else:
		freeMen.pop(0)

# Output
if (debugMode): print "=============================="
result = ""
for man in range(n):
	result += allPersons[man*2] + " -- " + allPersons[wife[man]*2+1] + "\n"
print result

# Test output
if (len(sys.argv) == 3):
	testFilename = sys.argv[2]
	testFile = open(testFilename, 'r')
	if (testFile.read() == result):
		print "==============================\nOK\n=============================="
	else:
		print "==============================\nNOT OK\n=============================="


