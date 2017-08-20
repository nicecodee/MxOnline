# encoding: utf8

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = u"用户信息"  # 自定义后台显示的应用名（否则会显示英文：organizations)
