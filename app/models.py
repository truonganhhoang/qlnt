# -*- coding: utf-8 -*-
from django.db import models
from django import forms
#from django.contrib.auth.models import User as Django_User

'''
Các mô hình dữ liệu dùng chung giữa các đơn vị trong hệ thống và 
các mô hình dữ liệu cấp Phòng, Sở (ngoài trường phổ thông)
'''

class Organization(models.Model):
    ''' Thông tin về sơ đồ tổ chức của các sở, phòng và các trường
    '''
    ORGANIZATION_LEVEL_CHOICES = (('T', 'Trường'),
                                 ('P', 'Phòng'),
                                 ('S', 'Sở'))
    name = models.CharField('Tên tổ chức', max_length=100) #tên đơn vị. tổ chức 
    address = models.CharField("Địa chỉ", max_length=255, null=True) #
    phone_number = models.CharField("Điện thoại", max_length=20, null=True)
    email = models.CharField(max_length=50)
    level = models.CharField("cấp", max_length=2, choices=ORGANIZATION_LEVEL_CHOICES) #Cấp
    upper_organization = models.ForeignKey('self', blank=True, null=True, verbose_name='Trực thuộc')
    manager_name = models.CharField("Tên thủ trưởng", max_length=100)
    
    def __unicode__(self):
        return self.name

class SchoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['upper_organization'].choices = [(-1, '-------')] + \
                [Organization.objects.filter("organization_type == 'P' or organization_type == 'S'")]
    
    name = forms.CharField(max_length=100, min_length=1)
    address = forms.CharField(max_length=255, min_length=1)
    phone_number = forms.CharField(max_length=40, min_length=9)
    upper_organization = forms.ChoiceField()


#class OrganizationForm(forms.Form):
#    name = forms.CharField(max_length=100, min_length=1)
#    adress = forms.CharField(max_length=255, min_length=1)
#    phone_number = forms.CharField(max_length=40, min_length=9)
#    email_adress = forms.EmailField()
#    manager_name = forms.CharField(max_length=100, min_length=1)


class PositionType(models.Model):
    '''
    Chức vụ công tác
    '''
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

## form validate for PositionType
#class PositionTypeForm(forms.Form):
#    name = forms.CharField(max_length=100, min_length=1)


class User(models.Model):
    '''
    Thông tin về người sủ dụng
    '''
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=40)
    #------------------------------ fax_number = models.CharField(max_length=50)
    email = models.EmailField()
    position = models.ForeignKey(PositionType)
    organization = models.ForeignKey(Organization)
    
    def __unicode__(self):
        return self.name

class UserForm(forms.ModelForm):
    class Meta:
        model = User

# Django dynamic fixture data
#user01 = new(Django_User)
#assert user01.username != 'user01'
#assert user01.password != '01'

#class SchoolYear(models.Model):
#    name = models.CharField(max_length=100)
#    start_date = models.DateField()
#    end_date = models.DateField()
#    active_year = models.BooleanField()
#    
#    def __unicode__(self):
#        return self.name
#
#class SchoolYearForm(forms.Form):
#    name = forms.CharField(max_length=100 , min_length=1)
#    start_date = forms.DateField()
#    end_date = forms.DateField()
#    active_year = forms.BooleanField()
#
#class Semester(models.Model):
#    name = models.CharField(max_length=100)
#    school_year = models.ForeignKey(SchoolYear)
##    school_id = models.ForeingKey(School)
#    start_date = models.DateField()
#    end_date = models.DateField()
#    post_start_date = models.DateField()
#    post_end_date = models.DateField()
#    does_grades = models.CharField(max_length=300)
#    does_exam = models.CharField(max_length=100)
#    does_comments = models.CharField(max_length=500)
#    
#    def __unicode__(self):
#        return self.name
#
#class SemesterForm(forms.Form):
#    name = forms.CharField(max_length=100, min_length=1)
#    start_date = forms.DateField()
#    end_date = forms.DateField()
#    post_start_date = forms.DateField()
#    post_end_date = forms.DateField()
#    does_grades = forms.CharField(max_length=300, min_length=1)
#    does_exam = forms.CharField(max_length=100, min_length=1)
#    does_comments = forms.CharField(max_length=500, min_length=1)