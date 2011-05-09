# -*- coding: utf-8 -*-
from django.db import models
from django import forms

class sms(models.Model):
    phone = models.CharField("Số điện thoại", max_length = 20, blank = False)
    content = models.CharField("Nội dung", max_length = 300, blank = False)
    created = models.DateTimeField("Thời gian tạo", auto_now_add = True)
    modified = models.DateTimeField("Thời gian sửa", auto_now = True)
    
    def __unicode__(self):
        return self.phone
    
class smsForm(forms.Form):
    phone = forms.CharField(label = 'Số điện thoại',
                            widget = forms.widgets.Textarea(attrs={'cols': 40, 'rows': 5}))
    content = forms.CharField(label = 'Nội dung', widget = forms.widgets.Textarea())
    
class smsFromExcelForm(forms.Form):
    file = forms.FileField()
