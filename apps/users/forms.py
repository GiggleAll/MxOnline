# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/1 10:54'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(label='username', required=True)
    password = forms.CharField(label='password', required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})
