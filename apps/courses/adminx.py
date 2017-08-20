# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/20 15:55'


import xadmin
from models import Course, Lesson, Video, CourseResource

# 注册课程
class CourseAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('name', 'desc', 'degree', 'learn_times', 'students', 'fav_num', 'click_num', 'add_time')  # 自定义后台显示的列
    search_fields = ('name', 'desc', 'degree', 'learn_times', 'students', 'fav_num', 'click_num')   # 自定义后台搜索字段(不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错）
    list_filter = ('name', 'desc', 'degree', 'learn_times', 'students', 'fav_num', 'click_num', 'add_time')    # 自定义后台过滤字段


xadmin.site.register(Course, CourseAdmin)


# 注册章节
class LessonAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('course', 'name', 'add_time')  # 自定义后台显示的列
    search_fields = ('course__name', 'name')    #course是Lesson的外键，这里不能直接写course， 而是course的一个具体字段，
    list_filter = ('course__name', 'name', 'add_time')    #course是Lesson的外键，这里不能直接写course， 而是course的一个具体字段，course是个对象，没法直接查询。


xadmin.site.register(Lesson, LessonAdmin)


# 注册视频
class VideoAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('lesson', 'name', 'add_time')
    search_fields = ('lesson__name', 'name') # 自定义后台搜索字段(不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错）
    list_filter = ('lesson__name', 'name', 'add_time')


xadmin.site.register(Video, VideoAdmin)


# 注册课程资源
class CourseResourceAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('course', 'name', 'download', 'add_time')
    search_fields = ('course__name', 'name', 'download')  # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter =  ('course__name', 'name', 'download', 'add_time')


xadmin.site.register(CourseResource, CourseResourceAdmin)