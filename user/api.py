from lib.http import render_json
from django.shortcuts import render
from lib.sms import send_sms
from common import errors
from django.core.cache import cache
from common import keys
from user.models import User,Profile
# Create your views here.

def submit_phone(request,code=0):
    """获取短信验证码"""
    if not request.method =='POST':
        return render_json('request method error',errors.REQUEST_METHOD_ERROR)
    else:
        phone = request.POST.get('phone')
        #发送信息，将结果和信息返回
        result,msg = send_sms(phone)
        # print(msg)
        # return JsonResponse({'status':'ok','msg':msg})

        return render_json(msg)

def submit_vcode(request):
    """通过验证码登录注册"""
    #判断是否是POST请求
    if not request.method == 'POST':
        return render_json('request method error', errors.REQUEST_METHOD_ERROR)
    phone = request.POST.get('phone')
    # 取到发到手机的验证码
    vcode = request.POST.get('vcode')
    #取到缓存中的验证码
    cache_vcode = cache.get(keys.VCODE_KEY%phone)

    #对比验证码是否一致
    if vcode == cache_vcode:
        #检测是否存在该用户
        # users = User.objects.filter(phonenum=phone)
        # if not users:
        #     # 1.没有该用户则返回错误，没有该用户
        #     # return render_json('no this user',errors.NO_THIS_USER)
        #
        #     #2.没有该用户则直接创建（防止客户流失）
        #     User.objects.create(phonenum=phone,nickname=phone)
        #3.直接检测没有该用户则直接创建该用户,返回值有2个，一个为user，另外一个是True或False
        user,_ = User.objects.get_or_create(phonenum=phone,nickname=phone)

        #将该用户存到session中
        request.session['uid'] = user.id
        return render_json(user.to_string())
    else:
        render_json('vcode error',errors.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)

    profile = user.profile
    return render_json(profile.to_string())

def set_profile(request):
    """修改个人资料"""
    pass
def upload_avatar(request):
    """头像上传"""
    pass
