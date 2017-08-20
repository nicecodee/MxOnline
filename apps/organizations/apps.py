# encoding: utf8

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    name = 'organizations'
    verbose_name = u"机构管理"  # 自定义后台显示的应用名（否则会显示英文：organizations)
