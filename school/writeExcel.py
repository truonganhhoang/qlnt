# -*- coding: utf-8 -*-
#from school.views import *

from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.viewCount import *
from school.utils import *
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils import simplejson
import time
import os.path
from xlwt import Workbook, XFStyle, Borders, Font, easyxf ,Alignment
import xlwt 
import xlrd
from xlrd import cellname

h1 = easyxf(
    'font:name Arial, bold on,height 1000 ;align: vert centre, horz center')
h2 = easyxf(
    'font:name Times New Roman, bold on,height 1000 ;align: vert centre, horz center')
h3 = easyxf(
    'font:name Times New Roman, bold on,height 400 ;align: vert centre, horz center')
h4 = easyxf(
'font   :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;'
'borders: top thin,right thin,left thin,bottom thin')
h5 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on, vert centre, horz center;'
'borders: top thin,right thin,left thin,bottom thin')
h6 = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right thin,left thin,bottom dotted')
h7 = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right thin,left thin,bottom thin')

h8 = easyxf(
'font:name Times New Roman ,height 240 ; align:horz left')

h9 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre')

first_name = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right thin,left no_line,bottom dotted')
last_name = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right no_line,left thin,bottom dotted')

first_name1 = easyxf(
'font:name Times New Roman ,height 220 ;'
'borders: right thin,left no_line,bottom thin')
last_name1 = easyxf(
'font:name Times New Roman ,height 220 ;'
'borders: right no_line,left thin,bottom thin')

def report(request):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    
    message=None
    year_id=None
    if year_id==None:
        year_id=get_current_year(request).id
    
    selectedYear =Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')

    
    t = loader.get_template(os.path.join('school','report.html'))    
    c = RequestContext(request, {"message":message,
                                }
                       )
    return HttpResponse(t.render(c))

def printPage13(book):
    s = book.add_sheet('trang 13')
    s.set_paper_size_code(8)
    s.write_merge(24,24,0,13,u'PHẦN GHI ĐIỂM',h1)
    s.write_merge(25,25,0,13,u'HỌC KỲ I',h2)
    
def printPage14(book,class_id):

    s = book.add_sheet('trang 14',True)
    book.set_active_sheet(1)
    s.set_paper_size_code(8)
        
    s.col(0).width = 1000
    s.col(1).width = 5000
    s.col(2).width = 2000
    s.col(3).width = 3000
    s.col(4).width = 4000
    s.col(5).width = 4000
    s.col(6).width = 1400
    s.col(7).width = 1400
    
    s.col(8).width = 3000
    s.col(9).width = 4000
    s.col(10).width = 4000
    s.col(11).width = 1400
    s.col(12).width = 1400
    
    s.write_merge(0,0,0,12,u'HỌC KỲ I',h3)
    
    s.write_merge(1,3,0,0,u'Số\nTT',h4)
    s.write_merge(1,3,1,2,u'Họ và tên',h4)
    
    s.write_merge(1,1,3,7,u'TOÁN',h4)
    s.write_merge(1,1,8,12,u'VẬT LÍ',h4)
    s.write_merge(2,2,3,4,u'Điểm hs 1',h5)
    s.write_merge(2,3,5,5,u'Điểm hs 2 (V)',h5)
    s.write_merge(2,3,6,6,u'KT\nhk',h5)
    s.write_merge(2,3,7,7,u'TBm',h5)
    
    s.write_merge(2,2,8,9,u'Điểm hs 1',h5)
    s.write_merge(2,3,10,10,u'Điểm hs 2 (V)',h5)
    s.write_merge(2,3,11,11,u'KT\nhk',h5)
    s.write_merge(2,3,12,12,u'TBm',h5)
    
    s.write(3,8,u'M',h5)
    s.write(3,9,u'v',h5)
    s.write(3,3,u'M',h5)
    s.write(3,4,u'v',h5)
    
    
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('index')
    toanList  = Mark .objects.filter(student_id__class_id=class_id,subject_id__name='Toán',term_id__number=1).order_by("student_id__index")
    vlList    = Mark .objects.filter(student_id__class_id=class_id,subject_id__name='Vật lí',term_id__number=1).order_by("student_id__index")
    i=0
    for p in pupilList:
        i +=1
        if i % 5 !=0:
            s.write(i+3,0,i,h6)
            s.write(i+3,1,p.last_name,last_name)
            s.write(i+3,2,p.first_name,first_name)
        else:    
            s.write(i+3,0,i,h7)
            s.write(i+3,1,p.last_name,last_name1)
            s.write(i+3,2,p.first_name,first_name1)
    print i        
    i=0    
    for m in toanList:
        i+=1    
        str1=""
        if m.mieng_1!=None: str1+=str(m.mieng_1)+" "
        if m.mieng_2!=None: str1+=str(m.mieng_2)+" "
        if m.mieng_3!=None: str1+=str(m.mieng_3)+" "
        if m.mieng_4!=None: str1+=str(m.mieng_4)+" "
        if m.mieng_5!=None: str1+=str(m.mieng_5)+" "
        str2=""
        if m.mlam_1!=None: str2+=str(m.mlam_1)+" "
        if m.mlam_2!=None: str2+=str(m.mlam_2)+" "
        if m.mlam_3!=None: str2+=str(m.mlam_3)+" "
        if m.mlam_4!=None: str2+=str(m.mlam_4)+" "
        if m.mlam_5!=None: str2+=str(m.mlam_5)+" "
        
        str3=""
        if m.mot_tiet_1!=None: str3+=str(m.mot_tiet_1)+" "
        if m.mot_tiet_2!=None: str3+=str(m.mot_tiet_2)+" "
        if m.mot_tiet_3!=None: str3+=str(m.mot_tiet_3)+" "
        if m.mot_tiet_4!=None: str3+=str(m.mot_tiet_4)+" "
        if m.mot_tiet_5!=None: str3+=str(m.mot_tiet_5)+" "
        
        str4=""
        if m.ck!=None: str4=str(m.ck)
        
        str5=""
        if m.tb!=None: str5=str(m.tb)
        if i % 5 !=0:
            s.write(i+3,3,str1,h6)
            s.write(i+3,4,str2,h6)
            s.write(i+3,5,str3,h6)
            s.write(i+3,6,str4,h6)
            s.write(i+3,7,str5,h6)
        else:    
            s.write(i+3,3,str1,h7)
            s.write(i+3,4,str2,h7)
            s.write(i+3,5,str3,h7)
            s.write(i+3,6,str4,h7)
            s.write(i+3,7,str5,h7)

    print i        
    i=0    
    for m in vlList:
        i+=1    
        str1=""
        if m.mieng_1!=None: str1+=str(m.mieng_1)+" "
        if m.mieng_2!=None: str1+=str(m.mieng_2)+" "
        if m.mieng_3!=None: str1+=str(m.mieng_3)+" "
        if m.mieng_4!=None: str1+=str(m.mieng_4)+" "
        if m.mieng_5!=None: str1+=str(m.mieng_5)+" "
        str2=""
        if m.mlam_1!=None: str2+=str(m.mlam_1)+" "
        if m.mlam_2!=None: str2+=str(m.mlam_2)+" "
        if m.mlam_3!=None: str2+=str(m.mlam_3)+" "
        if m.mlam_4!=None: str2+=str(m.mlam_4)+" "
        if m.mlam_5!=None: str2+=str(m.mlam_5)+" "
        
        str3=""
        if m.mot_tiet_1!=None: str3+=str(m.mot_tiet_1)+" "
        if m.mot_tiet_2!=None: str3+=str(m.mot_tiet_2)+" "
        if m.mot_tiet_3!=None: str3+=str(m.mot_tiet_3)+" "
        if m.mot_tiet_4!=None: str3+=str(m.mot_tiet_4)+" "
        if m.mot_tiet_5!=None: str3+=str(m.mot_tiet_5)+" "
        
        str4=""
        if m.ck!=None: str4=str(m.ck)
        
        str5=""
        if m.tb!=None: str5=str(m.tb)
        
        if i % 5 !=0:
            s.write(i+3,8,str1,h6)
            s.write(i+3,9,str2,h6)
            s.write(i+3,10,str3,h6)
            s.write(i+3,11,str4,h6)
            s.write(i+3,12,str5,h6)
        else:    
            s.write(i+3,8,str1,h7)
            s.write(i+3,9,str2,h7)
            s.write(i+3,10,str3,h7)
            s.write(i+3,11,str4,h7)
            s.write(i+3,12,str5,h7)
    print i        
    for t in range(i+1,56):
        if t % 5!=0:
            s.write(t+3,0,t,h6)
            s.write(t+3,1,"",last_name)
            s.write(t+3,2,"",first_name)
            for j in range(3,13):    
                s.write(t+3,j,"",h6)
        else:    
            s.write(t+3,0,t,h7)
            s.write(t+3,1,"",last_name1)
            s.write(t+3,2,"",first_name1)
            for j in range(3,13):    
                s.write(t+3,j,"",h7)
    if i>55: max =i
    else: max = 55
                
    s.write_merge(max+5,max+5,0,8,u'Trong trang này có......... điểm được sửa chữa,'+
u' trong đó môn: Toán....... điểm, Vật lí.......điểm',h8)
    
    s.write_merge(max+5,max+5,9,12,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,9,12,u'giáo viên chủ nhiệm',h9)
        
def printPage15(book):
    s = book.add_sheet('trang 15')
    book.set_active_sheet(2)
    s.set_paper_size_code(8)
    s.col(0).width = 500
    s.col(1).width = 500
    s.col(2).width = 500
    s.col(3).width = 500
    s.col(4).width = 500
    
def markBookClass(class_id):
    #student_list = _class.pupil_set.all().order_by('index')
    book = Workbook(encoding = 'utf-8')
    printPage13(book)
    printPage14(book,class_id)
    #printPage15(book)
    
    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename=ds_hoc_sinh_%s.xls' % unicode(class_id)
    book.save(response)
    return response

def printMarkBook(request,termNumber=1,class_id=-2):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    
    message=None
    year_id=None
    if year_id==None:
        year_id=get_current_year(request).id
    
    selectedYear =Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    
    class_id  = int(class_id)
    classList =Class.objects.filter(year_id=selectedYear) 
    if class_id!=-2 :
        return markBookClass(class_id)
        
    
    t = loader.get_template(os.path.join('school','print_mark_book.html'))    
    c = RequestContext(request, {"message":message,
                                 'classList':classList,
                                 'termNumber':termNumber,
                                 'classChoice':class_id,
                                }
                       )
    return HttpResponse(t.render(c))
