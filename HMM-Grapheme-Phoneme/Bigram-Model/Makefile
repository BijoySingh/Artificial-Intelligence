.phony: all word phone train kfold speak

all:
	python3 Main.py -w W I L D C A T
	python3 Main.py -p W AY L D K AE T

speak:
	python3 Main.py -w U M B R E L L A | espeak -v en
word:
	python3 Main.py -w U M B R E L L A

phone:
	python3 Main.py -p W AY L D K AE T  | festival --tts

train:
	python3 Main.py -t

kfold:
	python3 Main.py -k 5

ui:
	python3 Application.py