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
    
    
