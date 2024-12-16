.PHONY: install test

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests