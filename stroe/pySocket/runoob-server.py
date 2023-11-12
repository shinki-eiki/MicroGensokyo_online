#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
 
import socket               # 导入 socket 模块
 
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口
s.bind((host, port))        # 绑定端口

print(host)
print(socket.gethostbyname(host))
s.listen(1)                 # 等待客户端连接
while True:
    c,addr = s.accept()     # 建立客户端连接
    print('连接地址：', addr)
    # c.send('欢迎访问菜鸟教程！')
    c.send(bytes(b'Hello world!'))
    c.close()                # 关闭连接
    