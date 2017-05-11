from argparse import ArgumentParser

import sys



DESCRIPTION = 'csvtail - prints header and last lines of input.'

EXAMPLES = 'example: cat file.csv | csvtail -n -100 skip first 100 rows and print file.csv till the end.'



def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    lines=[]
    if args.number_of_lines>=0:
        first_line = input_stream.readline().strip()
        line = input_stream.readline().strip()
        while line:
            if len(lines)<args.number_of_lines:
                lines.append(line)
            else:
                lines=lines[1:]+[line]
            line = input_stream.readline().strip()
        output_stream.write(str(first_line)+'\n')
        for i in lines:
            output_stream.write(str(i)+"\n")
    else:
        first_line = input_stream.readline().strip()
        for i in range(-args.number_of_lines):
            input_stream.readline()
        line=input_stream.readline().strip()
        while line:
            output_stream.write(str(line) + "\n")
            line=input_stream.readline().strip()
            
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
