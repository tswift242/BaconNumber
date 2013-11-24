PYTHON = python
PROJDIR = bndlearner
#SRCS = $(wildcard *.py)
MAIN = $(PROJDIR)/main.py
SRCS = $(PROJDIR)/bndlearner.py $(PROJDIR)/bndlexceptions.py $(PROJDIR)/pickle_method.py $(MAIN)
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
