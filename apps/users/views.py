# encoding: utf8

'''****'''
'''导入django自带模块'''
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend  # 用于增加验证方式
from django.db.models import Q  # 用于实现 “或” 逻辑运算
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 哈希加密
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.shortcuts import render_to_response         # 分页


'''导入第三方模块'''
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页


'''导入自定义模块'''
from models import UserProfile, EmailVerifyRecord
from forms import LoginForm, RegisterForm, ForgetPwdForm, PwdResetForm
from utils.email_send import send_email_to_user
from utils.mixin_utils import LoginRequiredMixin  # 导入自定义的验证模块
from forms import UploadImageForm, UserInfoForm
from operations.models import UserCourse, UserFavorite, UserMessage
from organizations.models import CourseOrg, Teacher
from courses.models import Course


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

            # 写入欢迎注册的系统消息（用户可以在个人中心查看该消息）
            welcome_msg = UserMessage()
            welcome_msg.user = user.id
            welcome_msg.message = u"欢迎注册萌学在线网"
            welcome_msg.save()

            return render(request, 'login.html', {'msg': '请先激活账号（激活链接已发送到您的邮箱）！'})
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


# 退出登录
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        # 用户退出后，重定向到首页（注：重定向不能用 render）
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


# 激活用户
class ActivateUserView(View):
    def get(self, request, activate_code):
        email_record = EmailVerifyRecord.objects.filter(code=activate_code)  # email_record是一个列表(可以为空)
        if email_record:  # email_record 不为空，说明 activate_code 是有效的
            email = email_record[0].email  # 列表中只有一个对象，可直接获取该对象的email属性
            user = UserProfile.objects.get(email=email)  # 根据邮箱找到用户
            user.is_active = 1  # 激活该用户（也可设为 True)
            user.save()
            # 激活用户后，把activate_code对应的记录删除，否则同一个activate_code可以随时激活该用户，这是不合理的
            EmailVerifyRecord.objects.filter(code=activate_code).delete()
            return render(request, 'login.html', {'msg': '用户已成功激活，欢迎登录!'})
        return render(request, 'link_fail.html')


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {'forgetpwd_form': forgetpwd_form})

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
        return render(request, "forgetpwd.html", {'forgetpwd_form': forgetpwd_form})


# 显示重置密码页面（即：未提交）
class ShowPwdResetView(View):
    def get(self, request, reset_code):
        email_record = EmailVerifyRecord.objects.filter(code=reset_code)  # email_record是一个列表(可以为空)
        if email_record:  # email_record 不为空，说明 activate_code 是有效的
            email = email_record[0].email  # email_record列表中只有一个对象，可直接获取该对象的email属性
            return render(request, 'password_reset.html', {'email': email, 'reset_code': reset_code})
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
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致，请重新输入!'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            # 密码重置后，把reset_code对应的记录删除，否则同一个reset_code可以随时重置密码，这是不合理的
            EmailVerifyRecord.objects.filter(code=code).delete()
            return render(request, 'login.html')
        return render(request, 'password_reset.html', {'pwdreset_form': pwdreset_form})


# 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)  # 使用instace 来指定实例
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{ "status": "success" }', content_type="application/json")
        return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


# 用户修改头像
class UserImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)  # 利用ModelForm的特性，直接获取一个实例
        if image_form.is_valid():
            # 直接存入数据库
            image_form.save()
            suc_dict = {'status': 'success'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            fail_dict = {'status': 'fail'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")


# 在个人中心更改密码（注：这里使用忘记密码后重置密码时同一个PwdResetForm）
class UserPwdUpdateView(View):
    def post(self, request):
        pwd_update_form = PwdResetForm(request.POST)
        if pwd_update_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            code = request.POST.get("reset_code", "")
            if pwd1 != pwd2:
                fail_dict = {'status': 'fail', 'msg': "密码不一致"}
                return HttpResponse(json.dumps(fail_dict), content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            suc_dict = {'status': 'success'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            return HttpResponse(json.dumps(pwd_update_form.errors), content_type="application/json")


# 发送修改邮箱验证码
class UserSendEmailUpdateCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email", "")
        email_count = UserProfile.objects.filter(email=email).count()
        if email_count != 0:
            # fail_dict = { 'email': "邮箱已存在" }
            # return HttpResponse(json.dumps(fail_dict), content_type="application/json")
            return HttpResponse('{ "email": "邮箱已存在" }', content_type="application/json")

        # 发送激活码到用户的邮箱
        send_email_to_user(email, "update_email")

        # 提示发送成功
        return HttpResponse('{ "status": "success" }', content_type="application/json")
        # suc_dict = {'status': 'success'}
        # return HttpResponse(json.dumps(suc_dict), content_type="application/json")


# 修改邮箱
class UserEmailUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        # 查询数据库，查看是否存在该验证码的记录
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        # 如果记录存在，则修改邮箱，并提示修改成功
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            # 密码重置后，把code对应的记录删除，否则同一个code可以随时修改邮箱，这是不合理的
            EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email").delete()
            return HttpResponse('{ "status": "success" }', content_type="application/json")
        return HttpResponse('{ "email": "验证码错误或失效" }', content_type="application/json")


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


# 我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        # 定义一个空列表，用于存放我收藏的机构
        myfav_orgs = []
        # 从数据库中，找到我收藏的机构的所有记录，这些记录中我们需要的是fav_id，即机构的id
        fav_org_records = UserFavorite.objects.filter(user=request.user, fav_type="org")
        # 遍历上述记录，通过fav_id 取得所有机构的对象，并存入myfav_orgs列表
        for record in fav_org_records:
            org_id = record.fav_id
            org = CourseOrg.objects.get(id=org_id)
            myfav_orgs.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'myfav_orgs': myfav_orgs,
        })


# 我收藏的讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        # 定义一个空列表，用于存放我收藏的讲师
        myfav_teachers = []
        # 从数据库中，找到我收藏的讲师的所有记录，这些记录中我们需要的是fav_id，即讲师的id
        fav_teacher_records = UserFavorite.objects.filter(user=request.user, fav_type="teacher")
        # 遍历上述记录，通过fav_id 取得所有讲师的对象，并存入myfav_teachers列表
        for record in fav_teacher_records:
            teacher_id = record.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            myfav_teachers.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'myfav_teachers': myfav_teachers,
        })

# 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        # 定义一个空列表，用于存放我收藏的讲师
        myfav_courses = []
        # 从数据库中，找到我收藏的课程的所有记录，这些记录中我们需要的是fav_id，即课程的id
        fav_course_records = UserFavorite.objects.filter(user=request.user, fav_type="course")
        # 遍历上述记录，通过fav_id 取得所有课程的对象，并存入myfav_courses列表
        for record in fav_course_records:
            course_id = record.fav_id
            course = Course.objects.get(id=course_id)
            myfav_courses.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'myfav_courses': myfav_courses,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_msgs = UserMessage.objects.filter(user=request.user.id)

        # 用户进入"我的消息"页面后，把所有未读消息置为已读
        all_unread_msgs = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_msg in all_unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_msgs, 10, request=request)
        msgs = p.page(page)

        return render(request, 'usercenter-message.html', {
            'msgs': msgs,
        })




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
