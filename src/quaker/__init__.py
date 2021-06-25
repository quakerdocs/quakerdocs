"""
Main entrypoint of the program.
Call this script to invoke the generation of a static document/website.
"""
import argparse
from pathlib import Path

from quaker_lib.main import Main


def main():
    """
    Main entrypoint of the program.
    """
    arg_parser = argparse.ArgumentParser(description='QuakerDocs')
    arg_parser.add_argument('source_path', type=Path,
                            help='The directory containing the RST files.')
    arg_parser.add_argument('-d', type=Path, dest='build_path',
                            default='build',
                            help='The directory to write the output.')
    arg_parser.add_argument('--init', dest='init', action='store_true',
                            help="Initializes an empty project in the \
                                  specified source_path.")
    arg_parser.set_defaults(init=False)

    args = arg_parser.parse_args()

    print("Running QuakerDocs")
    main = Main(args.source_path, args.build_path, 'html')

    if args.init:
        main.init_empty_project()
        return 0

    if not Path(args.source_path).is_dir():
        print("Error: not a directory")
        arg_parser.print_help()
        return 1
    if not Path(args.source_path).exists():
        print("Error: directory not found")
        arg_parser.print_help()
        return 1

    main.generate()
    return 0


if __name__ == "__main__":
    main()
