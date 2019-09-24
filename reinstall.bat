@echo off 
echo 正在复制文件
copy program\Template.docx .\

copy program\reply.py reply.py
copy program\Ecode_v1.0.py eqrcode.py
copy program\Edata_v2.1.py edata.py
pause

echo 创建 code 文件夹
mkdir code
pause

echo 正在清理文件
attrib +h reinstall.bat
attrib +h program
del README.html
copy program\README.html .\
del install.bat
pause