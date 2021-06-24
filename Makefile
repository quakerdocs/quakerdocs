# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
BUILDFILE	  = src/quaker
SOURCEDIR     = docs
BUILDDIR      = build

.PHONY: main help Makefile

# Use the html builder by default.
main:
	make html

help:
	python3 $(BUILDFILE) --help

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.
%: Makefile
	python3 $(BUILDFILE) "$(SOURCEDIR)" -d "$(BUILDDIR)" -b $@

clean:
	rm -rf $(BUILDDIR) tmp


# Create a local search executable to test the search functionality.
# Only run after the search.hpp file has been created by the build process.
local_search:
	gcc -Wall -O3 -g3 -DRUN_LOCAL=1 -I"tmp/$(BUILDDIR)/search" src/wasm/search.c -o tmp/$(BUILDDIR)/search/search
