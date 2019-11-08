from setuptools import setup, find_packages

# 删除 dist 文件夹
from shutil import rmtree
rmtree('dist',ignore_errors=True)
del rmtree

# 读取说明文档
with open('README.md','r',encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "yiban",
    # 版本
    # 正式版.公测版.修复版.调试次数
    version = "0.2.0.8",
    # 作者
    author = 'DukeBode',
    author_email = 'Duke123@aliyun.com',
    # 描述
    description='Yiban Api',
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
        'openpyxl'
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
    },
    python_requires='>=3.8',
)