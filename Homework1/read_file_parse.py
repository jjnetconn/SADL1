import re
import time

#Initialize list and dict
men = []
ladies = {}

#Get timestamp for codestart
t0 = time.time()

#regex match on eg. "3 Rachel"
pat2 = re.compile("[0-9]\s+")

#regex match on eg. "1:6 2 4"
pat3 = re.compile("[0-9]\:")

#Openfile and read line by line
with open('stable-marriage-friends.in', 'r') as f:
	for line in f:
		match = pat2.match(line)
		if match:
			_matched= line
			_splitted = _matched.split(' ')
			_splitted[1] = _splitted[1].rstrip()
			
			if int(_splitted[0]) % 2 != 0:
				print _splitted[1]
				men.append([_splitted[1]])
			else:
				print _splitted[0] + _splitted[1]
				ladies.setdefault(int(_splitted[0]), _splitted[1])
#Get stop timestamp
t1 = time.time()
#Calc exec time
totaltime = t1 - t0

print "\n"
print "Start time: " + str(t0)
print "\n"
print "End time: " + str(t1)
print "\n"
print "execution time: "
print totaltime
print "\n"
print "Values in List, men:\n"
print men
print "\n"
print "Values in dict, ladies:\n"
print ladies