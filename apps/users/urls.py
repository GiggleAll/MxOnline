# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/13 21:45'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView
from .views import UpdateEmailView, UserCourseView, UserFavOrgView, UserFavTeacherView, UserFavCourseView
from .views import UserMessageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_load'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),
    # 我的收藏-机构
    url(r'^fav_org/$', UserFavOrgView.as_view(), name='fav_org'),
    # 我的收藏-讲师
    url(r'^fav_teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    # 我的收藏-课程
    url(r'^fav_course/$', UserFavCourseView.as_view(), name='fav_course'),
    # 我的消息
    url(r'^message/$', UserMessageView.as_view(), name='user_message'),
]
