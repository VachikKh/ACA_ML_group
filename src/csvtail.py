from argparse import ArgumentParser

import sys



DESCRIPTION = 'csvtail - prints header and last lines of input.'

EXAMPLES = 'example: cat file.csv | csvtail -n -100 skip first 100 rows and print file.csv till the end.'



def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout


    columns = input_stream.readline().split('\n')
    output_stream.write(str(columns[0])+'\n')
    for i in columns[-args.number_of_lines:]:
        output_stream.write(str(i)+'\n')
    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-n', '--number_of_lines', type=int, help='Number of last rows to print if positive ROWS_COUNT. Else skips ROWS_COUNT lines and prints till the end of input.', default=10)
    parser.add_argument('-o', '--output_file', type=str,help='Output file. stdout is used by default.')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    args = parser.parse_args()
    return args

main()