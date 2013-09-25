# Closest pairs in the plane
import math
import sys
import time

# TEST DATA
'''
P = [	
				(0, -10, 'far'),
				(0, 0, 'romeo'),
				(0, 1, 'juliet'),
				(0, 10, 'far')
				]
'''


# parse data
def test_input_file(inputf_name,input_dist):
	P = []
	inputf = open(inputf_name, 'r')
	for line in inputf:
		line = " ".join(line.split())
		if(not(line.split(' ')[0].isupper()) and not(line == "") and len(line.split(' ')) == 3):
			#print "About to split this line...: " + line
			P.append((float(line.split(' ')[1]),float(line.split(' ')[2].rstrip("\n")),line.split(' ')[0]))
	c0,c1 = closest_pair(P)

	calc_dist = round(distance(c0,c1),2)
	correct_dist = round(float(input_dist),2)
	correct = 'ERROR'
	if(calc_dist == correct_dist): correct = 'OK'
	print "Testing input file: " + inputf_name + " - found: " + str(calc_dist) + " correct: " + str(correct_dist) + " -> " + correct
	#print c0,c1
	#print "Closest distance: " + str(round(distance(c0,c1),2))
	#print "Distance should be: " + str(round(float(input_dist),2))
	#print "\n"

#print P

# helpers
def distance(p1,p2):
	return math.sqrt(math.fabs(p1[0]-p2[0])**2 + math.fabs(p1[1]-p2[1])**2)


def closest_pair(p):
	px = sorted(p, key=lambda x:x[0])
	py = sorted(p, key=lambda x:x[1])
	return closest_pair_rec(px,py)


def closest_pair_rec(px, py):
	if(len(px) < 3):
		if(len(px) < 2): return px[0],(float('inf'),float('inf'),'infinity')
		else: return px[0],px[1]
	
	splitter = len(px)/2
	qx = px[:splitter]
	rx = px[splitter:]

	x_max = qx[-1][0]
	qy,ry = [],[]
	for p in py:
		if(p[0] <= x_max):
			qy.append(p)
		else:
			ry.append(p)

	#qy, ry = [], []
    #xDivider = qx[-1][0]
    #for p in py:
		#if p[0] <= xDivider:
			#qy.append(p)
 		#else:
			#ry.append(p)

	#qx,qy = px[:splitter],py[:splitter]
	#rx,ry = px[splitter:],py[splitter:]
	#x_max = qx[-1]
	#qy = filter(lambda x : x[0] >= qx[0][0] and x[0] <= qx[-1][0],py)
	#ry = filter(lambda x : x[0] >= rx[0][0] and x[0] <= rx[-1][0],py)
	#ry = filter(lambda x : x[0] > x_max,rx)

	#qy = sorted(qx, key=lambda x:x[1])
	#ry = sorted(rx, key=lambda x:x[1])


	#qx,qy = px[:splitter],py[:splitter]
	#rx,ry = px[splitter:],py[splitter:]

	q0,q1 = closest_pair_rec(qx,qy)
	r0,r1 = closest_pair_rec(rx,ry)
	
	delta = min(distance(q0,q1),distance(r0,r1))
	#print "delta: " + str(delta)
	#print len(py)
	#x_max = qx[len(qx)-1]

	#print py
	#print "\n\n"

	within_delta = lambda x : math.fabs(x_max-x[0]) < delta
	sy = filter(within_delta, py)
	#sy = sorted(sy, key=lambda x:x[1])

	#sy = py
	#for y in sy:
		#if(y[2] == '1273'):
			#print 'OK 1 with x distance: ' + str(math.fabs(x_max[0]-y[0]))
		#if(y[2] == '1310'):
			#print 'OK 2 with x distance: ' + str(math.fabs(x_max[0]-y[0]))
	#print "Py: " + str(py)
	#print "Sy: " + str(sy)

	closest0,closest1 = r0,r1
	if(distance(q0,q1) < distance(r0,r1)):
		closest0,closest1 = q0,q1

	#if(len(sy)==1):
		#print "x_max: " + str(x_max) + " and sy point: " + str(sy[0])

	if(len(sy) > 1):
		s_count = 0
		s_min = distance(sy[0],sy[1])
		s0,s1 = sy[0],sy[1]
		for s in sy:
			n_count = 1
			while s_count+n_count < len(sy) and n_count < 16:
				n = sy[s_count+n_count]
				s_next = distance(s,n)
				if(s_next < s_min):
					s_min = s_next
					s0,s1 = s,n
				n_count += 1
			s_count += 1
		if(distance(s0,s1) < distance(closest0,closest1)):
			#print "There is a closer distance in S: " + str(distance(s0,s1))
			closest0,closest1 = s0,s1
	
	return closest0,closest1


inputfile_name = sys.argv[1]
inputfile = open(inputfile_name, 'r')
count = 1
for line in inputfile:
	filename = line.split(' ')[0].rstrip(':')
	dist = line.split(' ')[2].rstrip('\n')
	#if(count==16): test_input_file(filename,dist)
	test_input_file(filename,dist)
	count += 1






