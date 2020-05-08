'''
@Author: DukeBode
@Date: 2020-04-25 09:19:10
@LastEditTime: 2020-05-08 18:23:18
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\setup.py
'''
# 删除 dist、Forum-Data 文件夹
from shutil import rmtree
rmtree('Forum-Data',ignore_errors=True)
rmtree('build',ignore_errors=True)
rmtree('dist',ignore_errors=True)
del rmtree

with open('README.md','r',encoding='utf-8') as f:
    # 读取说明文档
    long_description = f.read()

from setuptools import setup, find_packages
from yiban import __version__

setup(
    name = "yiban",
    # 版本
    # 正式版.公测版.修复版.调试次数
    version = __version__,
    # 作者
    author = 'DukeBode',
    author_email = 'Duke123@aliyun.com',
    # 描述
    description='Yiban Tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 项目网址
    url = 'https://github.com/DukeBode/Yiban',
    packages = find_packages(),
    # platforms =
    # 许可证
    license = 'BSD 3-Clause',
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
    ],
    install_requires=[
        'openpyxl',
        'ruamel.yaml',
        'beautifulsoup4'
    ],
    # scripts=['yiban/edata.py'],
    # entry_points={
    #     'console_scripts': [
    #         'edata=yiban:main',
    #     ],
    # },
    # 关键字
    keywords='Yiban',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/DukeBode/Yiban/issues',
        'Source': 'https://github.com/DukeBode/Yiban',
        'Documentation': 'https://dukebode.github.io/Yiban',
    },
    python_requires='>=3.8',
)