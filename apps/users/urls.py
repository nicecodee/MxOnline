# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/23 10:56'

'''导入django自带模块'''
from django.conf.urls import url, include


'''导入第三方模块'''


'''导入自定义模块'''
from views import UserInfoView, UserImageUploadView, UserPwdUpdateView, UserSendEmailUpdateCodeView, \
    UserEmailUpdateView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView



'''自定义URL'''
urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),  #用户信息查看与保存
    url(r'^image/upload/$', UserImageUploadView.as_view(), name="user_image_upload"),  #用户信息
    url(r'^pwd/update/$', UserPwdUpdateView.as_view(), name="user_pwd_update"),  # 用户个人中心更改密码
    url(r'^send_emailupdate_code/$', UserSendEmailUpdateCodeView.as_view(), name="user_send_emailupdate_code"),  # 发送修改邮箱验证码
    url(r'^email_update/$', UserEmailUpdateView.as_view(), name="user_email_update"),  # 修改邮箱
    url(r'^mycourse/$', MyCourseView.as_view(), name="user_mycourse"),  # 我的课程
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="user_myfav_org"),  # 我收藏的课程机构
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="user_myfav_teacher"),  # 我收藏的讲师
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="user_myfav_course"),  # 我收藏的课程
    url(r'^mymessage/$', MyMessageView.as_view(), name="user_mymessage"),  # 我的消息
]


