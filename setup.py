from setuptools import setup, find_packages

setup(
    name = "yiban",
    # 正式版.公测版.修复版
    version = "0.1.2.20",
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
)