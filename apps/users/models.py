# encoding: utf8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here


# 用户 (自定义UserProfile 覆盖默认的user表)
class UserProfile(AbstractUser):  # 继承django自带的AbstractUser表，同时添加自定义的字段
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", u"女")), \
                              default="female", verbose_name=u"性别")
    address = models.CharField(max_length=100, default="", verbose_name=u"地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"手机")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", \
                              max_length=100, verbose_name=u"头像")

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):  # 如果是python3.x，就用 __str__(self)
        return self.username  # 这里的username是继承自AbstractUser的字段

    # 获取用户的未读信息条数
    def get_unread_msgs(self):
        from operations.models import UserMessage   # 注意这个import语句不能放在本函数之外，否则会导致循环引用
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=15, verbose_name=u"验证码类型", \
                                 choices=(("register", u"注册"),("forget", u"找回密码"),("update_email", u"修改邮箱")))
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):  # 如果是python3.x，就用 __str__(self)
        return '{0} ({1})'.format(self.code, self.email)

class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=1, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name