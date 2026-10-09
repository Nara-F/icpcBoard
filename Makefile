PYTHON ?= python3

.PHONY: install validate markdown html pdf all clean
install:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/build.py --validate-only

markdown:
	$(PYTHON) scripts/build.py --format markdown

html:
	$(PYTHON) scripts/build.py --format html

pdf:
	$(PYTHON) scripts/build.py --format pdf

all:
	$(PYTHON) scripts/build.py --format all

clean:
	rm -f output/html/icpcBoard.html output/markdown/icpcBoard.md output/pdf/icpcBoard.pdf
