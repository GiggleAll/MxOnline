# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/1 10:54'

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', required=True)
    password = forms.CharField(label='password', required=True, min_length=5)
