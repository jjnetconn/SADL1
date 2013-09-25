# SEQUENCE ALIGNMENT
from numpy import *
import sys


# HELPERS
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_score(char_x,char_y):
	#print "Compare " + char_x + " with " + char_y
	score = score_matrix[char_index[char_x]][char_index[char_y]]
	#print "The score is " + str(score)
	#print "\n"
	#score = 0
	return score



# Sequence algorithm
def alignment(X,Y):
	M = zeros( (len(Y)+1,len(X)+1) )
	# gap penalty
	delta = get_score(X[0],"*")

	#M = [[None for x in range(len(X)+1)] for y in range(len(Y)+1)]
	#A = [[None for x in range(len(X))] for y in range(len(Y))]
	#for i in range(len(X)+1): M[0][i] = 0
	#for j in range(len(Y)+1): M[j][0] = 0

	for j in range(len(Y)+1): M[j][0] = delta*j
	for i in range(len(X)+1): M[0][i] = delta*i
	#print M
	for j in range(1,len(Y)+1):
		for i in range(1,len(X)+1):
			alpha = get_score(X[i-1],Y[j-1])
			M[j][i] = max(alpha + M[j-1][i-1], delta + M[j][i-1], delta + M[j-1][i])

	print M

	return M[len(Y)][len(X)]






#parse score matrix
char_index = dict()
score_matrix = []

inputfile_name = sys.argv[1]
score_file = open(inputfile_name, 'r')
for line in score_file:
	if (not(line.startswith('#'))):
		items = " ".join(line.split())
		if(line.startswith(' ') and not(line == '')):
			count = 0
			for i in items.split(' '): 
				char_index[i] = count
				count += 1
		else:
			row = []
			for i in items.split(' '):
				if(is_int(i)):
					row.append(int(i))
			score_matrix.append(row)



print alignment("KQRK","KQRIKAAKABK")

