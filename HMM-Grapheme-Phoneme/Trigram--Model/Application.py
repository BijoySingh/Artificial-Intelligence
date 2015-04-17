from Read import *
from Train import *
from Viterbi import *
from Functions import *
import tkinter as tk
import pickle
import random
from subprocess import call
'''
class for managing the information Tkinter Window
'''
'''
The core application Gui
'''


class Application(tk.Frame):	

	canvas_width= 400
	canvas_height = 150
	def_background = "#f1f1f1"
	def_button_background = "#dddddd"
	def_color = "#000000"
	def_button_color = "#000000"

	result_word = ""
	result_phoneme_ipa = ""
	result_phoneme_arpabet = ""
	result_phoneme_espeak = ""

	filtered_file = "read_data.p"
	trained_file = "trained_data.p"

	def load_data(self):
		self.read_data = pickle.load( open( self.filtered_file, "rb" ) )
		self.train_data = pickle.load( open(self.trained_file, "rb" ) )


	def __init__(self, master=None):
		tk.Frame.__init__(self, master,background=self.def_background)
		self.pack()
		self.create_widgets()
		self.load_data()

	'''
	creates the buttons and panels
	'''
	def create_widgets(self):
		'''Top Frame'''

		self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
		self.canvas.pack(pady="1")

		self.frame_top = tk.Frame(self,background=self.def_background)

		self.word = tk.Entry(self.frame_top,bd="0.0")
		self.word.pack(side="left",padx="5")
		self.word.insert(0,"Wildcat")

		self.to_phoneme= tk.Button(self.frame_top,bg=self.def_button_background,fg=self.def_button_color,bd="0.0",padx="10",pady="5")
		self.to_phoneme["text"] = "CONVERT"
		self.to_phoneme["command"] = self.convert_word
		self.to_phoneme.pack(side="left",padx="5")


		self.phoneme = tk.Entry(self.frame_top,bd="0.0")
		self.phoneme.pack(side="left",padx="5")
		self.phoneme.insert(0,"")

		self.to_word= tk.Button(self.frame_top,bg=self.def_button_background,fg=self.def_button_color,bd="0.0",padx="10",pady="5")
		self.to_word["text"] = "CONVERT"
		self.to_word["command"] = self.convert_phoneme
		self.to_word.pack(side="left",padx="5")

		self.to_espeak= tk.Button(self.frame_top,bg=self.def_button_background,fg=self.def_button_color,bd="0.0",padx="10",pady="5")
		self.to_espeak["text"] = "ESPEAK"
		self.to_espeak["command"] = self.espeak
		self.to_espeak.pack(side="left",padx="5")
		self.create_graph()

		self.frame_top.pack(pady="1")
		self.frame_bottom = tk.Frame(self,background=self.def_background)
		self.sentence = tk.Entry(self.frame_bottom,bd="0.0")
		self.sentence.pack(side="left",padx="5")
		self.sentence.insert(0,"")

		self.convert_sentence= tk.Button(self.frame_bottom,bg=self.def_button_background,fg=self.def_button_color,bd="0.0",padx="10",pady="5")
		self.convert_sentence["text"] = "SPEAK"
		self.convert_sentence["command"] = self.convert_sentence_espeak
		self.convert_sentence.pack(side="left",padx="5")
		self.frame_bottom.pack(pady="1")


	def create_graph(self):
		'''Resetting the canvas background'''
		self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height,fill="#ffffff",width="0.0")
		
		# self.canvas.create_line(i*self.scale_factor,0,i*self.scale_factor,self.canvas_height,fill="#eeeeee")
		self.canvas.create_text(100,50,text="WORD",fill="#aaaaaa")
		self.canvas.create_text(100,65,text=str(self.result_word),fill="#666666")
		
		self.canvas.create_text(250,10,text="ARPAbet",fill="#aaaaaa")
		self.canvas.create_text(250,25,text=str(self.result_phoneme_arpabet),fill="#666666")

		self.canvas.create_text(250,50,text="IPA",fill="#aaaaaa")
		self.canvas.create_text(250,65,text=str(self.result_phoneme_ipa),fill="#666666")

		self.canvas.create_text(250,100,text="eSpeak",fill="#aaaaaa")
		self.canvas.create_text(250,115,text=str(self.result_phoneme_espeak),fill="#666666")
		
		return

	def convert_word(self):
		value = self.word.get()
		value = value.upper()
		value_l = []
		for char in value:
			value_l.append(char)

		self.result_word = create_output_from_array(value_l)
		viterbi_result = viterbi(self.train_data[0], self.read_data[0], value_l)
		self.result_phoneme_ipa = create_output_from_array(convertToIPA(viterbi_result[1][1:]),"")
		self.result_phoneme_arpabet = create_output_from_array(viterbi_result[1][1:])
		self.result_phoneme_espeak = create_output_from_array(convertToEspeak(viterbi_result[1][1:]),"")
		self.create_graph()
		return

	def convert_sentence_espeak(self):
		value = self.sentence.get()
		value = value.upper()
		value_arr = value.split(" ")
		espeak_result = ""
		for word in value_arr:
			value_l = []
			for char in word:
				value_l.append(char)
			self.result_word = create_output_from_array(value_l)
			viterbi_result = viterbi(self.train_data[0], self.read_data[0], value_l)
			espeak_result += create_output_from_array(convertToEspeak(viterbi_result[1][1:]),"") + " "
		call(["espeak", "[[" + espeak_result + "]]"])
		return	

	def convert_phoneme(self):
		value = self.phoneme.get()
		self.result_phoneme_arpabet = value
		value = value.split(" ")
		self.result_phoneme_espeak = ""
		self.result_phoneme_ipa = ""
		viterbi_result = viterbi(self.train_data[1], self.read_data[1], value)
		self.result_word = create_output_from_array(viterbi_result[1][1:],"")
		self.create_graph()
		return

	def espeak(self):
		value = self.result_phoneme_espeak
		call(["espeak","[[" + value + "]]"])
		self.create_graph()
		return



class Gui:
	root = tk.Tk() 
	app = None
	node_info = None
	def __init__(self):
		rt = self.root
		self.app = Application(master=rt)

	def start(self):
		self.app.mainloop()

gui = Gui()
gui.start()
