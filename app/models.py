# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
Các mô hình dữ liệu dùng chung giữa các đơn vị trong hệ thống và 
các mô hình dữ liệu cấp Phòng, Sở (ngoài trường phổ thông)
'''

ORGANIZATION_LEVEL_CHOICES = (('T', 'Trường'),
                             ('P', 'Phòng'),
                             ('S', 'Sở')) 

class Organization(models.Model):
    ''' Thông tin về sơ đồ tổ chức của các sở, phòng và các trường ''' 
    name = models.CharField('Tên tổ chức', max_length=100) #tên đơn vị. tổ chức 
    level = models.CharField("cấp", max_length=2, choices=ORGANIZATION_LEVEL_CHOICES) #Cấp
    upper_organization = models.ForeignKey('self', blank=True, null=True, verbose_name='Trực thuộc')
    manager_name = models.CharField("Tên thủ trưởng", max_length=100, blank=True, null=True)
    address = models.CharField("Địa chỉ", max_length=255, blank=True, null=True) #
    phone = models.CharField("Điện thoại", max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=100) #tên đơn vị. tổ chức 
    level = forms.CharField(max_length=2, widget=forms.RadioSelect(choices=ORGANIZATION_LEVEL_CHOICES)) #Cấp
    upper_organization = forms.ModelChoiceField(queryset=Organization.objects.all())    
    address = forms.CharField(max_length=255) #
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)

class Position(models.Model):
    LEVEL_CHOICES = (
        (1, 'Nhân Viên Cấp Sở'),
        (2, 'Nhân Viên Cấp Phòng'),
        (3, 'Nhân Viên Cấp Trường'),
        (4, 'Giáo Viên'),
        (5, 'Học Sinh')
    )
    '''
    Chức vụ công tác
    '''
    position_type = models.CharField(max_length=100)
    level = models.IntegerField(choices = LEVEL_CHOICES)
    
    def __unicode__(self):
        return self.position_type

class UserProfile(models.Model):
    '''
    Thông tin về người sủ dụng hệ thống, mở rộng User của Django.
    '''
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization, verbose_name='Đơn vị', null=True)
    position = models.ForeignKey(Position, verbose_name='Chức vụ', blank=True, null=True)
    phone = models.CharField('Điện thoại di động', max_length=20, blank=True, null=True) #để gửi tin nhắn.
    notes = models.CharField('Ghi chú', max_length=255, blank=True, null=True)
    #TODO permission
    
    def __str__(self):
        return "%s's profile" % self.user
    
    # @receiver(post_save, sender=User)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created: 
    #         profile, new = UserProfile.objects.get_or_create(user=instance)

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile

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
