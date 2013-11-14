PYTHON = python
#SRCS = $(wildcard *.py)
SRCS = bndlearner.py main.py
MAIN = main.py
CLASSES = $(SRCS:.py=.pyc)
GOAL = learn
OUTFILE = results.txt

.PHONY: default clean

default: $(GOAL)

$(GOAL): $(SRCS)
	$(PYTHON) $(MAIN) > $(OUTFILE)
	cat $(OUTFILE)

clean:
	-rm -f $(CLASSES)
