#FORD-FULKERSON
import sys
import Queue


# HELPERS
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False



# Edge class
class Edge(object):
	def __init__(self,u,v,w):
		self.source = u
		self.sink = v
		if(w == -1): w = 10000
		self.capacity = w

	def __repr__(self):
		return "%s->%s:%s" % (self.source, self.sink, self.capacity)

# NetworkFlow class
class NetworkFlow(object):
	def __init__(self):
		self.adj = {}
		self.flow = {}

	def add_vertex(self, vertex):
		self.adj[vertex] = []

	def add_edge(self, u, v, w):
		if(u == v):
			raise ValueError("u == v")
		edge = Edge(u,v,w)
		redge = Edge(v,u,w)
		edge.redge = redge
		redge.redge = edge
		self.adj[u].append(edge)
		self.adj[v].append(redge)
		self.flow[edge] = 0
		self.flow[redge] = 0

	def get_edges(self, vertex):
		return self.adj[vertex]

	
	def bfs(self, source, sink):
		q = Queue.Queue()
		checked = set()
		for edge in self.get_edges(source):
			q.put([(edge, 10000)])

		while not(q.empty()):
			temp_path = q.get()
			last_set = temp_path[-1]
			last_vertex = last_set[0].sink
			if(last_vertex == sink):
				return temp_path
			for edge in self.get_edges(last_vertex):
				residual = edge.capacity - self.flow[edge]
				if(residual > 0 and not (edge,residual) in checked):
					checked.add((edge,residual))
					new_path = []
					new_path = temp_path + [(edge, residual)]
					q.put(new_path)
		return None

	def augment(self, path):
		flow = min(res for edge,res in path) # bottleneck
		for edge,res in path:
			self.flow[edge] += flow
			self.flow[edge.redge] -= flow
 

	def maxflow_mincut(self, source, sink):
		path = self.bfs(source, sink)
		while path != None:
			self.augment(path)
			path = self.bfs(source, sink)
		maxflow = sum(self.flow[edge] for edge in self.get_edges(source))
		return maxflow, None
    


############
### RUN
############

nf = NetworkFlow()

# parse
indx = 0
indices = {}
inputfile_name = sys.argv[1]
input_file = open(inputfile_name, 'r')
for line in input_file:
	chars = line.rstrip('\n').split(' ')
	if(line != ""):
		if(len(chars) < 3):
			if(is_int(chars[0])):
				if(int(chars[0]) > 54): 
					continue
			nf.add_vertex(indx)
			indices[chars[0]] = indx
			indx += 1
		else:
			nf.add_edge(int(chars[0]), int(chars[1]), int(chars[2]))

maxflow,mincut = nf.maxflow_mincut(indices["ORIGINS"],indices["DESTINATIONS"])
print "Max-flow: " + str(maxflow)
print "Min-cut: " + str(mincut)




