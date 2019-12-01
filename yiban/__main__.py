import sys
import argparse
from shutil import copytree,rmtree,ignore_patterns,copyfile
from os.path import abspath,dirname,join
from os import mkdir
# print(dirname(abspath(__file__)))
# print(abspath(sys.path[0]))

run_dict={
    'forum':('edata.py','Forum-Data'),
}

def run(val):
    vars=run_dict[val]
    src = join(dirname(abspath(__file__)),vars[0])
    if vars[1]:mkdir(vars[1])
    dst = join(abspath(sys.path[0]),vars[1],vars[0])
    copyfile(src,dst)
#     rmtree(dst,ignore_errors=True)
#     copytree(src,dst)
    print(f'请在 {vars[1]} 文件夹下执行操作。')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='yiban',description='Yiban Api Guide')
    parser.add_argument('program',choices=run_dict.keys(),help='yiban\'s programs')
    args = vars(parser.parse_args())
    program = args['program']
    run(program)

