from learnt_circuits import *

input_circuit = open("circuit.txt")
circuit = input_circuit.read()
variable_count = 1
statements = []

facts = []

def convert_lst_to_string(lst):
	res = ""
	pos = 1
	for item in lst:
		res += str(item)
		if(pos != len(lst)):
			res += ","
			pos+=1
	return res

def create_statement(gate,lst,output):
	global statements
	statements.append(str(gate) +"([" +convert_lst_to_string(lst) +  "]," + str(output)+ ")")

class LogicGate(object):
	"""docstring for LogicGate"""
	def __init__(self,name=""):
		super(LogicGate, self).__init__()
		self.children = []
		self.name = name

	def printer(self,tabs=""):
		print(">> " + tabs + self.name)
		for kid in self.children:
			self.kid.printer(tabs + "  ")

	def isVariable(self):
		return (len(self.children)==0)

	def generate_code(self,output=0):
		output_str = ""
		if(output == 0):
			output_str = "O"
		else:
			output_str = "T" + str(output)
		
		global statements,variable_count

		statement_lst = []
		position = 0
		for kid in self.children:
			if(kid.isVariable()):
				statement_lst.append([-1,kid.name,position])
			else:
				statement_lst.append([variable_count,kid.name,position])
				variable_count += 1
			position += 1

		input_lst = []
		for stmt in statement_lst:
			if(stmt[0] == -1):
				input_lst.append(stmt[1])
			else:
				input_lst.append("T" + str(stmt[0]))
				self.children[stmt[2]].generate_code(stmt[0])

		create_statement(self.name,input_lst,output_str)				

	
identifier = ""
logic_gates = []
global_logic_gate = None
temporary_logic_gate = None
predicate_type = False


def handle_rejection():
	global logic_gates,temporary_logic_gate,global_logic_gate
	temporary_logic_gate = logic_gates.pop(len(logic_gates)-1)
	
	if(len(logic_gates) == 0):
		global_logic_gate = temporary_logic_gate
		return True
	
	logic_gates[len(logic_gates)-1].children.append(temporary_logic_gate)
	return False

def process_lhs(strng):
	str_split = strng.split("(")
	name = str_split[0]
	options = str_split[1].replace(")","")
	options = options.split(",")
	lhs_s = name.lower() + "(["
	for o in options:
		lhs_s += str(o)
		lhs_s += ","
	lhs_s = lhs_s[:-1]
	lhs_s += "], O)"
	return [name.lower(),lhs_s]

def process_rhs(strng):
	global logic_gates,temporary_logic_gate,global_logic_gate,identifier
	for c in strng:
		if(c == ","):
			if(predicate_type):
				if(handle_rejection()):
					break
			else:
				logic_gates[len(logic_gates)-1].children.append(LogicGate(identifier))
				identifier = ""	

		elif(c == "("):
			predicate_type = True
			temporary_logic_gate = LogicGate(identifier.lower())
			logic_gates.append(temporary_logic_gate)
			identifier = ""	

		elif(c == ")"):
			if(predicate_type):
				handle_rejection()
			else:			
				logic_gates[len(logic_gates)-1].children.append(LogicGate(identifier))
				identifier = ""	
				predicate_type = True

		else:
			identifier += c
			predicate_type = False

	handle_rejection()


circuit_sections = circuit.split("=")
lhs = process_lhs(circuit_sections[0])
process_rhs(circuit_sections[1])

if(global_logic_gate != None):
	global_logic_gate.generate_code()
	string_to_print = lhs[1]
	string_to_print += " :- "
	pos = 1
	for code in reversed(statements):
		string_to_print += code
		if(pos == len(statements)):
			string_to_print += "."
		else:
			string_to_print += " , "
		pos+=1

	to_continue = True
	if(lhs[0] in learnt.keys()):
		inp = str(input("circuit already exists, want to overwrite?"))
		if(inp != "y"):
			to_continue = False
		else:
			learnt[lhs[0]] = string_to_print	
	else:
		learnt[lhs[0]] = string_to_print

	if(to_continue):
		outfile = open("generated.pl","w")
		# for f in global_facts:
			# outfile.write(f + "\n")

		for key,value in learnt.items():
			outfile.write("verify(" + key + ",A,B):-" + key + "(A,B).\n")
			outfile.write(value +"\n")
		outfile.close()

	outfile = open("learnt_circuits.py","w")
	outfile.write("learnt = " + str(learnt))
	outfile.close()


