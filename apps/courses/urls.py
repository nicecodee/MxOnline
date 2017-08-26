# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/23 10:56'

'''导入django自带模块'''
from django.conf.urls import url, include

'''导入第三方模块'''

'''导入自定义模块'''
from views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, \
    CourseAddCommentsView, CourseVideoPlayView


'''自定义URL'''
urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),  # 课程列表
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),  # 课程详情页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),  # 章节信息
    url(r'^comments/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name="course_comments"),  # 查看课程评论
    url(r'^add_comments/$', CourseAddCommentsView.as_view(), name="course_add_comments"),  # 添加课程评论
    url(r'^videoplay/(?P<video_id>\d+)/$', CourseVideoPlayView.as_view(), name="video_play"),  # 课程视频播放页
]
