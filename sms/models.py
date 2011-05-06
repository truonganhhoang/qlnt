# -*- coding: utf-8 -*-
from django.db import models
from django import forms

class sms(models.Model):
    phone = models.CharField("Số điện thoại", max_length=20, blank=True, null=True)
    content = models.CharField("Nội dung", max_length=300, blank=True, null=True)
    
    def __unicode__(self):
        return self.phone
    
class smsForm(forms.Form):
    phone = forms.CharField(label = 'Số điện thoại người nhận', widget=forms.widgets.Textarea())
    content = forms.CharField(label = 'Nội dung', widget=forms.widgets.Textarea())