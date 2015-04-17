def read_file(p_filename,filename):
	phones_file = open(p_filename)
	start_symbol = "@"
	
	phones = [start_symbol]
	alphabets = [start_symbol]

	for line in phones_file:
		# line = to_ascii(line)
		line = line.strip()
		phones.append(line)
	phones_file.close()

	data_file = open(filename)
	data = []
	for line in data_file:
 		# line = to_ascii(line)
		line = line.strip()
		line_arr = line.split()
		word = line_arr[0]
		
		word_list = [start_symbol]
		phone_list = line_arr
		phone_list[0] = start_symbol
		for char in word:
			word_list.append(char)
			if(char not in alphabets):
				alphabets.append(char)

		if(len(word_list) == len(phone_list)):
			data.append((word_list,phone_list))

	data_file.close()

	return (phones,alphabets,data)

def create_string_key(a,b,c):
	return str(a) + "," + str(b) + "," + str(c)

def load_key(key):
	return key.split(",")