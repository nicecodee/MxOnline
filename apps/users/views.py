# encoding: utf8

'''****'''
'''导入django自带模块'''
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend  # 用于增加验证方式
from django.db.models import Q  # 用于实现 “或” 逻辑运算
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 哈希加密

'''导入自定义模块'''
from models import UserProfile, EmailVerifyRecord
from forms import LoginForm, RegisterForm, ForgetPwdForm, PwdResetForm
from utils.email_send import send_email_to_user




'''自定义类'''

# 重新定义auth的authenticate方法，来允许手机或邮箱登录(都用username的值来获取)
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):  # 使用继承自AbstractUser的check_password方法
                return user

        except Exception as e:
            return None


# 注册（重新定义View里面的get和post方法）
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user_count = UserProfile.objects.filter(email=username).count()
            if user_count != 0:
                return render(request, "register.html", \
                              {'register_form': register_form, 'msg': '该邮箱已被注册，请使用其他邮箱!'})
            user = UserProfile()
            user.username = username
            user.email = username
            user.password = make_password(password)
            user.is_active = 0  # 设置用户激活状态默认为0（也可设为 False)
            user.save()
            # 发送激活码到用户的注册邮箱
            send_email_to_user(username, "register")
            return render(request, 'login.html', {'msg':'请先激活账号（激活链接已发送到您的邮箱）！'})
        return render(request, "register.html", {'register_form': register_form})


# 登录（重新定义View里面的get和post方法）
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)  # 如果authenticate验证成功，返回一个对象，否则返回None
            if user is not None:
                if user.is_active:  # 用户必须存在，且用户已激活，才可登录
                    login(request, user)  # 调用auth自带的login方法（存入session）
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误!'})
        return render(request, 'login.html', {'login_form': login_form})


# 激活用户
class ActivateUserView(View):
    def get(self, request, activate_code):
        email_record = EmailVerifyRecord.objects.filter(code=activate_code)  # email_record是一个列表(可以为空)
        if email_record:   # email_record 不为空，说明 activate_code 是有效的
            email = email_record[0].email  # 列表中只有一个对象，可直接获取该对象的email属性
            user = UserProfile.objects.get(email=email)  # 根据邮箱找到用户
            user.is_active = 1  # 激活该用户（也可设为 True)
            user.save()
            #激活用户后，把activate_code对应的记录删除，否则同一个activate_code可以随时激活该用户，这是不合理的
            EmailVerifyRecord.objects.filter(code=activate_code).delete()
            return render(request, 'login.html', {'msg': '用户已成功激活，欢迎登录!'})
        return render(request, 'link_fail.html')


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {'forgetpwd_form':forgetpwd_form})
    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            username = request.POST.get("email", "")
            user_count = UserProfile.objects.filter(email=username).count()
            if user_count == 0:
                return render(request, "forgetpwd.html", \
                              {'forgetpwd_form': forgetpwd_form, 'msg': '该邮箱不存在，请重新输入!'})

            # 发送重置密码的凭证到用户的注册邮箱
            send_email_to_user(username, "forget")
            return render(request, 'send_success.html')
        return render(request, "forgetpwd.html", {'forgetpwd_form':forgetpwd_form})


# 显示重置密码页面（即：未提交）
class ShowPwdResetView(View):
    def get(self, request, reset_code):
        email_record = EmailVerifyRecord.objects.filter(code=reset_code)  # email_record是一个列表(可以为空)
        if email_record:    # email_record 不为空，说明 activate_code 是有效的
            email = email_record[0].email   # email_record列表中只有一个对象，可直接获取该对象的email属性
            return render(request, 'password_reset.html', {'email': email, 'reset_code':reset_code})
        else:
            return render(request, 'link_fail.html')
        # return render(request, 'password_reset.html')



# 执行重置密码（提交）
class PwdResetView(View):
    def post(self, request):
        pwdreset_form = PwdResetForm(request.POST)
        if pwdreset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            code = request.POST.get("reset_code", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg':'密码不一致，请重新输入!'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            #密码重置后，把reset_code对应的记录删除，否则同一个reset_code可以随时重置密码，这是不合理的
            EmailVerifyRecord.objects.filter(code=code).delete()
            return render(request, 'login.html')
        return render(request, 'password_reset.html', {'pwdreset_form': pwdreset_form})



'''自定义视图函数'''

# 登录
# 由于我们选择用类而不是函数来实现登录的逻辑，因此以下函数代码弃用
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)    # 调用auth自带的login方法
#             return render(request, 'index.html', {})
#         else:
#             return render(request, 'login.html', {'err': '用户名或密码错误！'})
#
#     return render(request, "login.html", {})
