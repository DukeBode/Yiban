from setuptools import setup, find_packages

setup(
    name = "yiban",
    # 正式版.公测版.修复版
    version = "0.1.0",
    url = 'https://dukebode.github.io',
    author = 'DukeBode',
    author_email = 'Duke123@aliyun.com',
    packages = find_packages(),
    install_requires=[
        'openpyxl'
    ]
)