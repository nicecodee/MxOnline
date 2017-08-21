# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/21 16:31'


'''导入python/django自带模块'''
from random import Random
from django.core.mail import send_mail


'''导入自定义模块'''
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM



'''自定义函数'''

# 生成随机字符串
def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送带有验证码的邮件
def send_register_email(email, send_type="register"):     # 0 表示发送注册邮件，1 表示发送找回密码邮件
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 利用django自带的方法发送邮件
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = u"萌学在线网注册激活链接"
        email_body = u"复制并通过浏览器打开以下链接，即可激活您的邮箱: http://127.0.0.1:8000/activate/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass



