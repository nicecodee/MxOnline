# encoding: utf8

"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
'''django自带模块'''
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView   #引入django自带的TemplateView,用于直接处理静态文件
from django.views.static import serve        # 用于处理静态文件


'''第三方模块'''
# 引入xadmin
import xadmin
from MxOnline.settings import MEDIA_ROOT    #, STATIC_ROOT


'''自定义模块'''
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActivateUserView, ForgetPwdView, \
    ShowPwdResetView, PwdResetView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),    # 把默认的admin 换成 xadmin
    url(r'^captcha/', include('captcha.urls')),     #第三方的图片验证码生成器，需要加上它的url

    # 使用TemplateView， 不用写view函数，直接处理 xx.html 等网页文件
    # url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^activate/(?P<activate_code>.*)/$', ActivateUserView.as_view(), name="user_activate"),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^showpwdreset/(?P<reset_code>.*)/$', ShowPwdResetView.as_view(), name="show_pwd_reset"),
    url(r'^pwdreset/$', PwdResetView.as_view(), name="pwd_reset"),

    # 设置上传文件的访问处理(注意路径 ^uploads 要和settings.py 里的 MEDIA_URL 对应)
    url(r'^uploads/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    # 处理静态文件（当settings.py设置DEBUG = False 时）
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    # 导入各个app的urls.py
    url(r'^org/', include('organizations.urls', namespace='org')),    # 课程机构URL配置
    url(r'^course/', include('courses.urls', namespace='course')),    # 课程相关URL配置
    url(r'^user/', include('users.urls', namespace='user')),  # 用户URL配置
]

# 全局404和500页面配置(注意：类似 handler404 这些变量名称是固定的)
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'