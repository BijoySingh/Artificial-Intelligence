from Read import *
from Train import *
from Viterbi import *
from Functions import *
import sys
import pickle
import random

command_input  = sys.argv

filtered_file = "read_data.p"
trained_file = "trained_data.p"

cl_input = load_from_command_line(command_input)
function_param = cl_input[0]
is_word = cl_input[1]
train = cl_input[2]
temp = cl_input[3]
k_fold = cl_input[4]

if(k_fold != False):
	k_fold_cross_validation_sequence = []
	read_data = read_file("phonemes.txt","data.txt")
	random.shuffle(read_data[2])
	# read_data = (read_data[0],read_data[1],read_data[2][0:1000])
	data_size = len(read_data[2])	
	kfold_ratio = 1.0*data_size/k_fold

	for i in range(int(data_size/k_fold) + 1):
		if((i+1)*kfold_ratio > data_size):
			break
		k_fold_cross_validation_sequence.append([int(i*kfold_ratio), int((i+1)*kfold_ratio)])
	
	avg_kfold_word = 0.0
	avg_kfold_phoneme = 0.0
	avg_total_count = 0.0
	word_confusion_matrix = dict()
	phoneme_confusion_matrix = dict()

	for c1 in read_data[1]:
		for c2 in read_data[1]:
			word_confusion_matrix[(c1,c2)] = 0

	for c1 in read_data[0]:
		for c2 in read_data[0]:
			phoneme_confusion_matrix[(c1,c2)] = 0


	pos = 0.0
	for k_fold_item in k_fold_cross_validation_sequence:
		print("Evaluated " + str(pos*100.0/len(k_fold_cross_validation_sequence)) + "% ...")
		pos += 1
		
		train_data = train_from_data(read_data,k_fold_item)
		# print(k_fold_item)

		matched_count_word = 0.0
		matched_count_phoneme = 0.0
		total_count = 0.0
		for test_items in read_data[2][k_fold_item[0]:k_fold_item[1]]:
			total_count += 1.0
			viterbi_result = viterbi(train_data[0],read_data[0],test_items[0][1:])

			# print(test_items[0][1:])
			# print(viterbi_result)
			
			matched_count_word += match_percent(test_items[1][1:],viterbi_result[1][1:],phoneme_confusion_matrix)

			viterbi_result = viterbi(train_data[1],read_data[1],test_items[1][1:])

			matched_count_phoneme += match_percent(test_items[0][1:],viterbi_result[1][1:],word_confusion_matrix)			

		if(total_count != 0.0):
			avg_kfold_word += matched_count_word/total_count
			avg_kfold_phoneme += matched_count_phoneme/total_count
			avg_total_count += 1.0

	avg_kfold_word /= avg_total_count
	avg_kfold_phoneme /= avg_total_count

	print("Average Word Conversion Accuracy : " + str(avg_kfold_word))
	print("Average Phoneme Conversion Accuracy : " + str(avg_kfold_phoneme))
	print_confusion_matrix(read_data[1],word_confusion_matrix,"alphabet_cm.csv")
	print_confusion_matrix(read_data[0],phoneme_confusion_matrix,"phoneme_cm.csv")

else:
	if(train or temp):
		#phonemes, alphabets, data
		read_data = read_file("phonemes.txt","data.txt")
		#phoneme->phoneme alphabet->alphabet
		train_data = train_from_data(read_data)

	if(train):
		pickle.dump(read_data , open(filtered_file, "wb" ))
		pickle.dump(train_data , open(trained_file, "wb" ))
	elif(not temp):
		read_data = pickle.load( open( filtered_file, "rb" ) )
		train_data = pickle.load( open(trained_file, "rb" ) )

	#probability state_sequence
	if(is_word and not(train)):
		viterbi_result = viterbi(train_data[0], read_data[0], function_param)
		# viterbi_result = viterbi(train_data[0], read_data[0], "ABANTO")
		result_ipa = create_output_from_array(convertToIPA(viterbi_result[1][1:]),"")
		result_arpabet = create_output_from_array(viterbi_result[1][1:])
		# print("ARPAbet \t" + result_arpabet)
		# print("IPA \t\t" + result_ipa)
		print("[[" + result_ipa + "]]")
	elif (not(train)):
		viterbi_result = viterbi(train_data[1], read_data[1], function_param)
		# viterbi_result = viterbi(train_data[1], read_data[1], ["AH0","B","AH0","N","T","OW0"])
		result = create_output_from_array(viterbi_result[1][1:],"")
		print(result)

# input("exit>")
