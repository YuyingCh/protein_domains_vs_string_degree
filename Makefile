all : boxplot.png
.PHONY : all

## download : download protein files from the links provided
downloads/*.txt : FORCE
	mkdir downloads
	cd downloads
	wget https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz
	gunzip 9606.protein.links.v11.0.txt.gz
	wget -L https://stockholmuniversity.box.com/shared/static/n8l0l1b3tg32wrzg2ensg8dnt7oua8ex -O proteins_w_domains.txt
FORCE :

## boxplot.png : create conda environment, analyse and plot the result
.ONESHELL:
SHELL = /usr/bin/bash
boxplot.png : downloads/*.txt environment.yml network.py
	conda env create -f environment.yml
	source $$(conda info --base)/etc/profile.d/conda.sh
	conda activate networkAnalysis
	python network.py

## clean : remove downloads and the generated plots
.PHONY : clean
clean :
	rm -f boxplot.png
	rm -rf downloads

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
