from arpabet_to_ipa import *
from arpabet_to_espeak import *

def create_output_from_array(arr,demarker = " "):
	pos = 1
	res_str = ""
	for ele in arr:
		res_str += str(ele)
		if(pos != len(arr)):
			res_str += demarker
		pos += 1
	return res_str

def load_from_command_line(command_input):
	function_type = ""
	function_param = []
	function_count = 0

	is_word = False
	train = False
	temp = False
	is_kfold = False

	if(len(command_input) <= 1):
		function_type = str(input("Function Type\n"))
	else:
		function_type = command_input[1]

	while(True):
		if(function_type == "-w"):
			is_word = True
			break
		if(function_type == "-Tw"):
			is_word = True
			temp = True
			break		
		elif(function_type == "-p"):
			break
		elif(function_type == "-t"):
			train = True
			break
		elif(function_type == "-k"):
			is_kfold = True
			train = True
			break
		if(function_type == "-Tp"):
			temp = True
			break
		else:
			function_type = str(input("Enter Valid Function Type\n"))
			break
	if(is_kfold):
		return [function_param,is_word, train, True, int(command_input[2])]
	if(train):
		return [function_param,is_word, train, temp, is_kfold]

	if(len(command_input) <= 2):
		function_count = int(input("Input Size\n"))
		for i in range(function_count):
			element = str(input("#"))
			function_param.append(element)
	else:
		function_param = command_input[2:]

	pos = 0
	for word in function_param:
		word = word.upper()
		function_param[pos] = word
		pos+=1

	return [function_param,is_word, train, temp,is_kfold]

def match_percent(l1,l2,confusion_matrix):
	temp_matched_count = 0.0
	for i in range(len(l1)):
		if(l1[i] == l2[i]):
			temp_matched_count += 1.0
		else:
			confusion_matrix[(l1[i],l2[i])] += 1
	
	temp_matched_count /= len(l1)
	return temp_matched_count

def convertToEspeak(arpabet):
	temp = []
	for x in arpabet:
		for y in conversion_espeak:
			if x == y[0]:
				temp.append(y[3])
				break
	
	return temp
def convertToIPA(arpabet):
	temp = []
	for x in arpabet:
		for y in conversion_espeak:
			if x == y[0]:
				temp.append(y[1])
				break
	
	return temp

def print_confusion_matrix(alphabet,matrix,filename="confusion_matrix.txt"):
	file_out = open(filename,"w")

	separator = "\t|"
	file_out.write("\\")
	string = separator
	for al in alphabet:
		file_out.write("," + al)
		string += al + separator
	print(string)
	file_out.write(";\n")
	
	string = ""
	for al in alphabet:
		string += "____"
	print(string)

	for a1 in alphabet:
		string = a1 + separator
		file_out.write(a1)
		i = 1
		for a2 in alphabet:
			if(matrix[(a1,a2)] > 0):
				string += str(matrix[(a1,a2)])
			
			file_out.write("," + str(matrix[(a1,a2)]))
			string += separator
		print(string)
		file_out.write(";\n")
