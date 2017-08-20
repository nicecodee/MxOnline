# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/20 15:02'

import xadmin
from xadmin import views    #用于设置主题

from models import EmailVerifyRecord, Banner

'''后台管理界面的样式与主题设置'''
# 启用xadmin的主题并注册
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

# 标题与页脚全局设置并注册
class GlobalSettings(object):
    site_title = u"萌学后台管理系统"
    site_footer = u"萌学在线网"
    menu_style= "accordion"     #设置左侧导航栏自动收起

xadmin.site.register(views.CommAdminView, GlobalSettings)


'''注册Model'''

# 注册邮箱验证Model
class EmailVerifyRecordAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('code', 'email', 'send_type', 'send_time')  # 自定义后台显示的列
    search_fields = ('code', 'email', 'send_type')   # 自定义后台搜索字段(不要把Datetime属性的send_time字段放在这里，否则搜索中文时会报错）
    list_filter = ('code', 'email', 'send_type', 'send_time')   # 自定义后台过滤字段


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


# 注册轮播图
class BannerAdmin(object):   # 注意这里不能继承admin.ModelAdmin
    list_display = ('title', 'image', 'url', 'index', 'add_time')  # 自定义后台显示的列
    search_fields = ('title', 'image', 'url', 'index')  # 自定义后台搜索字段(不要把Datetime属性的add_time字段放在这里，否则搜索中文时会报错）
    list_filter = ('title', 'image', 'url', 'index', 'add_time')   # 自定义后台过滤字段


xadmin.site.register(Banner, BannerAdmin)



