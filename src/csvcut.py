from argparse import ArgumentParser
import sys

DESCRIPTION='Select some columns from csv streem. Could change order of fields.'
EXAMPLES="csvcut -f 1,2 stat.txt csvcut -f st,shows,clicks stat.txt cat stat.txt | csvcut -f shows,uniq,clicks cat stat.txt | csvcut -f select_type-clicks all fields from select_type to clicks cat stats.txt | csvcut -f -shows stat.txt all fields from the first till shows csvcut -f page_id- all fields from page_id till the end csvcut -f description --complement all fields except for description"


def print_row(row,fields,out):
    out.write('\n')
    for i in range(len(fields)-1):
        out.write(str(row[fields[i]])+',')
    out.write(str(row[len(fields)-1]))

def unique(fields):
    f= list(set([x[1] for x in fields]))
    ret=[]
    for i in fields:
        if i[1] in f:
            f.remove(i[1])
            ret.append(i[0])
    return ret


def complement(fields,length):
    ret=list(range(length))
    for q in fields:
        ret.remove(q)
    return ret


def get_fields(fields,header):
    header1=list(header)
    if fields==None:
        return header1
    if ',' in fields:
        i=0
        while i<len(header1):
            if header1[i][1] not in fields:
                del header1[i]
                i-=1
            i+=1
        return header1
    else:
        if '-' in fields:
            for i in header1:
                if i[1]==fields:
                    return [i]

    else:
        if fields[0]=='-':
            field=fields[1:]
            index=0
            for i in header:
                if i==field:
                    break
                index+=1
            return header1[:index+1]
        elif fields[-1]=='-':
            index=0
            field=fields[:-1]
            for i in header:
                if i[1]==field:
                    break
                index+=1
            return header1[index:]
        else:
            index1=0
            index2=0
            field1=fields.split('-')[0]
            field2=fields.split('-')[1]
            for i in header:
                if i==field1:
                    break
                index1+=1
            for i in header:
                if i==field:
                    break
                index2+=1
            return header1[index1:index2+1]


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    header=input_stream.readline().strip().split(args.separator)
    header=[[i,elem] for i,elem in enumerate(header)]
    fields=get_fields(args.fields,header)
    if args.unique:
        fields=unique(fields)
    fields=[e[0] for e in fields]

    if args.complement:
        fields=complement(fields,len(header))
    output_stream.write(','.join([str(i[1]) for i in [header[q] for q in fields]]))
    line=input_stream.readline().strip()
    while line:
        print_row(line.split(args.separator),fields,output_stream)
        line=input_stream.readline().strip()


    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()

def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-f', '--fields',type=str, help="Specify list of fields (comma separated) to cut. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range 'F1-F2' stands for all fields between F1 and F2. Range '-F2' stands for all fields up to F2. Range 'F1-' stands for all fields from F1 til the end.",default=None)
    parser.add_argument('-c', '--complement', help='Instead of leaving only specified columns, leave all except specified',action='store_true')
    parser.add_argument('-u', '--unique', help='Remove duplicates from list of FIELDS',action='store_true')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
