# encoding: utf8

from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = u"课程管理"  #自定义后台显示的应用名（否则会显示英文：courses)