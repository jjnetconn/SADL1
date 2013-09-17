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
P = []

# parse data
inputfile_name = sys.argv[1]
inputfile = open(inputfile_name, 'r')
for line in inputfile:
	if(not(line.split(' ')[0].isupper())):
		P.append((float(line.split(' ')[1]),float(line.split(' ')[2].rstrip("\n")),line.split(' ')[0]))

#print P

# helpers
def distance(p1,p2):
	return math.sqrt(math.fabs(p1[0]-p2[0])**2 + math.fabs(p1[1]-p2[1])**2)


def closest_pair(p):
	px = sorted(p, key=lambda x:p[0])
	py = sorted(p, key=lambda x:p[1])
	return closest_pair_rec(px,py)


def closest_pair_rec(px, py):
	if(len(px) < 3):
		if(len(px) < 2): return px[0],(10000000,10000000,'infinity')
		else: return px[0],px[1]
	
	splitter = len(px)/2
	qx,qy = px[:splitter],py[:splitter]
	rx,ry = px[splitter:],py[splitter:]

	q0,q1 = closest_pair_rec(qx,qy)
	r0,r1 = closest_pair_rec(rx,ry)

	#distance = lambda p1,p2 : math.sqrt(math.fabs(p1[0]-p2[0])**2 + math.fabs(p1[1]-p2[1])**2)
	
	delta = min(distance(q0,q1),distance(r0,r1))
	x_max = qx[len(qx)-1]

	within_delta = lambda p : math.fabs(x_max[0]-p[0]) < delta
	sy = filter(within_delta, py)
	#print "Py: " + str(py)
	#print "Sy: " + str(sy)

	closest0,closest1 = r0,r1
	if(distance(q0,q1) < distance(r0,r1)):
		closest0,closest1 = q0,q1

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
			closest0,closest1 = s0,s1
	
	return closest0,closest1


c0,c1 = closest_pair(P)
print c0,c1
print "With distance: " + str(distance(c0,c1))




