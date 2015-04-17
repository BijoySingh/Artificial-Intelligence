.phony: perceptron neural graph

perceptron:
	@python3 Perceptron.py

neural:
	@python3 Network.py

graph:
	@dot -Tps ${SRC} -o ${OUT}
	@evince ${OUT}

xor:
	@dot -Tps xor_perceptron.gv -o xor_perceptron.ps
	@evince xor_perceptron.ps
3_pal:
	@dot -Tps palindrome_perceptron.gv -o palindrome_perceptron.ps
	@evince palindrome_perceptron.ps
4_pal:
	@dot -Tps palindrome_4_perceptron.gv -o palindrome_4_perceptron.ps
	@evince palindrome_4_perceptron.ps
full_adder:
	@dot -Tps full_adder_perceptron.gv -o full_adder_perceptron.ps
	@evince full_adder_perceptron.ps

clean:
	rm -rf *.gv
	rm -rf *.ps
	rm -rf __pycache__