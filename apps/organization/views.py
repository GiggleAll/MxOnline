# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


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

        # 通过关键字筛选
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

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


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'current_page': current_page,
            # 下面这个course_org一定要传进去，不然在调用到org_base.html时会出错
            # org_base.html用到了course_org
            'course_org': course_org,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """

    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        # 判读用户登录状态
        if not request.user.is_authenticated():
            # 如果没有登录
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            # 如果记录已经存在，则表示取消收藏
            exist_records.delete()

            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif fav_type == 2:
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif fav_type == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    讲师列表
    """

    def get(self, request):
        all_teacher = Teacher.objects.all()

        # 讲师排行榜
        teacher_ranklist = all_teacher.order_by('-click_nums')[:2]

        # 通过关键字筛选
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=keywords) |
                                             Q(work_company__icontains=keywords) |
                                             Q(work_position__icontains=keywords))

        # 进行排序
        sort_type = request.GET.get('sort', '')
        if sort_type == 'hot':
            all_teacher = all_teacher.order_by('-click_nums')
        else:
            all_teacher = all_teacher.order_by('-add_time')

        # 讲师总人数
        teacher_nums = all_teacher.count()

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 1, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'teacher_nums': teacher_nums,
            'sort_type': sort_type,
            'teacher_ranklist': teacher_ranklist,
        })


class TeacherDetailView(View):
    """
    讲师详情
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()

        teacher_ranklist = Teacher.objects.all().order_by('-click_nums')[:2]

        # 讲师是否被收藏
        has_fav_teacher = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True

        # 课程机构是否被收藏
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'teacher_ranklist': teacher_ranklist,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org
        })
