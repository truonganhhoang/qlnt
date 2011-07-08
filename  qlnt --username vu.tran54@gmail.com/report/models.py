# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms.extras.widgets import SelectDateWidget
# Create your models here.
ORGANIZATION_LEVEL_CHOICES = (('T', 'Trường'),
                             ('P', 'Phòng'),
                             ('S', 'Sở')) 

LEVEL_PRIORITY = (('T', 'Thường'),
                  ('K', 'Khẩn'),
                  ('M', 'Mật'),
                  ('O', 'Khác'))

TYPE_DOC = (('C', 'Công văn'),
            ('B', 'Báo cáo'),
            ('Q', 'Quyết định'),
            ('T', 'Tờ trình'),
            ('K', 'Khác'))

class ReceiverReport(models.Model):
    name = models.CharField('Tên báo cáo', max_length=1000, blank = True, null=False)
    munber_sign = models.CharField('Số hiệu', max_length=100, blank = True, null=False)
    type_doc = models.CharField(max_length=2, choices=TYPE_DOC)
    note = models.CharField('Trích yếu', max_length=1000)
    organization_send = models.CharField('Đơn vị gửi', max_length=500, blank = True, null=False)
    organization_level = models.CharField('cấp', max_length=2, choices=ORGANIZATION_LEVEL_CHOICES, blank = True)
    level_pri = models.CharField('Mức độ', max_length=10, choices=LEVEL_PRIORITY)
    address_receiver = models.CharField('Đơn vị nhận', max_length=500, blank = True, null=False)
    date_send = models.DateField('Ngày gửi báo cáo', null=False)
    date_receiver = models.DateField('Ngày nhận báo cáo', null=False)
    reply_doc = models.CharField('Trả lời công văn đi, số hiệu', max_length=100, blank = True, null=False)
    date_end = models.DateField('Ngày hết hạn xử lý', null=False)
    human_sign = models.CharField('Người kí', max_length=100, blank = True, null=False)
    store_place = models.CharField('Nơi lưu', max_length=1000, blank = True, null=False)
    
    def __unicode__(self):
        return self.name
class ReceiverReportForm(forms.ModelForm):
    date_send = forms.DateField(widget=SelectDateWidget())
    date_receiver = forms.DateField(widget=SelectDateWidget())
    date_end = forms.DateField(widget=SelectDateWidget())
    class Meta:
        model = ReceiverReport

class SendReport(models.Model):
    name = models.CharField('Tên báo cáo', max_length=1000, blank = True, null=False)
    munber_sign = models.CharField('Số hiệu', max_length=100, blank = True, null=False)
    status = models.BooleanField('Tình trạng', null=False, default = False)
    type_doc = models.CharField(max_length=2, choices=TYPE_DOC)
    note = models.CharField('Trích yếu', max_length=1000)
    level_pri = models.CharField('Mức độ', max_length=10, choices=LEVEL_PRIORITY)
    address_receiver = models.CharField('Đơn vị nhận', max_length=500, blank = True, null=False)
    date_write = models.DateField('Ngày soạn', null=False)
    date_public = models.DateField('Ngày ban hành', null=False)
    reply_doc = models.CharField('Trả lời công văn , số hiệu', max_length=100, blank = True, null=False)
    human_sign = models.CharField('Người kí', max_length=100, blank = True, null=False)
    store_place = models.CharField('Nơi lưu', max_length=1000, blank = True, null=False)
    
    def __unicode__(self):
        return self.name
class SendReportForm(forms.ModelForm):
    date_write = forms.DateField(widget=SelectDateWidget())
    date_end = forms.DateField(widget=SelectDateWidget())
    class Meta:
        model = SendReport