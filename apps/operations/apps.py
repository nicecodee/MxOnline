# encoding: utf8

from django.apps import AppConfig


class OperationsConfig(AppConfig):
    name = 'operations'
    verbose_name = u"用户操作"  # 自定义后台显示的应用名（否则会显示英文：operations)