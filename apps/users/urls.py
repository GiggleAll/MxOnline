# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/13 21:45'

from django.conf.urls import url

from .views import UserInfoView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    #
    # url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]