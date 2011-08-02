# -*- coding: utf-8 -*-


import os.path
import datetime
from django.core.paginator import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *
from django.middleware.csrf import get_token
from django.db import transaction
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError
from school.utils import *
from school.models import *
from school.forms import *
from school.school_settings import *
from sms.views import *
import xlrd

RECOVER_MARKTIME = os.path.join('helptool','recover_marktime.html')
SYNC_SUBJECT = os.path.join('helptool','sync_subject.html')

def recover_marktime(request):
    
    marks = Mark.objects.all()
    number_of_defect = 0
    
    if request.method == 'POST':
        for mark in marks:
            try:
                temp = mark.marktime
            except Exception as e:
                a = MarkTime()
                a.mark_id = mark
                a.save()
                number_of_defect +=1
        message = u'Bạn vừa tạo ' + str(number_of_defect) + u' MarkTime records'
    else:
        for mark in marks:
            try:
                temp = mark.marktime
            except Exception as e:
                number_of_defect += 1
        message = u'Thiếu ' + str(number_of_defect) + u'MarkTime records'
    context = RequestContext(request)
    return render_to_response( RECOVER_MARKTIME, { 'message' : message},
                               context_instance = context )
@transaction.commit_on_success
def sync_index(request):

    classes = Class.objects.all()
    message = ''
    try:
        for _class in classes:
            students = _class.pupil_set.order_by('first_name', 'last_name')
            index = 0
            for student in students:
                index +=1
                print index
                if not student.first_name.strip():
                    message += '\n' + student.last_name + ': wrong name'
                    names = student.last_name.strip().split(' ')
                    last_name = ' '.join(names[:len(names)-1])
                    first_name = names[len(names)-1]
                    try:
                        student.first_name = first_name
                        student.last_name = last_name
                        student.save()
                    except Exception as e:
                        print e
                if student.index != index:
                    student.index = index
                    student.save()

    except Exception as e:
        print e
    message += '\n' + u'Sync xong index.'
    context = RequestContext(request)
    return render_to_response( RECOVER_MARKTIME, { 'message' : message},
                               context_instance = context )

@transaction.commit_on_success
def sync_subject(request):
    classes = Class.objects.all()
    print classes
    message = ''
    number = 0
    try:
        school = get_school(request)
        if school.school_level == '1': ds_mon_hoc = CAP1_DS_MON
        elif school.school_level == '2': ds_mon_hoc = CAP2_DS_MON
        elif school.school_level == '3': ds_mon_hoc = CAP3_DS_MON
        else: raise Exception('SchoolLevelInvalid')
        if request.method == 'GET':
            print 'get'
            for _class in classes:
                if not _class.subject_set.count():
                    number+=1
            print 'message'
            message = u'Have ' + str(number) + ' classes those have no subject.'
        elif  request.method == 'POST':
            if 'sync' in request.POST:
                for _class in classes:
                    if not _class.subject_set.count():
                        index = 0
                        for mon in ds_mon_hoc:
                            index +=1
                            add_subject(mon, 1, None, _class, index)
                message = 'Syncing subject from all classes: Done'
                
        context = RequestContext(request)
        return render_to_response(SYNC_SUBJECT, {'message': message, 'number': number},
                                  context_instance = context)
    except Exception as e:
        print e
        