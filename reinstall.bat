@echo off 
echo ���ڸ����ļ�
copy program\Template.docx .\

copy program\reply.py reply.py
copy program\Ecode_v1.0.py eqrcode.py
copy program\Edata_v2.1.py edata.py
pause

echo ���� code �ļ���
mkdir code
pause

echo ���������ļ�
attrib +h reinstall.bat
attrib +h program
del README.html
copy program\README.html .\
del install.bat
pause