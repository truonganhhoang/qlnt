# -*- coding: utf-8 -*-


import os.path
import datetime
from django.core.paginator import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *
from django.db import transaction
from django.forms.extras.widgets import SelectDateWidget
from django import forms

from school.utils import *
from school.models import *
from school.school_settings import *
import xlrd
    
class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
    
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('school_id', 'user_id')
        field = ('birthday')
        widgets = {
            'birthday' : SelectDateWidget(years = range( this_year()-15 ,this_year()-100, -1)),
        }
        
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        exclude = ('school_id','user_id')
        field = ('birthday', 'school_join_date', 'ngay_vao_doan', 'ngay_vao_doi', 'ngay_vao_dang', 'father_birthday', 'mother_birthday')
        widgets = {
            'birthday' : SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'school_join_date' : SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'ngay_vao_doan': SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'ngay_vao_doi': SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'ngay_vao_dang': SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'father_birthday': SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'mother_birthday': SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
        }
    def __init__(self, school_id, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        school = Organization.objects.get(id = school_id)
        year_id = school.year_set.latest('time').id
        self.fields['start_year_id'] = forms.ModelChoiceField(queryset = StartYear.objects.filter(school_id = school_id))
        self.fields['class_id'] = forms.ModelChoiceField(queryset = Class.objects.filter(year_id = year_id))
    
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        
    def __init__(self, school_id, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['teacher_id'] = forms.ModelChoiceField(required = False, queryset=Teacher.objects.filter(school_id = school_id))
        self.fields['year_id'] = forms.ModelChoiceField(queryset=Year.objects.filter(school_id = school_id),initial = Year.objects.filter(school_id = school_id).latest('time'))
        self.fields['block_id'] = forms.ModelChoiceField(queryset=Block.objects.filter(school_id = school_id))

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject   
        
    def __init__(self, school_id, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['teacher_id'] = forms.ModelChoiceField(required = False, queryset = Teacher.objects.filter(school_id = school_id))

class KhenThuongForm(forms.ModelForm)        :
    class Meta:
        model = KhenThuong
        exclude = ('student_id', 'term_id')
        field = ('time', 'noi_dung')
        widgets = {
            'time' : SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
            'noi_dung': forms.Textarea(attrs = {'cols': 50, 'rows': 10}),
        }
        
class KiLuatForm(forms.ModelForm):        
    class Meta:
        model = KiLuat
        exclude = ('student_id', 'term_id')
        field = ('time', 'noi_dung')
        widgets = {
            'time' : SelectDateWidget(years = range( this_year() ,this_year()-100,-1)),
            'noi_dung': forms.Textarea(attrs = {'cols': 50, 'rows': 10}),
        }

class HanhKiemForm(forms.ModelForm):
    class Meta:
        model = HanhKiem
    
class DiemDanhForm(forms.ModelForm):
    class Meta:
        model = DiemDanh
        field = ('time')
        widgets = {
            'time' : SelectDateWidget(years = range( this_year() ,this_year()-100, -1)),
        }

class TKDiemDanhForm(forms.ModelForm):
    class Meta:
        model = TKDiemDanh

class TermForm(forms.ModelForm):
    class Meta:
        model = Term

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        
class DateForm(forms.Form):
    date = forms.DateField(label = '', widget = SelectDateWidget(years = range( this_year(), this_year()-2 , -1)), initial = date.today())

class UploadImportFileForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        print "Access __init___" 
        class_list = kwargs.pop('class_list')
        print "in form: ", class_list
        super(UploadImportFileForm, self).__init__(*args, ** kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Chọn lớp:', choices=class_list, required=False)
        self.fields['import_file'] = forms.FileField(label=u'Chọn file excel:')
        
class ManualAddingForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        class_list = kwargs.pop('class_list')
        super(ManualAddingForm, self).__init__(*args, ** kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Chọn lớp:', choices=class_list, required=False)
        
class ClassifyForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        students = kwargs.pop('student_list')
        classes = kwargs.pop('class_list')
        super(ClassifyForm, self).__init__(*args, ** kwargs)
        for student in students:
            label = ' '.join([student.last_name, student.first_name])
            label += u'[' + str(student.birthday.day ) + '-' + str(student.birthday.month) + '-' + str(student.birthday.year)+']'
            self.fields[str(student.id)] = forms.ChoiceField(label = label, choices=classes, required=False)
            
        
        
