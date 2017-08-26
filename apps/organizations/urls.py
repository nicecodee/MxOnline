# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/23 10:56'

'''导入django自带模块'''
from django.conf.urls import url, include


'''导入第三方模块'''


'''导入自定义模块'''
from views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, \
    OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView



'''自定义URL'''
urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name="org_list"),  # 课程机构列表
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),  # 用户添加咨询
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),  # 用户添加咨询
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),  # 机构课程列表
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),  # 机构介绍
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),  # 机构讲师
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),  # 机构或课程的收藏与取消

    # 讲师相关URL
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),  # 讲师列表页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),  # 讲师详情页
]


