# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


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


class CourseDetailView(LoginRequiredMixin, View):
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


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程的章节信息
    """

    def get(self, request, course_id):
        # 取出当前课程
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        if not UserCourse.objects.filter(user=request.user, course=course):
            UserCourse(user=request.user, course=course).save()

        # 取出当前课程的所有用户
        user_courses = course.get_user_courses()
        # 取出当前课程所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出当前课程所有用户的课程学习记录
        relate_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出当前课程所有用户课程学习记录中的课程id
        relate_course_ids = [user_course.course.id for user_course in relate_user_courses]
        # 取出当前课程所有用户的课程，并按点击量降序排列取5个
        relate_courses = Course.objects.filter(id__in=relate_course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
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


class AddCommentsView(View):
    """
    添加课程的评论信息
    """

    def post(self, request):
        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        if course_id > 0 and comments:
            course = Course.objects.get(id=course_id)
            course_comment = CourseComments(user=request.user, course=course, comments=comments)
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "已添加"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加评论出错"}', content_type='application/json')
