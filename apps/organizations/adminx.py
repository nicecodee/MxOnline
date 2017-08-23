# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/20 19:59'


import xadmin
from models import CityDict, CourseOrg, Teacher

# 注册城市字典Model
class CityDictAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('name', 'desc', 'add_time')
    search_fields = ('name', 'desc')   # 不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错
    list_filter = ('name', 'desc', 'add_time')

xadmin.site.register(CityDict, CityDictAdmin)


# 注册教学机构
class CourseOrgAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('name', 'desc', 'category', 'click_num', 'fav_num', 'image', 'address', 'city', 'add_time')
    search_fields = ('name', 'desc', 'category', 'click_num', 'fav_num', 'image', 'address', 'city__name')
    list_filter = ('name', 'desc', 'category', 'click_num', 'fav_num', 'image', 'address', 'city__name', 'add_time')

xadmin.site.register(CourseOrg, CourseOrgAdmin)


# 注册讲师
class TeacherAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('name', 'org', 'work_years', 'work_company', 'work_position', 'features', 'click_num', 'fav_num', 'add_time')
    search_fields = ('name', 'org__name', 'work_years', 'work_company', 'work_position', 'features', 'click_num', 'fav_num')
    list_filter = ('name', 'org__name', 'work_years', 'work_company', 'work_position', 'features', 'click_num', 'fav_num', 'add_time')

xadmin.site.register(Teacher, TeacherAdmin)