# encoding: utf8

'''/////////'''
'''导入python/django自带模块'''
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response         # 分页
from django.http import HttpResponse
import json


'''导入第三方模块'''
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页



'''导入自定义模块'''
from models import Course



'''自定义类'''

# 课程列表
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")   #默认显示的课程列表就是按添加时间（最新）排序

        hot_courses = all_courses.order_by("-click_num")[:3]  #按照点击量，获取排名前3的课程

        sort_by = request.GET.get('sort', "")
        # 按点击数排序
        if sort_by == "hot":
            all_courses = all_courses.order_by("-click_num")
        # 按学习人数（参与人数）排序
        if sort_by == "students":
            all_courses = all_courses.order_by("-students")


        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)  #注意把中间的每页显示数量写进去
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'hot_courses':hot_courses,
            'courses': courses,
            'sort_by': sort_by,
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        # 用户进入本页面，则课程的点击数加1
        course.click_num += 1
        course.save()

        return render(request, 'course-detail.html', {
            'course':course,
        })




