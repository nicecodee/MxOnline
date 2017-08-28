# encoding: utf8

'''/////////'''
'''导入python/django自带模块'''
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response  # 分页
from django.http import HttpResponse
import json
from django.db.models import Q  # 用于实现 “或” 逻辑运算


'''导入第三方模块'''
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页

'''导入自定义模块'''
from models import Course, CourseResource, Video
from operations.models import UserFavorite, CourseComments, UserCourse

# 导入自定义的登录验证类（Mixin在django中一般用于表示一个基础的view，当然也可以随意命令）
from utils.mixin_utils import LoginRequiredMixin


'''自定义类'''


# 课程列表
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")  # 默认显示的课程列表就是按添加时间（最新）排序
        hot_courses = all_courses.order_by("-click_num")[:3]  # 按照点击量，获取排名前3的课程

        # 搜索课程
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:          #__icontains 相当于sql的like语句(i表示不区分大小写)
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords)
                |Q(desc__icontains=search_keywords)
                |Q(detail__icontains=search_keywords)
            )

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
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
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
        })


# 课程章节与资源信息
class CourseInfoView(LoginRequiredMixin, View):    # 同时继承了LoginRequiredMixin，用于登录验证
    def get(self, request, course_id):
        '''获取课程资源'''
        course = Course.objects.get(id=int(course_id))  # 找出对应的课程
        course_resources = CourseResource.objects.filter(course=course)  # 找出该课程所有的资源

        # 课程学习人数加1
        course.students += 1
        course.save()

        '''查询用户是否已关联(开始学习)该课程, 如果未关联，则为用户关联该课程'''
        is_learning = UserCourse.objects.filter(user=request.user, course=course)
        if not is_learning:
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()

        '''获取相关课程'''
        # 获取学过当前课程的所有用户的UserCourse记录
        user_courses = UserCourse.objects.filter(course=course)
        # 从上述记录中，获取所有用户的id(一个列表）
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取上述所有用户学过的所有课程的记录（注意这里是记录的集合，即对象的集合）,同时排除当前课程的记录
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course) # user_id__in 是django ORM的用法，表示一个列表
        # 从上述记录中，获取所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据上述id，获取所有课程，并按点击量排序后取前3名
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:3]

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses':related_courses,
        })


# 课程评论
class CourseCommentsView(LoginRequiredMixin, View):   # 同时继承了LoginRequiredMixin，用于登录验证
    def get(self, request, course_id):
        '''获取课程评论'''
        course = Course.objects.get(id=int(course_id))  # 找出对应的课程
        course_resources = CourseResource.objects.filter(course=course)  # 找出该课程所有的资源
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")  # 找出该课程所有的评论,按时间降序排序

        '''获取相关课程'''
        # 获取学过当前课程的所有用户的UserCourse记录
        user_courses = UserCourse.objects.filter(course=course)
        # 从上述记录中，获取所有用户的id(一个列表）
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取上述所有用户学过的所有课程的记录（注意这里是记录的集合，即对象的集合）,同时排除当前课程的记录
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course) # user_id__in 是django ORM的用法，表示一个列表
        # 从上述记录中，获取所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据上述id，获取所有课程，并按点击量排序后取前3名
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:3]

        '''对课程评论进行分页'''
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(course_comments, 10, request=request)
        page_comments = p.page(page)

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'page_comments':page_comments,
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


# 课程视频播放页面
class CourseVideoPlayView(View):
    def get(self, request, video_id):
        '''获取课程资源'''
        video = Video.objects.get(id=int(video_id))  # 找出对应的课程视频
        course = video.lesson.course    # 用上述找到的视频，根据其外键找出对应的课程
        course_resources = CourseResource.objects.filter(course=course)  # 找出该课程所有的资源

        '''查询用户是否已关联(开始学习)该课程, 如果未关联，则为用户关联该课程'''
        is_learning = UserCourse.objects.filter(user=request.user, course=course)
        if not is_learning:
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()

        '''获取相关课程'''
        # 获取学过当前课程的所有用户的UserCourse记录
        user_courses = UserCourse.objects.filter(course=course)
        # 从上述记录中，获取所有用户的id(一个列表）
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取上述所有用户学过的所有课程的记录（注意这里是记录的集合，即对象的集合）,同时排除当前课程的记录
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course) # user_id__in 是django ORM的用法，表示一个列表
        # 从上述记录中，获取所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据上述id，获取所有课程，并按点击量排序后取前3名
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:3]

        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses':related_courses,
            'video':video,
        })