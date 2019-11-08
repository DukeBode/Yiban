import sys
import argparse
from shutil import copytree,rmtree,ignore_patterns
from os.path import abspath,dirname,join
# print(dirname(abspath(__file__)))
# print(abspath(sys.path[0]))

run_dict={
    'forum':('program','Forum-Data'),
}

def run(val):
    vars=run_dict[val]
    src = join(dirname(abspath(__file__)),vars[0])
    dst = join(abspath(sys.path[0]),vars[1])
    rmtree(dst,ignore_errors=True)
    copytree(src,dst)
    print(f'请在 {vars} 文件夹下执行操作。')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='yiban',description='Yiban Api Guide')
    parser.add_argument('program',choices=run_dict.keys(),help='yiban\'s programs')
    args = vars(parser.parse_args())
    program = args['program']
    run(program)
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# parser.add_argument('-url',help='微社区链接')
# parser.print_help()
