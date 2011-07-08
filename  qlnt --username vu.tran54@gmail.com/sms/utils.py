# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.files import File
from django.views.generic.list import ListView
from models import sms, smsFromExcelForm
import os
import urllib
import urllib2
import xlrd
import xlwt

TEMP_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'uploaded')
EXPORTED_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'exported')

def sendSMS(phone,content,user):
    open = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(open)
    print 0
    para = urllib.urlencode({'u': 'VT_username', 'p': 'VT_password'})
#    f = open.open('http://viettelvas.vn:7777/fromcp.asmx', para)
#    f.close();
    if checkValidPhoneNumber(phone):    
        '''Save to db'''
        s = sms(phone=phone, content=content, sender=user, recent=True, success=True)
        s.save()
                    
        '''Send sms via Viettel system'''
        data = urllib.urlencode({
                        'RequestID'     : '4',
                        'CPCode'        : '',
                        'UserID'        : '',
                        'ReceiverID'    : phone,
                        'ServiceID'     : '',
                        'CommandCode'   : '',
                        'Content'       : content,
                        'ContentType'   : ''})
#        f = open.open('http://viettelvas.vn:7777/fromcp.asmx', data)
    else:    
        '''Save to db'''
        s = sms(phone=phone, content=content, sender=user, recent=True, success=False)
        s.save()
        
def checkValidPhoneNumber(phone):
    user_list = User.objects.all()
    user_phone_list = []
    for u in user_list:
        try:
            if (u.get_profile().phone):
                user_phone_list.append(u.get_profile().phone)
        except:
            pass
        
    for p in user_phone_list:
        if p == phone:
            return True
    return False

def getUserFromPhone(phone):
    user_list = User.objects.all()
    for u in user_list:
        try:
            if phone == u.get_profile().phone:
                return u
        except:
            pass
    return ""


def save_file(file):
    saved_file = open(os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls'), 'wb+')
    for chunk in file.chunks():
        saved_file.write(chunk)
    saved_file.close()
    return 'sms_input.xls'
