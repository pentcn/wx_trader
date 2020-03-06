from time import sleep
from playsound import playsound
from WechatPCAPI.WechatPCAPI import WechatPCAPI


key_person = '期权服务咨询/兰楠@权英小刀'
# key_person = '四人小秘密/孙志刚'


def is_someone(message, name):
    try:
        info = name.split('/')
        if len(info) == 1:
            return message['data']['msgfrominfo']['wx_nickname'] == name
        else:
            return message['data']['msgfrominfo']['wx_nickname'] == info[1] and message['data']['msgtoinfo']['wx_nickname'] == info[0]
    except:
        return False


def get_content(message):
    try:
        return message['data']['msgcontent']
    except:
        return '对方发送非文本内容'


def on_message(message):
    if is_someone(message, key_person):
        content = get_content(message)
        print(content)
        playsound('./sound/200881.wav')


def start_wx():
    wx = WechatPCAPI(on_message=on_message)
    wx.start_wechat(block=True)

    while not wx.get_myself():
        sleep(5)
    print('PC版微信登录成功')


if __name__ == '__main__':
    start_wx()
