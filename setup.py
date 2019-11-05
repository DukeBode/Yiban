from setuptools import setup, find_packages

from shutil import rmtree
rmtree('dist',ignore_errors=True)
del rmtree

setup(
    name = "yiban",
    # 正式版.公测版.修复版.调试次数
    version = "0.1.2.32",
    url = 'https://dukebode.github.io',
    author = 'DukeBode',
    author_email = 'Duke123@aliyun.com',
    packages = find_packages(),
    install_requires=[
        'openpyxl'
    ],
    # scripts=['yiban/edata.py'],
    # entry_points={
    #     'console_scripts': [
    #         'edata=yiban:main',
    #     ],
    # },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/DukeBode/Yiban/issues',
        'Source': 'https://github.com/DukeBode/Yiban',
    },
    python_requires='>=3.8',
)