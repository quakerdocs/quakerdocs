# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
BUILDFILE	  = backend/main.py
SOURCEDIR     = docs
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	python3 $(BUILDFILE) --help

.PHONY: help Makefile backend

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.
%: Makefile
	python3 $(BUILDFILE) "$(SOURCEDIR)" -d "$(BUILDDIR)" -b $@

clean:
	rm -rf $(BUILDDIR)
