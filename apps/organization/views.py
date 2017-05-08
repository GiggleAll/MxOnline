# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm


# Create your views here.
class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id_get = request.GET.get('city', '')
        if city_id_get:
            # 外键都可以通过 变量名 + _id 这种方式取得
            all_orgs = all_orgs.filter(city_id=int(city_id_get))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()

        # 进行排序
        sort_type = request.GET.get('sort', '')
        if sort_type == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort_type == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id_get,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort_type': sort_type,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 返回的json中的key和value一定要用双引号括起来，不然前端无法正确解析返回的json，不执行success函数，而执行error函数
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')
