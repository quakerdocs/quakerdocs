"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

import argparse
import os

import docutils.core
import docutils.writers.html5_polyglot
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Class
from docutils.parsers.rst.directives.misc import Include


# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(string):
    if os.path.isdir(string):
        return string.strip('/')
    else:
        raise NotADirectoryError(string)


def main():
    arg_parser = argparse.ArgumentParser(description='SDG')
    arg_parser.add_argument('source_path', type=dir_path, help='The directory containing the RST files.')
    arg_parser.add_argument('destination_path', type=str, help='The directory to write the output.')
    arg_parser.add_argument('-b', type=str, dest='builder', default="html", help='Builder used for the generator.')
    args = arg_parser.parse_args()

    print("Hello, World!")
    print(args.source_path, args.destination_path, args.builder)

    directives.register_directive('rst-class', Class)
    directives.register_directive('include', Include)

    if not os.path.exists(args.destination_path):
        os.mkdir(args.destination_path)
    args.destination_path = dir_path(args.destination_path)

    slen = len(args.source_path)
    for root, dirs, files in os.walk(args.source_path):
        for dir in dirs:
            new_dir = os.path.join(args.destination_path, root[slen+1:], dir)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
        for file in files:
            if file.endswith('.rst'):
                print("==================== %s ====================" % file)
                src = os.path.join(root, file)
                dest = os.path.join(args.destination_path, root[slen+1:], file[:-4] + '.html')
                docutils.core.publish_file(source_path=src, destination_path=dest, writer_name=args.builder)


if __name__ == "__main__":
    main()
