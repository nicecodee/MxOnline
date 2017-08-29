# encoding: utf8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name



class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.CharField(max_length=10, verbose_name=u"机构标签", default="全国知名")
    category = models.CharField(max_length=20, verbose_name=u"机构类别", default="org",\
                                choices=(("org", "培训机构"), ("school", "高校"), ("personal", "个人")))
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏数")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_num = models.IntegerField(default=0, verbose_name=u"课程数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_num(self):      # 反向获取机构的讲师数量
        return self.teacher_set.all().count()


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    work_years =  models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    features = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(default='', upload_to="teachers/%Y/%m", verbose_name=u"头像", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    # 反向获取讲师的课程数
    def get_teacher_courses_num(self):
        return self.course_set.all().count()