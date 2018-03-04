#
# Author: Jake Zimmerman <jake@zimmerman.io>
# Modified-by: William Woodruff <william@yossarian.net>
#
# ===== Usage ================================================================
#
# NOTE:
#   When running these commands at the command line, replace $(TARGET) with
#   the actual value of the TARGET variable.
#
#
# make                  Compile all *.md files to PDFs
# make <filename>.pdf   Compile <filename>.md to a PDF
# make <filename>.tex   Generate the intermediate LaTeX for <filename>.md
#
# make view             Compile $(TARGET).md to a PDF, then view it
# make again            Force everything to recompile
#
# make clean            Get rid of all intermediate generated files
# make veryclean        Get rid of ALL generated files:
#
# make print            Send $(TARGET).pdf to the default printer:
#
# make live             View and rebuild $(TARGET).md as it changes
# ============================================================================

SHELL=/bin/bash
TARGET=fpff_spec

all: $(patsubst %.md,%.pdf,$(wildcard *.md))

PANDOC_FLAGS =\
	-f markdown+tex_math_single_backslash \
	-t latex \
	--variable urlcolor=blue

all: $(patsubst %.md,%.pdf,$(wildcard *.md))

# Generalized rule: how to build a .pdf from each .md
%.pdf: %.md
	pandoc $(PANDOC_FLAGS) $(LATEX_FLAGS) -o $@ $<

# Generalized rule: how to build a .tex from each .md
%.tex: %.md
	pandoc --standalone $(PANDOC_FLAGS) -o $@ $<

touch:
	touch *.md

again: touch all

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb || true

veryclean: clean
	rm -f *.pdf

view: $(TARGET).pdf
	if [ "Darwin" = "$(shell uname)" ]; then open $(TARGET).pdf ; else mupdf $(TARGET).pdf ; fi

print: $(TARGET).pdf
	lpr $(TARGET).pdf

live:
	make view &
	entr -c make $(TARGET).pdf <<< "$(TARGET).md"

.PHONY: all again touch clean veryclean view print live-dev
