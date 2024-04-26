all: requirements.txt
	echo ok

venv:
	python3 -m venv .venv
	. .venv/bin/activate
	pip3 install -r requirements.txt

requirements.txt:
	pip3 install -r requirements.txt
