# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
import re, xlrd, os

TEMP_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'uploaded')
def save_file(file):
    saved_file = open(os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls'), 'wb+')
    for chunk in file.chunks():
        saved_file.write(chunk)
    saved_file.close()
    return 'sms_input.xls'

class customDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d.%m.%yY"))
        super(customDateField, self).__init__(*args, **kwargs)

class sms(models.Model):
    phone = models.CharField("Số điện thoại", max_length=20, blank=False)
    content = models.CharField("Nội dung", max_length=300, blank=False)
    created = models.DateTimeField("Thời gian tạo", auto_now_add=True)
    sender = models.ForeignKey(User)
    recent = models.BooleanField()
    success = models.BooleanField()
    
    def createdFormat(self):
        return self.created.strftime('%d') + "/"\
                + self.created.strftime('%m') + " - "\
                + self.created.strftime('%H')+ ":"\
                + self.created.strftime('%M')
    
    def __unicode__(self):
        return self.phone
    
class smsForm(forms.Form):
    namespace_regex = re.compile(r'^[0-9\;\,\ ]+$')
    phone = forms.CharField(label='Số điện thoại',
                            help_text='<br /> <table>\
                                                <col width=160>\
                                                <tr>\
                                                <td></td>\
                                                <td><small><b>Lưu ý:</b> Các ký tự hỗ trợ: "0-9" "," ";" và dầu cách.</small>\
                                                <tr>\
                                                <td></td>\
                                                <td><small>Số điện thoại người nhận phân cách bằng dấu dấu cách hoặc ";" hoặc ",".</small></td>\
                                                </tr>\
                                                </table>',
                            validators=[RegexValidator(regex = namespace_regex)],
                            error_messages={'required': 'Hãy nhập vào số điện thoại.', 'invalid': 'Hãy nhập đúng ký tự cho phép.'},
                            widget=forms.widgets.Textarea(attrs={'cols': 50, 'rows': 5}))
    content = forms.CharField(label = 'Nội dung',
                            max_length=160,
                            help_text='<br /> <table>\
                                                <col width=160>\
                                                <tr>\
                                                <td></td>\
                                                <td><small><b>Lưu ý:</b> Số ký tự tối đa: 160 ký tự.</small>\
                                                </table>',
                            error_messages={'required': 'Hãy nhập vào nội dung tin nhắn.', 'max_length': u'Bạn đã nhập %(show_value)d ký tự. Tối đa: 160 ký tự.'},
                            widget=forms.widgets.Textarea(attrs={'cols': 50, 'rows': 5}))

CONTENT_TYPES = ['application/vnd.ms-excel']

class smsFromExcelForm(forms.Form):
    file  = forms.Field(label="Chọn file Excel:",
                        help_text='<br/><table>\
                                        <col width=160>\
                                        <tr>\
                                            <td></td>\
                                            <td><small><b>Lưu ý:</b> Bạn chỉ được tải lên file Excel (.xls).</small>\
                                        <tr>\
                                        </table>',
                        error_messages={'required': 'Bạn chưa chọn file nào để tải lên.'},
                        widget=forms.FileInput())
    
    def clean_file(self):
        file = self.cleaned_data['file']
        save_file(file)            
        filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
        
        if not file.content_type in CONTENT_TYPES:
            os.remove(filepath)
            raise forms.ValidationError(u'Bạn chỉ được phép tải lên file Excel.')
        elif os.path.getsize(filepath) == 0:
            raise forms.ValidationError(u'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.')
        elif xlrd.open_workbook(filepath).sheet_by_index(0).nrows == 0:
            raise forms.ValidationError(u'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.')
#        if content._size > settings.MAX_UPLOAD_SIZE:
#            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            return file