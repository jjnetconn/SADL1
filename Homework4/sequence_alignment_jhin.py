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

	for i in range(len(X)+1): M[0][i] = delta*i
	for j in range(len(Y)+1): M[j][0] = delta*j
	
	# build up M
	for j in range(1,len(Y)+1):
		for i in range(1,len(X)+1):
			alpha = get_score(X[i-1],Y[j-1])
			M[j][i] = max(alpha + M[j-1][i-1], delta + M[j][i-1], delta + M[j-1][i])

	# traceback for correct alignment
	x_sequence = y_sequence = ""
	i = len(X)
	j = len(Y)
	while(i > 0 or j > 0):
		if(i <= 0): 
			max_score = delta + M[j-1][i]
		elif(j <= 0):
			max_score = delta + M[j][i-1]
		else:
			alpha = get_score(X[i-1],Y[j-1])
			max_score = max(delta + M[j][i-1], delta + M[j-1][i], alpha + M[j-1][i-1])

		
		print "score: " + str(alpha)
		
		print "max score: " + str(max_score)
		print i, j
		# diagonal
		if(alpha + M[j-1][i-1] == max_score):
			print "diagonal"
			i -= 1
			j -= 1
			x_sequence = X[i] + x_sequence
			y_sequence = Y[j] + y_sequence
		# horizontal
		elif(delta + M[j][i-1] == max_score):
			print "horizontal"
			i -= 1
			x_sequence = X[i] + x_sequence
			y_sequence = "-" + y_sequence
		# vertical
		elif(delta + M[j-1][i] == max_score):
			print "vertical"
			j -= 1
			x_sequence = "-" + x_sequence
			y_sequence = Y[j] + y_sequence
			


	return M, M[len(Y)][len(X)], x_sequence, y_sequence






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


table,score,x_align,y_align = alignment("KQRK","KQRIKAAKABK")
print table
print score
print x_align
print y_align

