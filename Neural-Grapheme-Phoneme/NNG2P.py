from Read import *
from math import log
from Network import *
import random
import sys
import pickle


read_data_file = "read_data.p"
phone_map_file = "phone_map.p"
graph_map_file = "graph_map.p"
neural_network_file = "neural_network.p"

def get_command(command_input,command):
	for i in range(len(command_input)):
		if(command_input[i] == command):
			return int(command_input[i+1])

max_length = 10
train_size = 100
test_size = 50
force_length = False
load_from_pickle_file = False
redo_count = 100
reuse_neural_network = False
kfold_verification = False

command_input  = sys.argv

if("-f" in command_input):
	force_length = True
if("-k" in command_input):
	kfold_verification = True
if("-n" in command_input):
	reuse_neural_network = True
if("-T" in command_input):
	load_from_pickle_file = False
if("-l" in command_input):
	max_length = get_command(command_input,"-l")
if("-t" in command_input):
	train_size = get_command(command_input,"-t")
if("-s" in command_input):
	test_size = get_command(command_input,"-s")
if("-r" in command_input):
	redo_count = get_command(command_input,"-r")

def zero_arr(size):
	return [0 for _ in range(size)]

def generateMap(lis):
	bitLen = (int)(log(len(lis), 2)) + 1
	bitMap = {}
	backMap = {}
	for i in range(len(lis)):
		bitMap[lis[i]] = genBitString(i + 1, bitLen)
		backMap[str(bitMap[lis[i]])] = lis[i]
	return (bitMap, backMap, bitLen)

def genBitString(num, length):
	bitStr = [0 for _ in range(length)]
	i = 0
	while (num >= 1):
		#print(str(i) + " " + str(length) + " " + str(num))
		r = num % 2
		bitStr[i] = r
		i = i + 1
		num = (int) (num / 2)	
	return bitStr

def convertToBits(word_lst,bitmap,max_length,bit_size):
	conversion = []
	for w in word_lst:
		conversion += bitmap[w]
	zero_append = zero_arr(max_length*bit_size - len(conversion))
	conversion += zero_append
	return conversion

read_data = [[],[],[]]
PhoneMaps = [[],[],[]]
GraphMaps = [[],[],[]]

def write_to_file():
	global read_data, PhoneMaps, GraphMaps
	pickle.dump(read_data,open(read_data_file, "wb"))
	pickle.dump(PhoneMaps,open(phone_map_file, "wb"))
	pickle.dump(GraphMaps,open(graph_map_file, "wb"))

def load_data():
	global read_data, PhoneMaps, GraphMaps
	read_data = read_file("phonemes.txt","data.txt")
	random.shuffle(read_data[0])
	random.shuffle(read_data[1])
	random.shuffle(read_data[2])
	PhoneMaps = generateMap(read_data[0])
	GraphMaps = generateMap(read_data[1])


def load_from_file():
	global read_data, PhoneMaps, GraphMaps
	read_data = pickle.load(open( read_data_file, "rb" ))
	PhoneMaps = pickle.load(open( phone_map_file, "rb" ))
	GraphMaps = pickle.load(open( graph_map_file, "rb" ))

if(load_from_pickle_file):
	load_from_file()
else:
	load_data()
	write_to_file()

phone2bit = PhoneMaps[0]
bit2phone = PhoneMaps[1]
phone_bit_size = PhoneMaps[2]

graph2bit = GraphMaps[0]
bit2graph = GraphMaps[1]
graph_bit_size = GraphMaps[2]

'''
for d in read_data[2]:
	if(len(d[0]) > max_length):
		max_length = len(d[0])
'''

#GRAPHEME TO PHONEME
input_length = max_length*graph_bit_size
output_length = max_length*phone_bit_size

grapheme_to_phoneme_in_bits = []
phoneme_to_grapheme_in_bits = []

for d in read_data[2]:
	if(len(d[0]) > max_length or (force_length and len(d[0]) != max_length)):
		continue
	grapheme = convertToBits(d[0],graph2bit,max_length,graph_bit_size)
	phoneme = convertToBits(d[1],phone2bit,max_length,phone_bit_size)
	grapheme_to_phoneme_in_bits.append([grapheme,phoneme])
	grapheme_to_phoneme_in_bits.append([phoneme,grapheme])

def club(lst,bitsize):
	output = []
	i = 0
	word = []
	for w in lst:
		word .append(w)
		i += 1
		if(i == bitsize):
			output.append(word)
			word = []
			i = 0
	# print(output)
	return output

def test_network(network, truth_table,test_size,input_bit_size,output_bit_size,threshold=0.5,filename="testout.out"):	
	filen = open(filename,"w")
	random.shuffle(truth_table)
	random_sample = truth_table[:test_size]	
	
	correct_count = 0
	total_count = 0

	correct_bits_count = 0
	total_bits_count = 0
	
	for inp in random_sample:
		unclubbed_out = network.get_output(inp[0],threshold)
		for i in range(len(inp[1])):
			if(inp[1][i] == unclubbed_out[i]):
				correct_bits_count += 1
			total_bits_count += 1

		tinput = club(inp[0],input_bit_size)
		toutput = club(unclubbed_out,output_bit_size)
		tdesired = club(inp[1],output_bit_size)

		ti = []
		to = []
		tp = []

		for x in tinput:
			if(str(x) in bit2graph.keys()):
				ti.append(bit2graph[str(x)])
			# else:
				# ti.append("_")

		for x in toutput:
			if(str(x) in bit2phone.keys()):
				to.append(bit2phone[str(x)])
			else:
				to.append("-")

		for x in tdesired:
			if(str(x) in bit2phone.keys()):
				tp.append(bit2phone[str(x)])
			else:
				tp.append("_")

		for i in range(len(to)):
			if(to[i] == tp[i]):
				correct_count += 1
			total_count += 1


		# filen.write(str(ti))
		# filen.write("\n")
		filen.write(str(to))
		filen.write("\n")
		filen.write(str(tp))
		filen.write("\n")
		filen.write("_________________________")
		filen.write("\n")
	filen.write("ACCURACY :: " + str(100*correct_count/total_count) +  "\n")
	filen.write("BIT ACCURACY :: " + str(100*correct_bits_count/total_bits_count) +  "\n")
	print("ACCURACY :: " + str(100*correct_count/total_count))
	print("BIT ACCURACY :: " + str(100*correct_bits_count/total_bits_count))
	
table_to_test = grapheme_to_phoneme_in_bits	
inner_layer_length = max_length
outer_layer_length = output_length
input_layer_length = input_length

'''
table_to_test = phoneme_to_grapheme_in_bits
inner_layer_length = max_length
outer_layer_length = input_length
input_layer_length = output_length
'''

if(train_size > len(grapheme_to_phoneme_in_bits)):
	print("Over Demand")
	train_size = len(grapheme_to_phoneme_in_bits)

eta = 0.1
accuracy = 0.1
network = None

truth_table = []
test_table = []

if(kfold_verification):
	train_size = round((len(grapheme_to_phoneme_in_bits)*4)/5)
	truth_table = table_to_test[:train_size]
	test_table = table_to_test[train_size:]
	truth_table.append([zero_arr(input_length),zero_arr(output_length)])
else:
	truth_table = table_to_test[:train_size]
	test_table = truth_table
	truth_table.append([zero_arr(input_length),zero_arr(output_length)])

if(reuse_neural_network):
	network = pickle.load(open(neural_network_file, "rb" ))
else:
	network = Network([inner_layer_length,outer_layer_length],input_layer_length,eta,accuracy)
	network.train_network(truth_table,redo_count)
	pickle.dump(network,open(neural_network_file, "wb"))

test_network(network,test_table,test_size,graph_bit_size,phone_bit_size)
# test_network(network,test_table,test_size,phone_bit_size,graph_bit_size)


