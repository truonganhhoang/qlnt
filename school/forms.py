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

from school.utils import *
from school.models import *
from school.school_settings import *
import xlrd



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
            label += u'---' + str(student.birthday )
            self.fields[str(student.id)] = forms.ChoiceField(label = label, choices=classes, required=False)
            
        
        
