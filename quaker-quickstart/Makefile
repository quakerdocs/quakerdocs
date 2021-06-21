# You can set these variables from the command line, and also
# from the environment for the first two.
SOURCEDIR = .
BUILDDIR  = build

.PHONY: main help Makefile

# Use the html builder by default.
main:
	quaker "$(SOURCEDIR)" -d "$(BUILDDIR)" -b html

help:
	quaker --help

clean:
	rm -rf $(BUILDDIR)
