# 易班微社区统计

### 说明

1. 本程序在 Window 10 & Python 3.7 环境开发，未对其它环境测试。
1. 以下操作全程用网，请确保网络连接正常，网络质量稳定。
1. 如遇异常，请确认非网络问题后，截图留言。

### 下载

- 压缩包（下载后一定要先解压）：

https://github.com/DukeBode/Yiban/archive/Forum-Data.zip

- git 命令（需要有 git 环境）：

```sh
git clone -b Forum-Data https://github.com/DukeBode/Yiban.git
```

---

### 功能使用说明

提醒：使用之前请使用贵微社区定制的 config.py 覆盖系统自带的 config.py 文件

请确认安装好 Python 3 后，请在 powershell 
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

提醒：执行 SQL 操作前，请确认已执行获取微社区数据的操作

- SQL 查询数据(Ctrl + C 退出)

```sh
python edata.py sql
```

- SQL 查询各归属方发帖数量

```sh
python edata.py count
```

- SQL 查询示例

```sh
python edata.py demo
```

- 清理所有 xlsx 文件

```sh
python edata.py clean
```

### 相关软件
| 软件名 | 功能 | 链接 |
| :---: | :---: | :---: |
| Windows10 | 提供 bat 脚本环境 | [https://www.microsoft.com/zh-cn/software-download/windows10](https://www.microsoft.com/zh-cn/software-download/windows10) |
| 7-zip | 解压本程序包 | [https://www.7-zip.org/](https://www.7-zip.org/) |
| Python3 | 运行本 Python 程序 | [https://www.python.org/](https://www.python.org/) |
| VScode | 编辑程序代码 | [https://code.visualstudio.com/](https://code.visualstudio.com/) |

