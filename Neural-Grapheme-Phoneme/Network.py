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

	def get_perceptron_position(self,pid):
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
			# del_sum += (0.5)*(target[i] - output[i])*(target[i] - output[i])
			# del_sum += math.fabs(target[i] - output[i])
			if(math.fabs(target[i] - output[i]) > self.threshold):
				del_sum += 1

		if(del_sum > 0.01*len(target)):
			return True
		# error = del_sum
		# print(error)
		# if(error < len(target)*self.threshold/2):
		return False
		# return True
		

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

		perceptron_pos = self.get_perceptron_position(pid)
		perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
		oj = perceptron.output

		if(layer == len(self.length_sequence)-1):
			tj = self.current_target[perceptron_pos[1]]
			self.deltas[pid] = (tj - oj)*oj*(1 - oj)
			return self.deltas[pid]

		res_sum = 0
		for k in self.get_layer_range(layer+1):
			perceptron_pos_k = self.get_perceptron_position(k)
			perceptron_k = self.network[perceptron_pos_k[0]][perceptron_pos_k[1]]
			wkj = perceptron_k.weights[perceptron_pos[1]]
			delta_k = self.calculate_delta(k,layer+1)
			res_sum += (wkj*delta_k)*oj*(1-oj)
		self.deltas[pid] = res_sum
		return res_sum

	def update_neuron(self,pid,pos,value):
		perceptron_pos = self.get_perceptron_position(pid)
		if(pos == -1):
			length = len(self.network[perceptron_pos[0]][perceptron_pos[1]].weights)
			pos = length - 1

		self.network[perceptron_pos[0]][perceptron_pos[1]].weights[pos] += value
		# print("Updated Perceptron " + str(self.network[perceptron_pos[0]][perceptron_pos[1]].weights))

	def train_network(self,truth_table,redo_count=100):
		# truth_table = modifyTT(truth_table)
		rounds = 0
		max_round = redo_count
		progress = 0
		pain = True
		while (rounds < max_round and pain):
		# while (pain):
			pain = False
			print(str(round(rounds*10000/max_round)/100.0) + "% Done..")
			rounds += 1;
			row_count = 0
			last_row_count = 0
			for row in truth_table:
				row_count += 1
				# print(row_count)
				
				if(row_count - last_row_count > round(0.2*len(truth_table))):
					# print("\t" + str(round(row_count*100/len(truth_table))) + "% ...processed")
					last_row_count = row_count
				

				# print("Row" + str(row))
				# print(progress)
				progress += 1
				tmp_row = copy.deepcopy(row)
				current_output = self.evaluate_network(tmp_row[0],0)

				error = self.calculate_error(tmp_row[1],current_output)
				# print(error)
				# if(error < self.threshold):
					# continue
				if(error == False):
					continue

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
								perceptron_pos = self.get_perceptron_position(i)
								perceptron = self.network[perceptron_pos[0]][perceptron_pos[1]]
								oi = perceptron.output

							delta_w_ji = self.eta*oi*self.calculate_delta(j,layer_id+1)
							
							if(i == -1):
								self.update_neuron(j,-1,delta_w_ji)
							else:
								self.update_neuron(j,perceptron_pos[1],delta_w_ji)				
		'''
		print("Perceptron")
		for layer in self.network:
			for pcptrn in layer:
				print(pcptrn.weights)
		'''

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
					perceptron_pos = self.get_perceptron_position(i)
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
					perceptron_pos = self.get_perceptron_position(i)
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
				