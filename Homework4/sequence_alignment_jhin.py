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
	score = score_matrix[char_index[char_x]][char_index[char_y]]
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

		# diagonal
		if(alpha + M[j-1][i-1] == max_score):
			i -= 1
			j -= 1
			x_sequence = X[i] + x_sequence
			y_sequence = Y[j] + y_sequence
		# horizontal
		elif(delta + M[j][i-1] == max_score):
			i -= 1
			x_sequence = X[i] + x_sequence
			y_sequence = "-" + y_sequence
		# vertical
		elif(delta + M[j-1][i] == max_score):
			j -= 1
			x_sequence = "-" + x_sequence
			y_sequence = Y[j] + y_sequence
			


	return M, M[len(Y)][len(X)], x_sequence, y_sequence


def is_in_dict(key,dict):
	try:
		dict[key]
	except KeyError:
		return False
	else:
		return True 




char_index = dict()
score_matrix = []


#################
## PARSING
#################
# score matrix
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

# input file
specimen = []
specimen_name = ""
protein_string = ""
count = 0
inputfile_name = sys.argv[2]
input_file = open(inputfile_name, 'r')
for line in input_file:
	if (line.startswith('>')):
		if(count > 0):
			specimen.append((specimen_name,protein_string))
		items = " ".join(line.split())
		specimen_name = items.split(' ')[0].lstrip('>')
		protein_string = ""
	elif(line.isupper()):
		protein_string += line.rstrip('\n')
	count += 1
specimen.append((specimen_name,protein_string))
#print specimen

# output file
inputfile_name = sys.argv[3]
output_file = open(inputfile_name, 'r')
valid_output = dict()
for line in output_file:
	if(':' in line):
		count = 0
		comp_key = line.split(':')[0]
		score = int(line.split(':')[1].strip(' ').strip('\n'))
		valid_output[comp_key] = []
		valid_output[comp_key].append(score)
	elif(not(line == '')):
		valid_output[comp_key].append(line.strip('\n'))
#print valid_output



#########
## RUN
#########
# running algorithm on input file
for i in range(len(specimen)):
	for j in range(i+1,len(specimen)):
		spec1,spec2 = specimen[i][1],specimen[j][1]
		comp_key = specimen[i][0] + "--" + specimen[j][0]
		if(not(is_in_dict(comp_key,valid_output))): 
			spec1,spec2 = specimen[j][1],specimen[i][1]
			comp_key = specimen[j][0] + "--" + specimen[i][0]
		table,score,x_align,y_align = alignment(spec1,spec2)
		#comp_key = specimen[i][0] + "--" + specimen[j][0]
		#if(not(is_in_dict(comp_key,valid_output))): comp_key = specimen[j][0] + "--" + specimen[i][0]
		print comp_key + ": " + str(score)
		print x_align
		print y_align
		#print valid_output[comp_key]
		if(valid_output[comp_key][0] == score): valid_score = "OK"
		else: valid_score = "ERROR"
		if(valid_output[comp_key][1] == x_align and valid_output[comp_key][2] == y_align): valid_align = "OK"
		else: valid_align = "ERROR"
		print "Validating score... " + valid_score
		print "Validating alignment... " + valid_align + "\n"



#table,score,x_align,y_align = alignment("KQRK","KQRIKAAKABK")
#print table
#print score
#print x_align
#print y_align

