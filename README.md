# wechatBot
开发环境：Python3 
安装 schedule datetime itchat requests 等库 
pip3 install 库名

将城市，群聊名，朋友备注名等信息改成自己的就成

运行之后会出现一个二维码，就是那种在网页登陆微信的二维码。扫一下，确认登陆即可。
注：因为这个相当于开了网页版微信，所以如果在电脑端或网页端再次登陆微信，程序将会结束

如果您有服务器的话，可以将脚本部署在上面 （在脚本的目录下 输入 nohup python3 -u main.py 1>out.log 2>&1 &)
但如果没有的话，可能就得保持电脑不关机了
