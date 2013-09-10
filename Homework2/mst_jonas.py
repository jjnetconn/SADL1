## KRUSKAL IMPLEMENTATION (MST)
import Queue
import sys
import time

parse_time = 0
algorithm_time = 0

# test data
'''
graph = {
		"vertices": ["Duckberg","Gotham City","Metropolis"],
		"edges": set([
			(2324,"Duckberg","Gotham City"),
			(231,"Duckberg","Metropolis"),
			(2298,"Gotham City","Metropolis")
			])
		}
'''
graph = {
		'vertices':[],
		'edges':set()
		}

# parse input file
parse_time = time.time()

inputfile_name = sys.argv[1]
inputfile = open(inputfile_name, 'r')
for line in inputfile:
	# vertices
	if(line.find('--') == -1):
		v = line.replace('"','').replace(' \n','')
		graph['vertices'].append(v)
	else:
		v = line.split('--')[0].replace('"','')
		w = line.split('--')[1].split(' [')[0].replace('"','')
		weight = int(line.split('--')[1].split(' [')[1].replace(']','').replace('\n',''))
		graph['edges'].add((weight,v,w))

parse_time = time.time() - parse_time

# Union Find (weighted)
parent = dict()
rank = dict()

def find(v):
	while v != parent[v]:
		v = parent[v]
	return v

def union(v, w):
	root_v = find(v)
	root_w = find(w)
	# make smaller root point to larger one
	if(rank[root_v] < rank[root_w]):
		parent[root_v] = root_w
		rank[root_w] += rank[root_v]
	else:
		parent[root_w] = root_v
		rank[root_v] += rank[root_w]


# Kruskals algorithm
def kruskal(graph):
	# an edges parent is itself from start (with rank 0)
	for vertice in graph['vertices']:
		parent[vertice] = vertice
		rank[vertice] = 0

	mst = []

	# priority queue
	'''
	pq = Queue.PriorityQueue()
	for edge in graph['edges']:
		pq.put(edge)

	while(not(pq.empty())):
		edge = pq.get()
		weight,v,w = edge
		if(find(v) != find(w)):
			union(v,w)
			mst.append(edge)
	'''
	edges = list(graph['edges'])
	edges.sort()
	for edge in edges:
		weight,v,w = edge
		if(find(v) != find(w)):
			union(v,w)
			mst.append(edge)

	return mst


# total weight
def total_weight(mst):
	total_weight = 0
	for edge in mst:
		weight,v,w = edge
		total_weight += weight
	return total_weight


algorithm_time = time.time()
mst = kruskal(graph)
algorithm_time = time.time() - algorithm_time

print "\nTotal distance is: " + str(total_weight(mst))
print "\nParsing time: " + str(parse_time)
print "Algorithm time: " + str(algorithm_time)
print "Total time: " + str(parse_time + algorithm_time) + "\n"





