# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/21 11:18'


'''导入django自带模块'''
from django import forms


'''导入第三方模块'''
from captcha.fields import CaptchaField



'''自定义form'''

# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=40)
    password = forms.CharField(required=True, min_length=6)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误!'})


# 忘记密码表单
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误!'})


# 重置密码表单
class PwdResetForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)