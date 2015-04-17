from Perceptron import *
import copy
import math
class Network(object):
	"""docstring for Network"""

	def perceptron_array(self,size, input_size):
		dummy = []
		for i in range(size):
			p = Perceptron(input_size,True)
			dummy.append(p)
		return dummy

	def get_layer(self,pid):
		layer_count = 0
		for length in self.length_sequence:
			if(pid < length):
				return (layer_count,pid)
			layer_count += 1
			pid -= length

	def get_layer_range(self, layer):
		count = 0
		layer_count = 0
		layer_range = []
		for length in self.length_sequence:
			if(layer_count == layer):
				temp_length = 0
				while(temp_length != length):
					layer_range.append(count + temp_length)
					temp_length += 1
				return layer_range
			count += length
			layer_count += 1

	def __init__(self, length_sequence,input_size,eta,threshold):
		super(Network, self).__init__()
		self.length_sequence = length_sequence
		self.network = []
		self.current_target = []
		self.deltas = []
		prev_length = input_size

		for length in length_sequence:
			self.network.append(self.perceptron_array(length,prev_length))
			for i in range(length):
				self.deltas.append(0)
			prev_length = length

		self.eta = eta
		self.threshold = threshold

	def evaluate_network(self, input_sequence, layer, mode=0):
		if(layer == len(self.network)):
			return input_sequence

		new_input_sequence = []
		input_sequence.append(-1)
		for perceptron in self.network[layer]:

			perceptron.process_input(input_sequence,mode)
			new_input_sequence.append(perceptron.output)

		return self.evaluate_network(new_input_sequence,layer+1,mode)

	def calculate_error(self,target,output):
		del_sum = 0
		for i in range(len(target)):
			del_sum += (target[i] - output[i])*(target[i] - output[i])
		return (0.5)*del_sum
		# for i in range(len(target)):
		# 	if(math.fabs(target[i] - output[i]) > self.threshold):
		# 		return True
		# return False

	def get_output(self,input_sequence,threshold):
		output = self.evaluate_network(input_sequence,0,0)
		final_out = []
		for o in  output:
			if(o < threshold):
				o = 0
			elif(o > 1 - threshold):
				o = 1
			else:
				o = 0.5
			final_out.append(o)
		return final_out

	def calculate_delta(self,pid,layer):
		# print("Calculating Delta " + str(self.deltas) + " for " + str(pid))
		if(self.deltas[pid] != -1):
			return self.deltas[pid]

		perceptron_pos = self.get_layer(pid)
		perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
		oj = perceptron.output

		if(layer == len(self.length_sequence)-1):
			tj = self.current_target[perceptron_pos[1]]
			self.deltas[pid] = (tj - oj)*oj*(1 - oj)
			return self.deltas[pid]

		res_sum = 0
		for k in self.get_layer_range(layer+1):
			perceptron_pos_k = self.get_layer(k)
			perceptron_k = self.network[perceptron_pos_k[0]][perceptron_pos_k[1]]
			wkj = perceptron_k.weights[perceptron_pos[1]]
			delta_k = self.calculate_delta(k,layer+1)
			res_sum += (wkj*delta_k)*oj*(1-oj)
		self.deltas[pid] = res_sum
		return res_sum

	def update_neuron(self,pid,pos,value):
		perceptron_pos = self.get_layer(pid)
		if(pos == -1):
			length = len(self.network[perceptron_pos[0]][perceptron_pos[1]].weights)
			pos = length - 1

		self.network[perceptron_pos[0]][perceptron_pos[1]].weights[pos] += value
		# print("Updated Perceptron " + str(self.network[perceptron_pos[0]][perceptron_pos[1]].weights))

	def train_network(self,truth_table):
		# truth_table = modifyTT(truth_table)
		pain = True
		progress = 0
		while (pain):
			pain = False
			for row in truth_table:
				# print("Row" + str(row))
				# print(progress)
				progress += 1
				tmp_row = copy.deepcopy(row)
				current_output = self.evaluate_network(tmp_row[0],0)

				error = self.calculate_error(tmp_row[1],current_output)
				# print(error)
				if(error < self.threshold):
					continue
				# if(error == False):
				# 	continue

				pain = True
				self.current_target = row[1]

				for i in range(len(self.deltas)):
					self.deltas[i] = -1
				
				# print("Starting Training")

				for i in range(-1,len(row[0])):
					for j in self.get_layer_range(0):
						oi = -1
						if(i != -1):
							oi = row[0][i]
						delta_w_ji = self.eta*oi*self.calculate_delta(j,0)
						self.update_neuron(j,i,delta_w_ji)

				for layer_id in range(len(self.length_sequence)-1):
					# print("Training : " + str(layer_id))

					for i in (self.get_layer_range(layer_id)+[-1]):
						for j in self.get_layer_range(layer_id+1):
							# print("Doing Perceptron : " + str(i) + "," + str(j))
							oi = -1
							perceptron_pos = []
							if(i != -1):
								perceptron_pos = self.get_layer(i)
								perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
								oi = perceptron.output

							delta_w_ji = self.eta*oi*self.calculate_delta(j,layer_id+1)
							
							if(i == -1):
								self.update_neuron(j,-1,delta_w_ji)
							else:
								self.update_neuron(j,perceptron_pos[1],delta_w_ji)

				break

		print("Perceptron")
		for layer in self.network:
			for pcptrn in layer:
				print(pcptrn.weights)

	def generate_network(self,filename):
		file_out = open(filename + ".gv","w")
		file_out.write("digraph " + filename + " {\n")
		file_out.write("graph [ordering=\"out\"];\n")
		file_out.write("graph [ordering=\"out\"];\n")
		round_amount = 2
		# Scheduling -> LongTermNode [label = " can be "]
		for layer_id in range(-1,len(self.length_sequence)-1):
			if(layer_id == -1):
				for i in (self.get_layer_range(0)):
					pos = 0
					perceptron_pos = self.get_layer(i)
					perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
					for w in perceptron.weights:
						if(pos == len(perceptron.weights) - 1):
							file_out.write("t_" + str(i) + " -> " + "p_" + str(i))
							file_out.write("[label = \"" + str(round(w,round_amount)) + "\"];\n")
							file_out.write("{ rank=same; " +  "t_" + str(i) + "; " + "p_" + str(i) + "; }\n")
						else:
							file_out.write("x_" + str(pos) + " -> " + "p_" + str(i))
							file_out.write("[label = \"" + str(round(w,round_amount)) + "\"];\n")
						pos += 1
			else:
				for i in (self.get_layer_range(layer_id+1)):
					perceptron_pos = self.get_layer(i)
					perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
					pos = 0
					for j in self.get_layer_range(layer_id):							
						file_out.write("p_" + str(j) + " -> " + "p_" + str(i))
						file_out.write("[label = \"" + str(round(perceptron.weights[pos],round_amount)) + "\"];\n")
						pos += 1
					
					file_out.write("t_" + str(i) + " -> " + "p_" + str(i))
					file_out.write("[label = \"" + str(round(perceptron.weights[pos],round_amount)) + "\"];\n")
					file_out.write("{ rank=same; " +  "t_" + str(i) + "; " + "p_" + str(i) + "; }\n")
						
		file_out.write("}")
		file_out.close()	
				

def test_network(network, truth_table,threshold=0.5):	
	for inp in truth_table:
		print(str(inp[0]) + " >> " + str(network.get_output(inp[0],threshold)) + " :: " + str(inp[1]))

eta = 0.1
do_array = [1,1,1,1]
strictness = 0.4
accuracy_required = (strictness*strictness)/2.0
accuracy = accuracy_required

print("Strictness : "+ str(strictness))
print("Guarantee Accuracy : " + str(accuracy_required))
print("Given Accuracy : " + str(accuracy) + "\n")

if(do_array[0] == 1):
	network_xor = Network([2,1],2,eta,accuracy)
	xor_truth_table = [[[0,0],[0]],[[0,1],[1]],[[1,0],[1]],[[1,1],[0]]]
	network_xor.train_network(xor_truth_table)
	test_network(network_xor,xor_truth_table,strictness)
	network_xor.generate_network("xor_perceptron")

if(do_array[1] == 1):
	network_palindrome = Network([2,1],3,eta,accuracy)
	palindrome_truth_table = [[[0,0,0],[1]],[[0,0,1],[0]],[[0,1,0],[1]],[[1,0,0],[0]],
			[[1,1,0],[0]],[[1,0,1],[1]],[[0,1,1],[0]],[[1,1,1],[1]]]
	network_palindrome.train_network(palindrome_truth_table)
	test_network(network_palindrome,palindrome_truth_table,strictness)
	network_palindrome.generate_network("palindrome_perceptron")

if(do_array[2] == 1):
	network_palindrome_4 = Network([3,1],3,eta,accuracy)
	palindrome_4_truth_table = [[[0,0,0,0],[1]],[[0,0,0,1],[0]],[[0,0,1,0],[0]],[[0,1,0,0],[0]],
			[[0,1,1,0],[1]],[[0,1,0,1],[0]],[[0,0,1,1],[0]],[[0,1,1,1],[0]],
			[[1,0,0,0],[0]],[[1,0,0,1],[1]],[[1,0,1,0],[0]],[[1,1,0,0],[0]],
			[[1,1,1,0],[0]],[[1,1,0,1],[0]],[[1,0,1,1],[0]],[[1,1,1,1],[1]]]
	network_palindrome_4.train_network(palindrome_4_truth_table)
	test_network(network_palindrome_4,palindrome_4_truth_table,strictness)
	network_palindrome_4.generate_network("palindrome_4_perceptron")

if(do_array[3] == 1):
	network_full_adder = Network([2,2],3,eta,accuracy)
	full_adder_truth_table = [[[0,0,0],[0,0]],[[0,0,1],[0,1]],[[0,1,0],[0,1]],[[1,0,0],[0,1]],
			[[1,1,0],[1,0]],[[1,0,1],[1,0]],[[0,1,1],[1,0]],[[1,1,1],[1,1]]]
	network_full_adder.train_network(full_adder_truth_table)
	test_network(network_full_adder,full_adder_truth_table,strictness)
	network_full_adder.generate_network("full_adder_perceptron")

