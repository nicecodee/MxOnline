# encoding: utf8
from __future__ import unicode_literals

'''导入python/django自带模块'''
from datetime import datetime
from django.db import models


'''导入第三方模块'''


'''导入自定义模块'''
from organizations.models import CourseOrg, Teacher




'''自定义Model'''
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    notice = models.CharField(max_length=200, verbose_name=u"课程公告", default="")
    degree = models.CharField(max_length=2, verbose_name=u"难度", choices=(("L", u"初级"), ("M", u"中级"), ("H", u"高级")))
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
    students = models.IntegerField(default=0 ,verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0 ,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    category = models.CharField(default="", max_length=20, verbose_name=u"课程类别")
    tag = models.CharField(max_length=20, verbose_name=u"课程标签", default="")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    must_know = models.CharField(max_length=300, verbose_name=u'课程须知', default="")
    what_you_learn = models.CharField(max_length=300, verbose_name=u'你能学到什么', default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    # 外键
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    # 反向获取本课程的章节数
    def get_lesson_num(self):
        return self.lesson_set.all().count()

    # 反向获取学习本课程的5个用户
    def get_user_courses(self):
        return self.usercourse_set.all()[:5]

    # 反向获取本课程的所有章节
    def get_course_lessons(self):
        return self.lesson_set.all()



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

    # 反向获取本章节的所有视频
    def get_lesson_videos(self):
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
    url = models.CharField(max_length=200, verbose_name=u"访问地址", default="")
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