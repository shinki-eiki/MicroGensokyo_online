# 简单的单客户循环服务器

from socket import *
# 主机地址为0000，表示绑定本机所有网络接口ip地址
IP='0.0.0.0'
# 端口号
PORT=15480
# 一次从socket缓冲区最多读取512个字节数据
BUFLEN=512

# 实例化对象
#参数依次代表网络层使用IP协议，传输层使用tcp协议
listenSocker=socket(AF_INET,SOCK_STREAM)
#绑定端口和地址
listenSocker.bind((IP,PORT))
#使处于监听状态，最多接受5个客服端
listenSocker.listen(5)
print(f'服务器启动成功！在{PORT}端口等待客户端连接...')

dataSocket,addr=listenSocker.accept()
print('接受一个客户端连接：',addr)

while True: 
    # 尝试读取对方发送的消息
    # BUFLEN 指定从接收缓冲里最多读取多少字节
    recved = dataSocket.recv(BUFLEN)

    # 如果返回空bytes，表示对方关闭了连接
    # 退出循环，结束消息收发
    if not recved:
        break

    # 读取的字节数据是bytes类型，需要解码为字符串
    info = recved.decode()
    print(f'收到对方信息： {info}')

    # 发送的数据类型必须是bytes，所以要编码
    dataSocket.send(f'服务端接收到了信息 {info}'.encode())

dataSocket.close()
listenSocker.close()
