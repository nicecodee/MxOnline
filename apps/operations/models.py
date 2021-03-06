# encoding: utf8

from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from courses.models import Course
from users.models import UserProfile


# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")


    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.comments


class UserFavorite(models.Model):
    fav_id = models.IntegerField(default=0 ,verbose_name=u"数据id")
    fav_type = models.CharField(choices=(("course", u"课程"), ("org", u"课程机构"), ("teacher", u"讲师")), default="course", \
                                   verbose_name=u"收藏类型", max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")  # 默认为0，表示消息发给所有用户
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name


