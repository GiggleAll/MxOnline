# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

# Create your views here.
class CourseListView(View):
    def get(self, request):
        # 所有的课程
        all_course = Course.objects.all()

        # 热门课程
        hot_course = all_course.order_by('-click_nums')[:3]

        # 对所有课程进行排序
        sort_type = request.GET.get('sort', '')
        if sort_type == 'hot':
            all_course = all_course.order_by('-click_nums')
        elif sort_type == 'students':
            all_course = all_course.order_by('-students')
        else:
            all_course = all_course.order_by('-add_time')

        # 对所有课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_course': courses,
            'hot_course': hot_course,
            'sort_type': sort_type
        })
