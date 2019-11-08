import sys
from shutil import copytree,ignore_patterns
from os.path import abspath,dirname,join
# print(dirname(abspath(__file__)))
# print(abspath(sys.path[0]))
try:
    copytree(
        join(dirname(abspath(__file__)),'program'),
        join(abspath(sys.path[0]),'Forum-Data')
        # ,
        # ignore=ignore_patterns(
        #     "__init__.py",
        #     "__main__.py",
        #     "__pycache__"
        # )
    )
except FileExistsError:
    print('文件已存在')

