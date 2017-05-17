from argparse import ArgumentParser
import sys


DESCRIPTION = 'csvhead - Print header and first lines of input'
EXAMPLES = 'example: cat file.csv | csvhead -n 100 |less -SR'


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout


    first_line = input_stream.readline().strip()
    line = input_stream.readline().strip()
    output_stream.write(str(first_line)+'\n')
    count_of_prints=0
    while line:
        if count_of_prints<args.number_of_lines:
            output_stream.write(str(line)+'\n')
        else:
            break
        count_of_prints+=1
        line = input_stream.readline().strip()



    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-f', '--format_floats', help='Format floating-point numbers nicely', action='store_true')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-n', '--number_of_lines', type=int, help='Number of first rows to print')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
