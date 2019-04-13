import random
import requests
from  swiper.config import *
from django.core.cache import cache
from common import keys

def generator_vcode(length=4):
    start = 10**(length-1)
    end = 10**length
    return str(random.randrange(start,end))



def send_sms(phone_num):
    params = YZX_SMS_PARAMS.copy()
    vcode = generator_vcode()
    #生成验证码默认长度为4，可以传入其他长度
    params['param'] = vcode
    params['mobile'] = phone_num

    #设置缓存，180是缓存时间(单位s)
    cache.set(keys.VCODE_KEY%phone_num,vcode,180)

    res = requests.post(url=YZX_SMS_URL,json=params)
    print(res.status_code)
    if res.status_code == 200:
        result = res.json()
        code = result.get('code')
        msg = result.get('msg')
        if code == '000000':
            return True,msg
    else:
        return False,'server error'

if __name__ == '__main__':
    #测试
    send_sms(13760776819)