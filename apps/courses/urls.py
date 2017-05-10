# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/9 0009 17:12'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentsView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节页
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    # 添加评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),
]
