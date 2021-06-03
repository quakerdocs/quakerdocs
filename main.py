"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""

import argparse
import os

import docutils.core

import html5writer
import custom_dirs
import spdirs


# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(string):
    if os.path.isdir(string):
        return string.strip('/')
    else:
        raise NotADirectoryError(string)


def main():
    """
    Main entrypoint of the program.
    """
    arg_parser = argparse.ArgumentParser(description='SDG')
    arg_parser.add_argument('source_path', type=dir_path, help='The directory containing the RST files.')
    arg_parser.add_argument('destination_path', type=str, help='The directory to write the output.')
    arg_parser.add_argument('-b', type=str, dest='builder', default="html", help='Builder used for the generator.')
    args = arg_parser.parse_args()

    print("Running SDG 0.0.1")

    # Check if destination path exists, otherwise create it.
    if not os.path.exists(args.destination_path):
        print("Making output directory...")
        os.mkdir(args.destination_path)
    args.destination_path = dir_path(args.destination_path)

    # Set-up reStructuredText directives
    spdirs.setup()
    custom_dirs.setup()

    # Load user configuration
    # Check if file exists? Other cwd?
    exec(open(os.path.join(args.source_path, 'conf.py')).read())

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
                with open(src) as f:
                    document = docutils.core.publish_doctree(source=f.read(), source_path=src)
                    write_file = open(dest, 'wb')
                    write_file.write(docutils.core.publish_from_doctree(document, destination_path=dest, writer=html5writer.Writer()))
                    write_file.close()

    print("The generated documents have been saved in %s" % args.destination_path)
    return 0


if __name__ == "__main__":
    """
    Redirect to main-function
    """
    exit(main())
