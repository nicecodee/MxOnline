# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/20 20:25'

import xadmin
from models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


# 注册用户咨询
class UserAskAdmin(object):  # 注意这里不能继承admin.ModelAdmin
    list_display = ('name', 'mobile', 'course_name', 'add_time')
    search_fields = ('name', 'mobile', 'course_name')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('name', 'mobile', 'course_name', 'add_time')


xadmin.site.register(UserAsk, UserAskAdmin)


# 注册用户咨询
class CourseCommentsAdmin(object):  # 注意这里不能继承admin.ModelAdmin
    list_display = ('course', 'user', 'comments', 'add_time')
    search_fields = ('course__name', 'user__nickname', 'comments')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('course__name', 'user__nickname', 'comments', 'add_time')


xadmin.site.register(CourseComments, CourseCommentsAdmin)


# 注册用户收藏
class UserFavoriteAdmin(object):  # 注意这里不能继承admin.ModelAdmin
    list_display = ('user', 'fav_id', 'fav_type', 'add_time')
    search_fields = ('user__nickname', 'fav_id', 'fav_type')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('user__nickname', 'fav_id', 'fav_type', 'add_time')

xadmin.site.register(UserFavorite, UserFavoriteAdmin)


# 注册用户消息
class UserMessageAdmin(object):  # 注意这里不能继承admin.ModelAdmin
    list_display = ('user', 'message', 'has_read', 'add_time')
    search_fields = ('user', 'message', 'has_read')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('user', 'message', 'has_read', 'add_time')

xadmin.site.register(UserMessage, UserMessageAdmin)


# 注册用户课程
class UserCourseAdmin(object):  # 注意这里不能继承admin.ModelAdmin
    list_display = ('user', 'course', 'add_time')
    search_fields = ('user__nickname', 'course__name')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('user__nickname', 'course__name', 'add_time')

xadmin.site.register(UserCourse, UserCourseAdmin)
