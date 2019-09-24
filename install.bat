@echo off 
echo 更新pip
python -m pip install -U pip
pause

echo 安装所需依赖
pip install -r program/requirements.txt
pause

echo 正在复制文件
copy program\Template.docx .\

copy program\Ecode_v1.0.py eqrcode.py
copy program\Edata_v1.5.py edata.py
pause

echo 创建 code 文件夹
mkdir code
pause

echo 正在清理文件
attrib +h install.bat
attrib +h program
del README.html
copy program\README.html .\
pause