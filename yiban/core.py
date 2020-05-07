'''
@Author: your name
@Date: 2020-05-07 23:08:55
@LastEditTime: 2020-05-08 00:43:39
@LastEditors: your name
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\core.py
'''
class Uri:
    def __init__(self,ssl=True):
        self.protocol = 'https' if ssl else 'http'
        self.host = 'yiban.cn'
    
    def __call__(self,data):
        return f'{self.protocol}://{self.host}/{data}'

    def uri(self,address,data):
        return f'{self.protocol}://{address}.{self.host}/{data}'

