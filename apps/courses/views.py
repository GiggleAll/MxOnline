# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View

from .models import Course

# Create your views here.
class CourseListView(View):
    def get(self, request):
        # 所有的课程
        all_course = Course.objects.all()
        # 热门课程
        hot_course = all_course.order_by('-click_nums')[:3]

        return render(request, 'course-list.html', {
            'all_course': all_course,
            'hot_course': hot_course,
        })
