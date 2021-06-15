# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
BUILDFILE	  = src/main.py
SOURCEDIR     = codegrade/docs
BUILDDIR      = build

.PHONY: main help Makefile

# Use the html builder by default.
main:
	make html

help:
	python3 $(BUILDFILE) --help

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.
%: Makefile emsdk
	python3 $(BUILDFILE) "$(SOURCEDIR)" -d "$(BUILDDIR)" -b $@

clean:
	rm -rf $(BUILDDIR)


# Create a local search executable to test the search functionality.
# Only run after the search.hpp file has been created by the build process.
local_search:
	g++ -I"$(BUILDDIR)/search" src/wasm/search.cpp -o $(BUILDDIR)/search/search

# Download and install the Emscripten toolchain in ./emsdk. If you have
# emscripten installed somewhere else, you can also simlink that
# installation to ./emsdk.
emsdk:
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk && ./emsdk install latest && ./emsdk activate latest
