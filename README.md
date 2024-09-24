# MicroGensokyo_online

可以进行局域网联机对战的游戏软件《微型幻想乡》。

演示视频地址：https://www.bilibili.com/video/BV1P24y1M75z/

要求python版本3.8.9及以上。 
需要安装PIL库
```shell
pip install pillow
```

安装完成后，运行主程序
```shell
python MicroGensokyo.py
```
即可打开一个游戏窗口。
局域网中的多个游戏窗口之间按照下述操作相连接：

1.由其中一个窗口点击"建立主机"；

2.再由其他窗口输入该窗口主机的IP，端口为15480，密码无需输入，然后点击“连接主机”即可与该主机连接。

3.最后由该主机点击“开始游戏”即可开始进行局域网联机游戏。
