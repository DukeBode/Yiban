# 易月动态

## 文件说明

/code/          供二维码存放 
/clean.bat      快速清空 code 文件夹，初始化 Template.docx，删除数据库
/edata.py       用于获取微社区的发帖信息，使用前需根据修改相关内容
/qrcode.py      用于批量生成二维码
/Template.docx  易月动态模板，可使用 clean.bat 重建
/readme.md      本文档

## 二维码

1. Execl 整理数据
1. 确保所有文件名不能包含下列任何字符 \/:*?<>|
1. 复制至txt文档中
1. python qr
1. 打开 code 文件夹
1. 确认数量，全选，生成 code.zip
1. 重命名分享

## 特色学院轻应用

1. 导出上月1日至本月1日的轻应用数据
1. 筛选数据选定合适的时间
1. pv改为浏览量，按浏览量排名选取前五，校级不得超过两条
1. 删除创建者ID、应用状态、发布时间等列
1. 整理内容，以序号、机构、轻应用名称、添加人数、浏览量的顺序整理
1. 机构根据用户姓名及应用名称填写，以 LUT 的院系设置为准

## 易班头条

1. 文本编辑器打开 Edata 文件 设置 lut.save() 变量
1. python Edata
1. 获取点击量排行（前100）
1. 粘贴至 excel 表
1. $分列，筛选，排序
1. 删除通知类，按浏览量排名选取前五，校级不得超过两条
1. 整理内容，序号、机构、标题、访问量的顺序整理
1. 机构根据用户姓名及应用名称填写，以 LUT 的院系设置为准
1. 重命名后分享

## 附

1. LUT 院系设置  http://www.lut.cn/www/HdClsContentMain.asp?ClassId=10
1. 7-zip压缩软件 https://www.7-zip.org/
1. vscode编辑器  https://code.visualstudio.com/
1. powershell/cmd 打开： 工作目录下按住shift右键打开
