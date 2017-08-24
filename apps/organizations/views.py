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
from models import CourseOrg, CityDict
from forms import UserAskForm
from courses.models import Course
from operations.models import UserFavorite



'''自定义类'''

# 课程机构列表
class OrgListView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:3]  #按照点击量，获取排名前3的机构

        # 按城市筛选
        city_id = request.GET.get('cid', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))   #city_id是CourseOrg表的一个字段（外键生成）
        # 按机构类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort_by = request.GET.get('sort', "")
        # 按学习人数排序
        if sort_by == "students":
            all_orgs = all_orgs.order_by("-stu_num")
        # 按课程数排序
        if sort_by == "courses":
            all_orgs = all_orgs.order_by("-course_num")


        org_num = all_orgs.count() # 获取经过筛选后的机构数量（默认为全部机构的数量）

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)  #注意官方说明忘了把中间的每页显示数写进去，这是官方的疏忽
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'orgs':orgs,
            'org_num':org_num,
            'all_citys':all_citys,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort_by':sort_by,
        })


# 用户添加咨询（提交"我要学习" 表单），采用异步方式，前端用ajax实现
class AddUserAskView(View):
   def post(self, request):
       userask_form = UserAskForm(request.POST)
       if userask_form.is_valid():
           userask_form.save(commit=True)    # 不需要取出表单数据，直接存入数据库(这就是Model转换成的form的优点)
           # return HttpResponse('{"status:"success"}', content_type='application/json')
           suc_dict = {'status':'success'}
           return  HttpResponse(json.dumps(suc_dict), content_type="application/json")
       else:
           # return HttpResponse('{"status:"fail","msg":u"添加出错"}', content_type='application/json')
           fail_dict = {'status':'fail', 'msg':u'填写错误'}
           return HttpResponse(json.dumps(fail_dict), content_type="application/json")


# 机构详情首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据org_id查询对应的机构

        # 判断用户是否已收藏机构
        has_fav = False # 默认用户未收藏机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]   # 获取该机构的前3个课程
        all_teachers = course_org.teacher_set.all()[:1]     # 获取该机构的第1个教师
        return render(request, 'org-detail-homepage.html', {
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


# 机构课程列表
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据org_id查询对应的机构

        # 判断用户是否已收藏机构
        has_fav = False # 默认用户未收藏机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()   # 获取该机构的课程
        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })



# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据org_id查询对应的机构

        # 判断用户是否已收藏机构
        has_fav = False # 默认用户未收藏机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))  # 根据org_id查询对应的机构

        # 判断用户是否已收藏机构
        has_fav = False # 默认用户未收藏机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()   # 获取该机构的讲师
        return render(request, 'org-detail-teachers.html', {
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构收藏与取消
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)  #默认值为0而不是空字符串，是为了避免filter查询时空字符串抛出异常
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated():     # 验证用户是否登录
            fail_dict = {'status': 'fail', 'msg': u'用户未登录'}
            return HttpResponse(json.dumps(fail_dict), content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:   #如果已经存在记录，说明用户要取消收藏
            exist_records.delete()
            suc_dict = {'status': 'success', 'msg': u'收藏'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = fav_type
                user_fav.save()
                suc_dict = {'status': 'success', 'msg': u'取消收藏'}
                return HttpResponse(json.dumps(suc_dict), content_type="application/json")
            else:
                fail_dict = {'status': 'fail', 'msg': u'收藏出错'}
                return HttpResponse(json.dumps(fail_dict), content_type="application/json")





