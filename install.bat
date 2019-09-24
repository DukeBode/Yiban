python -m pip install -U pip
pip install -r program/requirements.txt

copy program\Template.docx .\
move program\clean.bat .\
move program\readme.md .\

mkdir code
mklink qrcode.py program\Ecode_v1.0.py
mklink edata.py program\Edata_v1.3.py

del program\requirements.txt
attrib +h program
del "Python download.url"
del README.txt
del install.bat