# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build
RELEASE       = v0.5

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

DOCREPONAME = pyne.github.com
DOCREPOURL  = https://github.com/pyne/pyne.github.com

.PHONY: help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest

all: html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  dirhtml   to make HTML files named index.html in directories"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  qthelp    to make HTML files and a qthelp project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  doctest   to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR) build_nuc_data rxname_listing

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	doxygen Doxyfile
	find _build/html/tutorial/ -type f -exec sed -i -e 's/container{width:[0-9]*px}/container{width:95%}/g' {} \;
	find _build/html/examples/ -type f -exec sed -i -e 's/container{width:[0-9]*px}/container{width:95%}/g' {} \;
	echo "pyne.io" > $(BUILDDIR)/html/CNAME
	touch $(BUILDDIR)/html/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/metasci.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/metasci.qhc"

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

push-latest:
	cd $(BUILDDIR) && \
	test -d $(DOCREPONAME) || git clone $(DOCREPOURL) $(DOCREPONAME) && \
	cd $(DOCREPONAME) && \
	git pull origin master && \
	rm -rf latest && \
	mkdir latest && touch latest/_ && \
	cp -r ../html/* latest/ && \
	git add latest/ && \
	git commit -am "Pushed latest docs at $$(date)" && \
	git push

push-release:
	cd $(BUILDDIR) && \
	test -d $(DOCREPONAME) || git clone $(DOCREPOURL) $(DOCREPONAME) && \
	cd $(DOCREPONAME) && \
	git pull origin master && \
	rm -rf $(RELEASE) && \
	mkdir $(RELEASE) && touch $(RELEASE)/_ && \
	cp -r ../html/* $(RELEASE)/ && \
	git add $(RELEASE)/ && \
	git commit -am "Pushed $(RELEASE) docs at $$(date)" && \
	git push

push-test:
	cd $(BUILDDIR) && \
	test -d $(DOCREPONAME) || git clone $(DOCREPOURL) $(DOCREPONAME) && \
	cd $(DOCREPONAME) && \
	git checkout -b website_preview origin/website_preview && \
	rm -rf * && \
	cp -r ../html/* . && \
	git add . && \
	git commit -am "Pushed root-level docs at $$(date) on ci_testing branch" && \
	git push

# USE THIS ONE!!!
push-root:
	cd $(BUILDDIR) && \
	test -d $(DOCREPONAME) || git clone $(DOCREPOURL) $(DOCREPONAME) && \
	cd $(DOCREPONAME) && \
	git pull origin master && \
	rm -rf * && \
	cp -r ../html/* . && \
	git add . && \
	git commit -am "Pushed root-level docs at $$(date)" && \
	git push
