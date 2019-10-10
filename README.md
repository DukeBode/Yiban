# 易班微社区统计


### 下载

- 压缩包：

https://github.com/DukeBode/Yiban/archive/Forum-Data.zip

- git 命令：

```sh
git clone -b Forum-Data https://github.com/DukeBode/Yiban.git
```

---

### 功能使用说明

请在 powershell 环境下输入以下命令
> 在文件所在目录 按住 shift 键，并点击鼠标右键，选择 powershell 即可打开

- 统计话题评论（单篇）

```sh
python edata.py replys 易班话题链接
```

- 话题内容（单篇）

```sh
python edata.py content 易班话题链接
```

- 查看微社区数据表头

```sh
python edata.py heads
```

- 获取微社区数据（请在查询数据之前执行）

```sh
python edata.py articles 开始年-月-日
```

执行以下操作前，请确认已执行获取微社区数据的操作

- SQL 查询数据(Ctrl + C 退出)

```sh
python edata.py sql
```

- SQL 查询示例

```sh
python edata.py demo
```

- 清理所有 xlsx 文件

```sh
python edata.py clean
```


### 程序功能
- [x] 通过标题关键词统计指定时间段内发过的帖子
- [x] 通过标题关键词数组统计相关主题发帖量
- [x] 获取点击量、回复量、点赞排行
- [x] 获取个人发帖的发帖量、点击量、点赞量、评论量
- [x] 统计评论信息

### 程序环境
| 软件名 | 功能 | 链接 |
| :---: | :---: | :---: |
| Windows10 | 提供 bat 脚本环境 | [https://www.microsoft.com/zh-cn/software-download/windows10](https://www.microsoft.com/zh-cn/software-download/windows10) |
| 7-zip | 解压本程序包 | [https://www.7-zip.org/](https://www.7-zip.org/) |
| Python3 | 运行本 Python 程序 | [https://www.python.org/](https://www.python.org/) |
| VScode | 编辑程序代码 | [https://code.visualstudio.com/](https://code.visualstudio.com/) |


<!-- ### 安装说明 -->

<!-- 1. 确认程序环境以及网络连接正常
1. 在[更新日志](#更新日志)中下载最新版
1. 使用 7-zip（或其它压缩软件）解压安装包
1. 首次使用，点击 install.bat 文件进行安装环境和部署程序
1. 非首次使用，点击 reinstall.bat 文件直接进行部署程序
1. 确认安装，如有红色字体，请重新安装 -->
