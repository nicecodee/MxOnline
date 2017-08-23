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


# 用户添加咨询（提交"我要学习" 表单），该功能采用异步方式，前端用ajax实现
class AddUserAskView(View):
   def post(self, request):
       userask_form = UserAskForm(request.POST)
       if userask_form.is_valid():
           userask_form.save(commit=True)    # 不需要取出表单数据，直接存入数据库(这就是Model转换成的form的优点)
           suc_dict = {'status':'success'}
           return  HttpResponse(json.dumps(suc_dict), content_type="application/json")
       else:
           fail_dict = {'status':'fail', 'msg':u'填写错误'}
           return HttpResponse(json.dumps(fail_dict), content_type="application/json")