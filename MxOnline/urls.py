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


'''第三方模块'''
# 引入xadmin
import xadmin


'''自定义模块'''
from users.views import LoginView, RegisterView, ActivateUserView


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),    # 把默认的admin 换成 xadmin
    url(r'^captcha/', include('captcha.urls')),     #第三方的图片验证码生成器，需要加上它的url

    # 使用TemplateView， 不用写view函数，直接处理 xx.html 等网页文件
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^activate/(?P<activate_code>.*)/$', ActivateUserView.as_view(), name="user_activate"),

]
