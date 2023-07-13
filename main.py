import argparse
from parser import parser  # assuming your parser is in parser.py

def main():
    # set up command-line argument parsing
    parser_arg = argparse.ArgumentParser(description='Parse a program.')
    parser_arg.add_argument('filename', help='the name of the file to parse')

    # parse command-line arguments
    args = parser_arg.parse_args()

    # read the source code from the file
    with open(args.filename, 'r') as file:
        source_code = file.read()

    # parse the source code
    result = parser.parse(source_code)

    # print the result
    print(result)

if __name__ == '__main__':
    main()

