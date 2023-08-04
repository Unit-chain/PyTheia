import argparse
from parser import parser  # assuming your parser is in parser.py
from lexer import lexer

def pretty_print(data, indent=0):
    if isinstance(data, tuple):
        if any(isinstance(item, (list, tuple)) for item in data):
            print('  '*indent + '(' + ', '.join(str(i) for i in data if not isinstance(i, (list, tuple))), end="")
            for item in data:
                if isinstance(item, (list, tuple)):
                    print()
                    pretty_print(item, indent+1)
            print('  '*indent + ')')
        else:
            print('  '*indent + str(data))
    elif isinstance(data, list):
        print('  '*indent + '[')
        for item in data:
            pretty_print(item, indent+1)
        print('  '*indent + ']')
    else:
        print('  '*indent + str(data))


        
def main():

    data = """typedef int myInt;"""

    lexer.input(data)

    for token in lexer:
        print(token)

    # read the source code from the file
    with open("struct.th", 'r') as file:
        source_code = file.read()

    # parse the source code
    result = parser.parse(source_code)

    # print the result
    print(result, "\n")
    pretty_print(result)

if __name__ == '__main__':
    main()

