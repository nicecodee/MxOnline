# encoding: utf8
from __future__ import unicode_literals

'''导入python/django自带模块'''
from datetime import datetime
from django.db import models


'''导入第三方模块'''


'''导入自定义模块'''
from organizations.models import CourseOrg




'''自定义Model'''
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=2, verbose_name=u"难度", choices=(("L", u"初级"), ("M", u"中级"), ("H", u"高级")))
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
    students = models.IntegerField(default=0 ,verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0 ,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    category = models.CharField(default="", max_length=20, verbose_name=u"课程类别")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_lesson_num(self):       # 反向获取本课程的章节数
        return self.lesson_set.all().count()

    def get_user_courses(self):       # 反向获取学习本课程的5个用户
        return self.usercourse_set.all()[:5]



class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    course = models.ForeignKey(Course, verbose_name=u"课程")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="courses/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    course = models.ForeignKey(Course, verbose_name=u"课程")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name