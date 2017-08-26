# encoding: utf8

'''/////////'''
'''导入python/django自带模块'''
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response  # 分页
from django.http import HttpResponse
import json

'''导入第三方模块'''
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页

'''导入自定义模块'''
from models import Course, CourseResource
from operations.models import UserFavorite, CourseComments

'''自定义类'''


# 课程列表
class CourseListView(View):
    def get(self, request):
        current_page = "course"  # 用于高亮首页的“公开课”标签
        all_courses = Course.objects.all().order_by("-add_time")  # 默认显示的课程列表就是按添加时间（最新）排序
        hot_courses = all_courses.order_by("-click_num")[:3]  # 按照点击量，获取排名前3的课程

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
        p = Paginator(all_courses, 3, request=request)  # 注意把中间的每页显示数量写进去
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'hot_courses': hot_courses,
            'courses': courses,
            'sort_by': sort_by,
            'current_page': current_page,
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        current_page = "course"  # 用于高亮首页的“公开课”标签

        course = Course.objects.get(id=int(course_id))
        # 用户进入本页面，则课程的点击数加1
        course.click_num += 1
        course.save()
        # 根据课程的标签，获取相关的推荐课程(不包含本课程）
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag).exclude(id=course_id)[:2]  # 列出两个相关课程
        else:  # 如果没有相关课程，则置为空列表，否则会报错
            related_courses = []

        # 判断用户是否已收藏课程
        has_fav_course = False  # 默认用户未收藏课程
        has_fav_org = False  # 默认用户未收藏机构
        if request.user.is_authenticated():  # 判断用户是否登录
            # 判断用户是否收藏课程
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            # 判断用户是否收藏机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'current_page': current_page,
        })


# 课程章节信息
class CourseInfoView(View):
    def get(self, request, course_id):
        current_page = "course"  # 用于高亮首页的“公开课”标签

        course = Course.objects.get(id=int(course_id))  # 找出对应的课程
        course_resources = CourseResource.objects.filter(course=course)  # 找出该课程所有的资源

        return render(request, 'course-video.html', {
            'current_page': current_page,
            'course': course,
            'course_resources': course_resources,
        })


# 课程评论
class CourseCommentsView(View):
    def get(self, request, course_id):
        current_page = "course"  # 用于高亮首页的“公开课”标签

        course = Course.objects.get(id=int(course_id))  # 找出对应的课程
        course_resources = CourseResource.objects.filter(course=course)  # 找出该课程所有的资源
        course_comments = CourseComments.objects.filter(course=course)  # 找出该课程所有的评论
        return render(request, 'course-comment.html', {
            'current_page': current_page,
            'course': course,
            'course_resources': course_resources,
            'course_comments': course_comments,
        })


# 添加课程评论(通过ajax实现）
class CourseAddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated():  # 验证用户是否登录
            fail_dict = {'status': 'fail', 'msg': u'用户未登录'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            suc_dict = {'status': 'success', 'msg': u'添加成功'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            fail_dict = {'status': 'fail', 'msg': u'添加失败'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")
