# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite


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


class CourseDetailView(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 课程是否被收藏
        has_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

        # 课程机构是否被收藏
        has_fav_course_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_course_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(~Q(id=course.id), tag=course.tag).order_by('-click_nums')[:1]
        else:
            relate_courses = Course.objects.filter(~Q(id=course.id)).order_by('-click_nums')[:1]

        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_course': has_fav_course,
            'has_fav_course_org': has_fav_course_org,
            'relate_courses': relate_courses,
        })


class CourseVideoView(View):
    """
    课程的章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        return render(request, 'course-video.html', {
            'course': course,
        })


class CourseCommentView(View):
    """
    课程的评论信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        return render(request, 'course-comment.html', {
            'course': course,
        })
