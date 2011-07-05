# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views.generic.list import ListView
from sms.models import sms
from sms.utils import *
from school.forms import *



import os
import urllib
import urllib2
import xlrd
import xlwt

TEMP_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'uploaded')
EXPORTED_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'exported')


def manual_sms(request):
    print request.method
    if request.method == 'POST':
        #sendSMS('123','check sendSMS function', request.user)
        #return HttpResponseRedirect(reverse('sent_sms'))
#        return HttpResponse(request.POST.getlist('receiver'))
        receiver_list = request.POST.getlist('receiver')
        phone_list = request.POST['phone']
        content = request.POST['content']
        if ((len(phone_list) != 0 and len(content) != 0) or\
            (len(receiver_list) != 0 and len(content) != 0) ):
            # update all record in sms db: recent = false
            all_sms = sms.objects.filter(sender=request.user)
            for s in all_sms:
                s.recent = False
                s.save()
            
            phone = []
            for r in receiver_list:
                user = User.objects.get(username=r)
                try:
                    phone.append(user.get_profile().phone)
                except:
                    pass
                
            for p1 in phone_list.split(','):
                p1 = p1.split(';')
                for p2 in p1:
                    p2 = p2.split()
                    for p3 in p2:
                        phone.append(p3)
                        
            open = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            urllib2.install_opener(open)
                
            para = urllib.urlencode({'u': 'VT_username', 'p': 'VT_password'})
                
    #        f = open.open('http://viettelvas.vn:7777/fromcp.asmx', para)
    #        f.close();
                
            for p in phone:
                if checkValidPhoneNumber(p):    
                    '''Save to db'''
                    s = sms(phone=p, receiver=getUserFromPhone(p), content=content, sender=request.user, recent=True, success=True)
                    s.save()
                        
                    '''Send sms via Viettel system'''
                    data = urllib.urlencode({
                                    'RequestID'     : '4',
                                    'CPCode'        : '',
                                    'UserID'        : '',
                                    'ReceiverID'    : p,
                                    'ServiceID'     : '',
                                    'CommandCode'   : '',
                                    'Content'       : content,
                                    'ContentType'   : '',
                                    })
    #                f = open.open('http://viettelvas.vn:7777/fromcp.asmx', data)
                else:    
                    '''Save to db'''
                    s = sms(phone=p, receiver=getUserFromPhone(p), content=content, sender=request.user, recent=True, success=False)
                    s.save()
            return HttpResponseRedirect(reverse('sent_sms'))
        else:
            if(len(content)==0):
                content_error = 'Hãy nhập nội dung tin nhắn!'
            else:
                content_error = ''
            if(len(phone_list)==0 and len(receiver_list)==0):
                phone_error = 'Hãy nhập số điện thoại người nhận, hoặc chọn trong danh sách bên dưới.'
            else:
                phone_error = ''
                
            user = User.objects.filter()
            user_list = []
            for u in user:
                try:
                    if (u.get_profile().position in ['HIEU_TRUONG','HIEU_PHO','TRUONG_PHONG','GIAM_DOC_SO']):
                        user_list.append(u)
                except:
                    pass
            
            t = loader.get_template('school/manual_sms.html')
            c = RequestContext(request, {'user_list': user_list,
                                         'content_error': content_error,
                                         'phone_error': phone_error})
            return HttpResponse(t.render(c))
    else:    
        user = User.objects.all()
        user_list = []
        for u in user:
            try:
                if (u.get_profile().position in ['HIEU_TRUONG','HIEU_PHO','TRUONG_PHONG','GIAM_DOC_SO']\
                    and not u.is_superuser):
                    user_list.append(u)
            except:
                pass
        
        print "right view"    
        t = loader.get_template('school/manual_sms.html')
        c = RequestContext(request, {'user_list': user_list})
        return HttpResponse(t.render(c))

CONTENT_TYPES = ['application/vnd.ms-excel']

def excel_sms(request):
    if request.method == 'POST':
        if 'upload' in request.POST:          
            form = smsFromExcelForm(request.POST, request.FILES)
            if form.is_valid():
                print "what the fuck"
                form.clean_file()
                filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
                list = xlrd.open_workbook(filepath)
                sheet = list.sheet_by_index(0)
                data = []
                for r in range(1, sheet.nrows):
                    data.append({'number': sheet.cell_value(r,0),
                                 'content': sheet.cell_value(r,1)})
                t = loader.get_template('school/excel_sms.html')
                c = RequestContext(request, {'data' : data})
                return HttpResponse(t.render(c))
            else:
                print "tag1"
                if request.FILES:
                    file = request.FILES['file']
                    filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
                    if not file.content_type in CONTENT_TYPES:
                        error = 'Bạn chỉ được phép tải lên file Excel.'
                    elif os.path.getsize(filepath) == 0:
                        os.remove(filepath)
                        error = 'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.'
                    elif xlrd.open_workbook(filepath).sheet_by_index(0).nrows == 0:
                        os.remove(filepath)
                        error = 'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.'
                    t = loader.get_template('school/excel_sms.html')
                    c = RequestContext(request, {'error' : error})
                    return HttpResponse(t.render(c))
                else:
                    t = loader.get_template('school/excel_sms.html')
                    c = RequestContext(request)
                    return HttpResponse(t.render(c))
        
        elif 'delete' in request.POST:
            filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
            os.remove(filepath)
            t = loader.get_template('school/excel_sms.html')
            c = RequestContext(request)
            return HttpResponse(t.render(c))
                
        elif 'send' in request.POST:
            # update all record in sms db: recent = false
            all_sms = sms.objects.filter(sender=request.user)
            for s in all_sms:
                if s.recent:
                    s.recent = False
                    s.save()
            filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
            list = xlrd.open_workbook(filepath)
            sheet = list.sheet_by_index(0)
            open = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            urllib2.install_opener(open)
            
            para = urllib.urlencode({'u': 'VT_username', 'p': 'VT_password'})
            
#            f = open.open('http://viettelvas.vn:7777/fromcp.asmx', para)
#            f.close();            
            for r in range(1, sheet.nrows):
                if checkValidPhoneNumber(sheet.cell_value(r,0)):    
                    '''Save to db'''
                    s = sms(phone=sheet.cell_value(r,0), receiver=getUserFromPhone(sheet.cell_value(r,0)), content=sheet.cell_value(r,1), sender=request.user, recent=True, success=True)
                    s.save()
                    
                    '''Send sms via Viettel system'''
                    data = urllib.urlencode({
                                'RequestID'     : '4',
                                'CPCode'        : '',
                                'UserID'        : '',
                                'ReceiverID'    : sheet.cell_value(r,0),
                                'ServiceID'     : '',
                                'CommandCode'   : '',
                                'Content'       : sheet.cell_value(r,1),
                                'ContentType'   : '',
                                })
#                    f = open.open('http://viettelvas.vn:7777/fromcp.asmx', data)
                else:    
                    '''Save to db'''
                    s = sms(phone=sheet.cell_value(r,0), receiver=getUserFromPhone(sheet.cell_value(r,0)), content=sheet.cell_value(r,1), sender=request.user, recent=True, success=False)
                    s.save()
            os.remove(filepath)
            return HttpResponseRedirect(reverse('sent_sms'))
    else:
        if os.path.lexists(os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')):
            filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
            list = xlrd.open_workbook(filepath)
            sheet = list.sheet_by_index(0)
            data = []
            for r in range(1, sheet.nrows):
                data.append({'number': sheet.cell_value(r,0),
                            'content': sheet.cell_value(r,1)})
            t = loader.get_template('school/excel_sms.html')
            c = RequestContext(request, {'data' : data})
            return HttpResponse(t.render(c))
        else:
            t = loader.get_template('school/excel_sms.html')
            c = RequestContext(request)
            return HttpResponse(t.render(c))

#def export_excel(request):
#    response = HttpResponse(mimetype="application/ms-excel")
#    response['Content-Disposition'] = 'attachment; filename=Thống kê tin nhắn.xls'
#    
#    wb = xlwt.Workbook(encoding='utf-8')
#    ws = wb.add_sheet('Thống kê tin nhắn')
#    
#    queryset=sms.objects.all()
#    
#    ws.write(0, 0, 'Số điện thoại người nhận')
#    ws.write(0, 1, 'Nội dung tin nhắn')
#    ws.write(0, 2, 'Thời gian tạo')
#    ws.write(0, 4, 'Người gửi')
#    begin = 1;
#    for q in queryset:
#        ws.write(begin, 0, q.phone)
#        ws.write(begin, 1, q.content)
#        ws.write(begin, 2, q.created)
#        ws.write(begin, 4, q.sender.username)
#        begin = begin+1
#    
#    wb.save(response)
#    return response

def sent_sms(request):
    print "sent_sms view"
    sms_list = sms.objects.filter(sender=request.user,recent=True,success=True)
    t = loader.get_template('school/sent_sms.html')
    c = RequestContext(request, {'sms_list': sms_list})
    return HttpResponse(t.render(c))

def failed_sms(request):
    sms_list = sms.objects.filter(sender=request.user,recent=True,success=False)
    t = loader.get_template('school/failed_sms.html')
    c = RequestContext(request, {'sms_list': sms_list})
    return HttpResponse(t.render(c))
