# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.validators import RegexValidator
import re

class sms(models.Model):
    phone = models.CharField("Số điện thoại", max_length = 20, blank = False)
    content = models.CharField("Nội dung", max_length = 300, blank = False)
    created = models.DateTimeField("Thời gian tạo", auto_now_add = True)
    modified = models.DateTimeField("Thời gian sửa", auto_now = True)
    
    def __unicode__(self):
        return self.phone
    
class smsForm(forms.Form):
    namespace_regex = re.compile(r'^[0-9\;\,\ ]+$')
    error_message = 'alo'
    phone = forms.CharField(label = 'Số điện thoại',
                            help_text = '<br /> <table>\
                                                <tr>\
                                                <td><small><b>Lưu ý:</b></small><br /></td>\
                                                <td><small>Các ký tự hỗ trợ: "0-9" "," ";" và dầu cách.</small>\
                                                <tr>\
                                                <td></td>\
                                                <td><small>Số điện thoại người nhận phân cách bằng dấu dấu cách hoặc ";" hoặc ",".</small></td>\
                                                </tr>\
                                                </table>',
                            validators = [RegexValidator(regex = namespace_regex)],
                            widget = forms.widgets.Textarea(attrs={'cols': 40, 'rows': 5}))
    content = forms.CharField(label = 'Nội dung',
                              max_length = 160,
                              help_text = '<br /> <table>\
                                                <tr>\
                                                <td><small><b>Lưu ý:</b></small><br /></td>\
                                                <td><small>Số ký tự tối đa: 160 ký tự.</small>\
                                                </table>',
                              widget = forms.widgets.Textarea())
    
class smsFromExcelForm(forms.Form):
    file = forms.FileField()
