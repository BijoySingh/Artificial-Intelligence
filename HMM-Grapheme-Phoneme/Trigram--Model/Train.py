def train_from_data(read_data,k_fold=False):
	phones = read_data[0]
	alphabets = read_data[1]
	data = read_data[2]
	empty_probability = 0.00000000001
	
	'''
	print("PHONEME SIZE >> " + str(len(phones)))
	print("ALPHABET SIZE >> " + str(len(alphabets)))
	print("DATA SIZE >> " + str(len(data)))
	'''

	alphabet_transition = dict()
	phoneme_transition = dict()
	alphabet_start_symbol = dict()
	phoneme_start_symbol = dict()

	for a1 in alphabets:
		for a2 in alphabets:
			for a3 in alphabets:
				for p in phones:
					alphabet_transition[(a1,a2,a3,p)] = empty_probability

	for p1 in phones:
		for p2 in phones:
			for p3 in phones:
				for a in alphabets:
					phoneme_transition[(p1,p2,p3,a)] = empty_probability

	for p1 in phones:
		for p2 in phones:
			phoneme_start_symbol[(p1,p2)] = 0

	for a1 in alphabets:
		for a2 in alphabets:
			alphabet_start_symbol[(a1,a2)] = 0

	if(k_fold == False):
		k_fold = [-1,-1]
	
	data_pos = -1
	for item in data:

		data_pos += 1
		if(data_pos >= k_fold[0] and data_pos < k_fold[1]):
			continue

		#data is (word,sound)
		word = item[0]
		sound = item[1]

		word_pos = 1
		while(word_pos < len(sound)-1):
			alphabet_transition_tuple = (word[word_pos-1],word[word_pos],word[word_pos+1],sound[word_pos+1])
			# print(alphabet_transition_tuple)
			phoneme_transition_tuple = (sound[word_pos-1],sound[word_pos],sound[word_pos+1],word[word_pos+1])
			
			word_current_state = (word[word_pos-1],word[word_pos])
			sound_current_state = (sound[word_pos-1],sound[word_pos])

			alphabet_transition[alphabet_transition_tuple] = (alphabet_transition[alphabet_transition_tuple]*alphabet_start_symbol[word_current_state] + 1)/(alphabet_start_symbol[word_current_state]+1)

			phoneme_transition[phoneme_transition_tuple] = (phoneme_transition[phoneme_transition_tuple]*phoneme_start_symbol[sound_current_state] + 1)/(phoneme_start_symbol[sound_current_state] + 1)

			alphabet_start_symbol[word_current_state] +=1
			phoneme_start_symbol[sound_current_state] +=1

			word_pos += 1
		
	# print(alphabet_transition)
	return (phoneme_transition,alphabet_transition)


