# coding=utf-8
__author__ = 'szh'
__date__ = '2017/5/6 17:54'
import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        :return: 
        '''
        mobile = self.cleaned_data['mobile']
        regex_mobile = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')

