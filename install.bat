@echo off 
echo ����pip
python -m pip install -U pip
pause

echo ��װ��������
pip install -r program/requirements.txt
pause

echo ���ڸ����ļ�
copy program\Template.docx .\

copy program\Ecode_v1.0.py eqrcode.py
copy program\Edata_v1.5.py edata.py
pause

echo ���� code �ļ���
mkdir code
pause

echo ���������ļ�
attrib +h install.bat
attrib +h program
del README.html
copy program\README.html .\
pause