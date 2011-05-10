# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
import re

class customDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d.%m.%yY"))
        super(customDateField, self).__init__(*args, **kwargs)

class sms(models.Model):
    phone = models.CharField("Số điện thoại", max_length = 20, blank = False)
    content = models.CharField("Nội dung", max_length = 300, blank = False)
    created = models.DateField("Thời gian tạo", auto_now_add = True)
    modified = models.DateField("Thời gian sửa", auto_now = True)
    sender = models.ForeignKey(User)
    
    def createdFormat(self):
        return self.created.strftime('%d') + "/"\
                + self.created.strftime('%m') + "/"\
                + self.created.strftime('%Y')
    
    def modifiedFormat(self):
        return self.modified.strftime('%d') + "/"\
                + self.modified.strftime('%m') + "/"\
                + self.modified.strftime('%Y')
    
    def __unicode__(self):
        return self.phone
    
class smsForm(forms.Form):
    namespace_regex = re.compile(r'^[0-9\;\,\ ]+$')
    phone = forms.CharField(label = 'Số điện thoại',
                            help_text = '<br /> <table>\
                                                <col width=160>\
                                                <tr>\
                                                <td></td>\
                                                <td><small><b>Lưu ý:</b> Các ký tự hỗ trợ: "0-9" "," ";" và dầu cách.</small>\
                                                <tr>\
                                                <td></td>\
                                                <td><small>Số điện thoại người nhận phân cách bằng dấu dấu cách hoặc ";" hoặc ",".</small></td>\
                                                </tr>\
                                                </table>',
                            validators = [RegexValidator(regex = namespace_regex)],
                            error_messages={'required': 'Hãy nhập vào số điện thoại.', 'invalid': 'Hãy nhập đúng ký tự cho phép.'},
                            widget = forms.widgets.Textarea(attrs={'cols': 50, 'rows': 5}))
    content = forms.CharField(label = 'Nội dung',
                            max_length = 160,
                            help_text = '<br /> <table>\
                                                <col width=160>\
                                                <tr>\
                                                <td></td>\
                                                <td><small><b>Lưu ý:</b> Số ký tự tối đa: 160 ký tự.</small>\
                                                </table>',
                            error_messages={'required': 'Hãy nhập vào nội dung tin nhắn.', 'max_length': u'Bạn đã nhập %(show_value)d ký tự. Tối đa: 160 ký tự.'},
                            widget = forms.widgets.Textarea(attrs={'cols': 50, 'rows': 5}))
    
class smsFromExcelForm(forms.Form):
    file = forms.FileField()
