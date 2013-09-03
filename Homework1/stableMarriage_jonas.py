import sys

# Helpers
def isInt(i):
    try: 
        int(i)
        return True
    except ValueError:
        return False

# datastructures

# TEST
#n = 3
#persons = ['Ross', 'Monica', 'Chandler', 'Phoebe', 'Joey', 'Rachel']
#free_men = range(3)
#man_pref = [[2,1,0],[0,1,2],[2,1,0]]
#woman_pref = [[1,2,0],[2,0,1],[0,2,1]]
#next = [0] * n
#current = [-1] * n
#ranking = [[1,3,2],[2,1,3],[3,1,2]] # aux array

n = 0
persons = []
man_pref = []
ranking = []

# Read parameters
if ((len(sys.argv) < 2) or (len(sys.argv) > 4)):
   print "USAGE:	stableMarriage.py <inputfile> [<testfile>]"
   print ""
   print "	PARAMETERS"
   print "	<inputfile>	Filename of inputfile"
   print "	<testfile>		Filename of expected outputfile"
   exit()

# Parsing inputfile
inputfile_name = sys.argv[1]
inputfile = open(inputfile_name, 'r')
for line in inputfile:
	if ((line.startswith("n=")) and (isInt(line.partition("=")[2]))):
		# init lists
		n = int(line.partition("=")[2])
		persons = [''] * 2 * n
		man_pref = [[0] * n] * n
		ranking = [[0] * n] * n
	elif ((line) and (not line.startswith("#")) and (isInt(line[0])) and (n != 0)):
		if (line.find(":") != -1):
			prefs_str = line.strip().split(": ")[1].split(" ")
			prefs = [0] * n
			ranks = [0] * n
			index = 0			
			if (int(line.split(": ")[0])%2 == 1):
				# Read men prefs
				for pref_str in prefs_str:
					prefs[index] = (int(pref_str)-1)/2
					index += 1
				man_pref[(int(line.split(": ")[0])-1)/2] = prefs
			else:
				# Read women prefs (inverse)
				for pref_str in prefs_str:
					ranks[(int(pref_str)-1)/2] = index
					index += 1
				# build aux array ranking for later men comparison
				ranking[(int(line.split(": ")[0])-1)/2] = ranks
		else:
			# Read all persons
			persons[int(line.strip().split(" ")[0])-1] = line.strip().split(" ")[1].replace("\n","")

# Reading results
#print "All persons: " + str(persons) + "\nMen Preferences: " + str(man_pref) + "\nRanking: " + str(ranking) 


# Gale-Shapley algorithm
free_men = range(n)
next = [0] * n # next woman to propose to
current = [-1] * n # a womans current man (-1 = none)
while len(free_men) > 0:
	m = free_men.pop(0)
	w = man_pref[m][next[m]]
	next[m] += 1
	# w is free
	if(current[w] == -1):
		#m and w become engaged
		current[w] = m
	else:
		# check if woman prefers current man
		if(ranking[w][m] > ranking[w][current[w]]):
			# m stays free
			free_men.append(m)
		else:
			# old man becomes free and new engaged to w
			free_men.append(current[w])
			current[w] = m


# print out matches
result = ''
for man in range(n):
	#print "Next woman : " + str(man_pref[man][next[man]-1]) + "\n"
	result += persons[man*2] + " -- " + persons[man_pref[man][next[man]-1]*2+1] + "\n"
print result



# Test output
if (len(sys.argv) == 3):
	testfile_name = sys.argv[2]
	testfile = open(testfile_name, 'r')
	if (testfile.read() == result):
		print "==============================\nOK\n=============================="
	else:
		print "==============================\nNOT OK\n=============================="

