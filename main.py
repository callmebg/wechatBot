#!/usr/bin/env python3
#coding=utf-8

import schedule
import time
from datetime import datetime
import itchat
import  json
import  urllib.request
import requests
from urllib.parse import urlencode
import random
 
#城市代码可以在 http://www.weather.com.cn/ 上搜索城市，然后在地址栏里可以看到类似
#http://www.weather.com.cn/weather1d/101010100.shtml#search 这样子的东西，里面那串数字就是城市代码
cityList_bsgs = [
    {'code':'101240711','name':"会昌"}
]
#微信群聊名
chatroom_list = ['自家群']
#微信备注名
friend_list = ['张三','李四']
 
#迷信一波，获取个黄历
def get_huangli():
    data = {}
    #appkey 可以在"http://api.jisuapi.com/"免费申请，现在直接用下面这个也成
    data["appkey"] = "8b7a3df10a84b04a"
    data["year"] = datetime.now().year
    data["month"] = datetime.now().month
    data["day"] = datetime.now().day
    url_values = urlencode(data)
    url = "http://api.jisuapi.com/huangli/date" + "?" + url_values
    r = requests.get(url)
    jsonarr = json.loads(r.text)
    #print(jsonarr)
    '''
    无法判断是否为0
    if jsonarr["status"] != "0":
        print(jsonarr["msg"])
        exit()
    '''
    result = jsonarr["result"]
    #print(result)
    content1='天干地支:' + ','.join(result['suici'])
    content2='今日应当注意的生肖:' + result["chong"]
    content3='宜：' + ','.join(result['yi'])
    content4='忌：' + ','.join(result['ji'])
    t = '今日黄历：'+content1+'\n'+content2+'\n'+content3+'\n'+content4
    # print(t)
    return t
 
#每日一句
def get_iciba():
    url = 'http://open.iciba.com/dsapi/'
    r =requests.get(url)
    content = json.loads(r.text)
    return '每日一句：\n'+content['content'] +'\n'+content['note']

#获取该城市实时天气
def getCityWeather_RealTime(cityID):
    url = "http://www.weather.com.cn/data/sk/" + str(cityID) + ".html"
    try:
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')
 
        jsonDatas = json.loads(weatherInfomation)
 
        city        = jsonDatas["weatherinfo"]["city"]
        temp        = jsonDatas["weatherinfo"]["temp"]
        fx          = jsonDatas["weatherinfo"]["WD"]        #风向
        fl          = jsonDatas["weatherinfo"]["WS"]        #风力
        sd          = jsonDatas["weatherinfo"]["SD"]        #相对湿度
        tm          = jsonDatas["weatherinfo"]["time"]
 
        content = city +" " + temp + "℃ " + fx + fl + " " + "相对湿度" + sd + " "  + "发布时间:" + tm
        twitter = {'image': "", 'message': content}
 
    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None
 
#获取该城市全天天气
#返回dict类型: twitter = {'image': imgPath, 'message': content}
def getCityWeather_AllDay(cityID):
    url = "http://www.weather.com.cn/data/cityinfo/" + str(cityID) + ".html"
    stdout = urllib.request.urlopen(url)
    weatherInfomation = stdout.read().decode('utf-8')
    jsonDatas = json.loads(weatherInfomation)

    city        = jsonDatas["weatherinfo"]["city"]
    temp1       = jsonDatas["weatherinfo"]["temp1"]
    temp2       = jsonDatas["weatherinfo"]["temp2"]
    weather     = jsonDatas["weatherinfo"]["weather"]
    img1        = jsonDatas["weatherinfo"]["img1"]

    content = city + "," + weather + ",最高气温:" + temp2 + ",最低气温:"  + temp1
    twitter = {'image': "icon\d" + img1, 'message': content}
    
    return twitter

 
def get_context():
    for city in cityList_bsgs:
        title_small = "[会昌实时天气预报]"
        twitter = getCityWeather_RealTime(city['code'])
        #print(title_small + twitter['message'])
        twitter_realTime = title_small + twitter['message']
 
    for city in cityList_bsgs:
        title_small = "[会昌全天天气预报]"
        twitter = getCityWeather_AllDay(city['code'])
        #print(title_small + twitter["message"])
        twitter_wholeDay = title_small + twitter["message"]
    t = "美好的一天从我的问候开始:各位亲人早上好!\n"+twitter_realTime+"\n"+twitter_wholeDay+'\n'+get_huangli()+'\n'+get_iciba()
    #print(t)
    return t

now = 0
def get_contextt(hello):
    global now
    bq = ['╭(●｀∀´●)╯','╰(●’◡’●)╮',' (●’◡’●)ﾉ ','ヾ(*´▽‘*)ﾉ','╭(′▽`)╭','(′▽`)╯',' (ฅ´ω`ฅ)',' ♪（＾∀＾●）',' （●´∀｀）♪','ヽ(｡◕‿◕｡)ﾉ','✧(๑•̀ㅂ•́)و✧','ε٩ (๑> 灬 <)۶з', '(๑´灬`๑)',' ٩(๑`灬´๑)۶' ,'(•̅灬•̅ )',' (๑ơ 灬 ơ)',' (ง •̀灬•́)ง']
    #t = random.randint(0,len(bq)-1)
    #random以时间为种子，所以不适用于这里的定时发送
    if now == 16:
        now = 0
    t = now + 1
    now = t
    r = hello + bq[t]
    return r
 
def SentChatRoomsMsg(name, context):
    userName = "测试"
    
    groups = itchat.get_chatrooms(update = True)
    #print("groups: ")
    #print(groups)
    
    for room in groups:
        if room['NickName'] == name:
            #nonlocal userName
            userName = room['UserName']
            break
            
    print("userName: "+userName)
    itchat.send_msg(context, userName)
    print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    print("发送到：" + name + "\n")
    print("发送内容：" + context + "\n")
    print("*********************************************************************************")

def SentFriendsMsg(name, context):
    userName = "测试"

    group = itchat.get_friends(update = True)
    #print(group)
    for fname in group:
        if fname['RemarkName'] == name:
            userName = fname['UserName']
            break
    
    print("userName: "+userName)
    itchat.send_msg(context, userName)
    print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    print("发送到：" + name + "\n")
    print("发送内容：" + context + "\n")
    print("*********************************************************************************")

 
def loginCallback():
    print("***登录成功***")
 
def exitCallback():
    print("***已退出***")


if __name__ == "__main__":
    itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCallback, exitCallback=exitCallback)

    for sent_chatroom in chatroom_list:
        schedule.every().day.at("07:00").do(SentChatRoomsMsg,name = sent_chatroom,context = get_context())
        print("任务" + ":\n"+"待发送到：" + sent_chatroom + "\n"+"待发送内容：" + get_context() + "\n")
        print("******************************************************************************\n")

    for friend in friend_list:
        schedule.every().day.at("07:00").do(SentFriendsMsg,name = friend,context = get_contextt('早上好！'))
        schedule.every().day.at("23:00").do(SentFriendsMsg,name = friend,context = get_contextt('晚安！别再熬夜了。'))
        print("任务" + ":\n"+"待发送到：" + friend + "\n")
        print("******************************************************************************\n")


    while True:
        # 启动服务，run_pending()运行所有可以运行的任务
        schedule.run_pending()
