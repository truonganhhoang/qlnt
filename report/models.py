from django.db import models
from django import forms
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
    name = models.CharField('Tên báo cáo', max_length=1000)
    munber_sign = models.CharField('Số hiệu', max_length=100)
    type_doc = models.CharField(max_length=2, choices=TYPE_DOC)
    note = models.CharField('Trích yếu', max_length=1000)
    organization_send = models.CharField('Đơn vị gửi', max_length=500)
    organization_level = models.CharField('cấp', max_length=2, choices=ORGANIZATION_LEVEL_CHOICES)
    level_pri = models.CharField('Mức độ', max_length=10, choices=LEVEL_PRIORITY)
    address_receiver = models.CharField('Đơn vị nhận', max_length=500)
    date_send = models.DateField('Ngày gửi báo cáo')
    date_receiver = models.DateField('Ngày nhận báo cáo')
    reply_doc = models.CharField('Trả lời công văn đi, số hiệu', max_length=100)
    date_end = models.DateField('Ngày hết hạn xử lý')
    human_sign = models.CharField('Người kí', max_length=100)
    store_place = models.CharField('Nơi lưu', max_length=1000)

class SendReport(models.Model):
    name = models.CharField('Tên báo cáo', max_length=1000)
    munber_sign = models.CharField('Số hiệu', max_length=100)
    status = models.BooleanField('Tình trạng')
    type_doc = models.CharField(max_length=2, choices=TYPE_DOC)
    note = models.CharField('Trích yếu', max_length=1000)
    level_pri = models.CharField('Mức độ', max_length=10, choices=LEVEL_PRIORITY)
    address_receiver = models.CharField('Đơn vị nhận', max_length=500)
    date_write = models.DateField('Ngày soạn')
    date_public = models.DateField('Ngày ban hành')
    reply_doc = models.CharField('Trả lời công văn , số hiệu', max_length=100)
    human_sign = models.CharField('Người kí', max_length=100)
    store_place = models.CharField('Nơi lưu', max_length=1000)