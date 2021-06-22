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

docs: Makefile emsdk
	python3 $(BUILDFILE) "docs" -d "builddocs" -b html

clean:
	rm -rf $(BUILDDIR) tmp


# Create a local search executable to test the search functionality.
# Only run after the search.hpp file has been created by the build process.
local_search:
	gcc -Wall -O3 -g3 -I"tmp/$(BUILDDIR)/search" src/wasm/search.c -o tmp/$(BUILDDIR)/search/search

test:
	clang --target=wasm32 -Wall -O3 -g3 -I"tmp/$(BUILDDIR)/search" src/wasm/search.c -o tmp/$(BUILDDIR)/search/search.wasm


# Download and install the Emscripten toolchain in ./emsdk. If you have
# emscripten installed somewhere else, you can also simlink that
# installation to ./emsdk.
emsdk:
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk && ./emsdk install latest && ./emsdk activate latest
