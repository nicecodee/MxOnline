# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/23 10:56'

'''导入django自带模块'''
from django.conf.urls import url, include


'''导入第三方模块'''


'''导入自定义模块'''
from views import UserInfoView, UserImageUploadView, UserPwdUpdateView



'''自定义URL'''
urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),  #用户信息
    url(r'^image/upload/$', UserImageUploadView.as_view(), name="user_image_upload"),  #用户信息
    url(r'^pwd/update/$', UserPwdUpdateView.as_view(), name="user_pwd_update"),  # 用户个人中心更改密码
]


