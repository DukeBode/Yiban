pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install -r requirements.txt

attrib +h requirements.txt
attrib +h install.ps1
attrib +h install_env.ps1