.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python3 code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python3 code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log



# ----------------------------------------------------------------------------------------------------------------
#
#Answer these questions (write the answers in a comment at the bottom of your Makefile or in a separate text file):
#
# 1. If you edit code/preprocess.py, which targets will Make rebuild? Which targets will it skip?
#    - Make will rebuild the figures (figure_5_2.png and figure_5_3.png)
#    - Then it will rebuild paper/paper.pdf
#    - It will NOT rebuild did_table.tex
#
# 2. If you edit code/did_analysis.py, which targets will Make rebuild? Which targets will it skip?
#    - Make will rebuild did_table.tex
#    - Then it will rebuild paper/paper.pdf
#    - It will NOT rerun preprocess.py
#
# 3. If you edit paper/paper.tex, which targets will Make rebuild? Which targets will it skip?
#    - Make will only rebuild paper/paper.pdf
#    - No Python scripts will run
#
# ---------------------------------------------------------------------------------------------------------------
