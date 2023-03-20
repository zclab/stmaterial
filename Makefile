VERSION			= latest

LOCALSERVERUSER	= syf
LOCALSERVER		= zclab.net
LOCALSERVERPATH	= /Users/syf/Documents/www/docs/themes/stmaterial

PROJECTPATH   	= ./
SPHINXOPTS    	=
SPHINXBUILD   	= sphinx-build
SPHINXPROJ    	= ssdoc
SOURCEDIR     	= docs
BUILDDIR      	= docs/_build
TARGETDIR		= $(HOME)/Documents/www/docs/themes/stmaterial

all: build
build: html copy

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: 
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

pdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clear:
	@rm -rf "$(BUILDDIR)"

open: $(BUILDDIR)/html/index.html
	@open $<

gallery:
	@python docs/scripts/generate_link_images.py

copy:
	@if [ ! -d "$(TARGETDIR)" ]; then mkdir $(TARGETDIR); else rm -rf $(TARGETDIR)/*; fi
	@cp -r docs/_build/html/* $(TARGETDIR)

deploy: html
	@rsync -av --progress --delete "$(BUILDDIR)/html/" $(LOCALSERVERUSER)@$(LOCALSERVER):$(LOCALSERVERPATH)

.PHONY: help html all clear open pdf gallery copy build