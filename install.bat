echo "����pip"
python -m pip install -U pip
echo "��װ��������"
pip install -r program/requirements.txt
echo "���ڸ����ļ�"
copy program\Template.docx .\

copy program\Ecode_v1.0.py eqrcode.py
copy program\Edata_v1.3.py edata.py
echo "���� code �ļ���"
mkdir code
echo "���������ļ�"
attrib +h install.bat
attrib +h program
del README.html
copy program\README.html .\