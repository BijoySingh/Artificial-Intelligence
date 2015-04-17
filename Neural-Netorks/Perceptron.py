import math
import random

def modifyTT(truth_table):
		for row in truth_table:
			row[0].append(-1)
			if(row[1] == 0):
				lst = row[0]
				lst = [-1*x for x in row[0]]
				row[0] = lst
		return truth_table

class Perceptron(object):

	output = 0
	
	def __init__(self, size,randm = False):
		super(Perceptron, self).__init__()
		self.weights = []
		self.weight_deltas = []
		for i in range(size+1):
			if(randm):
				self.weights.append(random.random())
			else:	
				self.weights.append(0)
			self.weight_deltas.append(0)

		self.number_of_inputs = size

	def process_input(self, inp,mode=0):
		if(mode == 0):
			self.output = self.getSigmoidClass(inp)
		else:
			self.output = self.getClass(inp)

	def reset_weight_deltas(self):
		for delta in self.weight_deltas:
			delta = 0

	def get_sum(self,inp):
		# print("W : "+  str(len(self.weights)) + " : " + str(self.weights))
		# print(inp)
		net = 0
		pos = 0
		for wt in self.weights:
			net += wt*inp[pos]
			pos+=1
		return net

	def getSigmoidClass(self,inp):
		net = self.get_sum(inp)
		value = 1.0 /(1.0 + math.exp(-1*net))
		return value

	def getClass(self, inp):
		net = self.get_sum(inp)
		if(net > 0):
			return 1
		return 0

	def train(self, truth_table):
		truth_table = modifyTT(truth_table)
		print(truth_table)
		pain = True
		pos = 1
		while (pain):
			print(str(pos) + ">>" + str(self.weights))
			pos+=1
			pain = False
			for row in truth_table:
				current_class = self.getClass(row[0])
				if(current_class != 1):
					pain = True
					for i in range(len(row[0])):
						self.weights[i] += row[0][i]
					break

		print(self.weights)

'''
print("AND")
and_pc = Perceptron(2)
and_tt = [[[0,0],0],[[1,0],0],[[0,1],0],[[1,1],1]]
and_pc.train(and_tt)

print("OR")
or_pc = Perceptron(2)
or_tt = [[[0,0],0],[[1,0],1],[[0,1],1],[[1,1],1]]
or_pc.train(or_tt)

print("MAJORITY")
maj_pc = Perceptron(3)
maj_tt = [[[0,0,0],0],[[0,0,1],0],[[0,1,0],0],[[1,0,0],0],
		[[1,1,0],1],[[1,0,1],1],[[0,1,1],1],[[1,1,1],1]]
maj_pc.train(maj_tt)
'''
'''
print("PALINDROME")
pal_pc = Perceptron(3)
pal_tt = [[[0,0,0],1],[[0,0,1],0],[[0,1,0],1],[[1,0,0],0],
		[[1,1,0],0],[[1,0,1],1],[[0,1,1],0],[[1,1,1],1]]
pal_pc.train(pal_tt)
'''