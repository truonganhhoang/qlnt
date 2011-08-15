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
s1=1000
s2=5000
s3=2000
m1=3000
m2=4000
m3=4000
m4=1400
m5=1400

m6=3000
m7=3000
m8=3500
m9=1000
m10=1400

h1 = easyxf(
    'font:name Arial, bold on,height 1000 ;align: vert centre, horz center')
h2 = easyxf(
    'font:name Times New Roman, bold on,height 1000 ;align: vert centre, horz center')
h3 = easyxf(
    'font:name Times New Roman, bold on,height 400 ;align: vert centre, horz center')
h4 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;'
'borders : top thin ,right thin, left thin, bottom thin')
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

def printASubject(class_id,s,mon,x,y):
    if mon==u'Ngoại ngữ':
        s.write_merge(x,x,y,y+4,'NGOẠI NGỮ:...........................................',h4)        
    else:    
        s.write_merge(x,x,y,y+4,mon.upper(),h4)
            
    
    s.write_merge(x+1,x+1,y,y+1,u'Điểm hs 1',h5)
    s.write_merge(x+1,x+2,y+2,y+2,u'Điểm hs 2\n(V)',h5)
    s.write_merge(x+1,x+2,y+3,y+3,u'KT\nhk',h5)
    s.write_merge(x+1,x+2,y+4,y+4,u'TBm',h5)
    

    s.write(x+2,y,u'M',h5)
    s.write(x+2,y+1,u'v',h5)
    
    monList    = Mark .objects.filter(student_id__class_id=class_id,subject_id__name=mon,term_id__number=1).order_by("student_id__index")

    i=0    
    for m in monList:
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
            s.write(x+i+2,y,str1,h6)
            s.write(x+i+2,y+1,str2,h6)
            s.write(x+i+2,y+2,str3,h6)
            s.write(x+i+2,y+3,str4,h6)
            s.write(x+i+2,y+4,str5,h6)
        else:    
            s.write(x+i+2,y,str1,h7)
            s.write(x+i+2,y+1,str2,h7)
            s.write(x+i+2,y+2,str3,h7)
            s.write(x+i+2,y+3,str4,h7)
            s.write(x+i+2,y+4,str5,h7)

    for t in range(i+1,56):
        if t % 5!=0:
            for j in range(y,y+5):    
                s.write(x+t+2,j,"",h6)
        else:    
            for j in range(y,y+5):    
                s.write(x+t+2,j,"",h7)
def printName(class_id,s,x,y):     
    
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('index')
    i=0
    for p in pupilList:
        if i % 5 !=0:
            s.write(x+i,y,i+1,h6)
            s.write(x+i,y+1,p.last_name,last_name)
            s.write(x+i,y+2,p.first_name,first_name)
        else:    
            s.write(x+i,y,i+1,h7)
            s.write(x+i,y+1,p.last_name,last_name1)
            s.write(x+i,y+2,p.first_name,first_name1)
        i +=1
        
    for t in range(i+1,56):
        if t % 5 !=0:
            s.write(x+t-1,y,t,h6)
            s.write(x+t-1,y+1,"",last_name)
            s.write(x+t-1,y+2,"",first_name)
        else:    
            s.write(x+t-1,y,t,h7)
            s.write(x+t-1,y+1,"",last_name1)
            s.write(x+t-1,y+2,"",first_name1)
            
def printPage13(book):
    s = book.add_sheet('trang 13')
    s.set_paper_size_code(8)
    s.write_merge(24,24,0,13,u'PHẦN GHI ĐIỂM',h1)
    s.write_merge(25,25,0,13,u'HỌC KỲ I',h2)
    
def printPage14(book,class_id,number,mon1,mon2):
    s = book.add_sheet('trang'+str(number+13) ,True)
    book.set_active_sheet(number)
    s.set_paper_size_code(8)
        
    s.col(0).width = s1
    s.col(1).width = s2
    s.col(2).width = s3
    s.col(3).width = m1
    s.col(4).width = m2
    s.col(5).width = m3
    s.col(6).width = m4
    s.col(7).width = m5
    
    s.col(8).width  = m6
    s.col(9).width  = m7
    s.col(10).width = m8
    s.col(11).width = m9
    s.col(12).width = m10
    
    s.write_merge(0,0,0,12,u'HỌC KỲ I',h3)
    
    s.write_merge(1,3,0,0,u'Số\nTT',h4)
    s.write_merge(1,3,1,2,u'Họ và tên',h4)
            
    printName(class_id,s,4,0)        
    printASubject(class_id,s,mon1,1,3)
    printASubject(class_id,s,mon2,1,8)
    
    max = 55
                
    s.write_merge(max+5,max+5,0,8,u'Trong trang này có......... điểm được sửa chữa,'+
u' trong đó môn: '+ mon1+u'....... điểm, '+ mon2+u'.......điểm',h8)
    
    s.write_merge(max+5,max+5,9,12,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,9,12,u'giáo viên chủ nhiệm',h9)
        
def printPage15(book,class_id,number,mon1,mon2,mon3):
    s = book.add_sheet('trang'+str(number+13) ,True)
    book.set_active_sheet(number)
    s.set_paper_size_code(8)
        
    s.col(0).width = s1
    
    s.col(1).width = m6
    s.col(2).width = m7
    s.col(3).width = m8
    s.col(4).width = m9
    s.col(5).width = m10
    
    s.col(6).width = m6
    s.col(7).width = m7
    s.col(8).width = m8
    s.col(9).width = m9
    s.col(10).width = m10

    s.col(11).width = m6
    s.col(12).width = m7
    s.col(13).width = m8
    s.col(14).width = m9
    s.col(15).width = m10
    
    s.write_merge(0,0,0,15,u'HỌC KỲ I',h3)    
    s.write_merge(1,3,0,0,u'Số\nTT',h4)
        
    printASubject(class_id,s,mon1,1,1)
    printASubject(class_id,s,mon2,1,6)
    printASubject(class_id,s,mon3,1,11)
    
    
    max=55
    
    s.write_merge(max+5,max+5,0,11,u'Trong trang này có......... điểm được sửa chữa,'+
u' trong đó môn: '+ mon1+u'....... điểm, '+ mon2+u'.......điểm, '+mon3+u'.......điểm',h8)

    s.write_merge(max+6,max+6,0,11,u'Ghi chú: số TT ở trang này là số TT ở trang '+str(number+12),h8)
    
    s.write_merge(max+5,max+5,12,15,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,12,15,u'giáo viên chủ nhiệm',h9)


    
def markBookClass(class_id):
    #student_list = _class.pupil_set.all().order_by('index')
    book = Workbook(encoding = 'utf-8')
    printPage13(book)
    printPage14(book,class_id,1,u'Toán',u'Vật lí')    
    printPage15(book,class_id,2,u'Hóa học',u'Sinh học',u'Tin học')    
    printPage14(book,class_id,3,u'Ngữ văn',u'Lịch sử')
    printPage15(book,class_id,4,u'Địa lí',u'Ngoại ngữ',u'GDCD')    
    printPage15(book,class_id,5,u'NN2',u'Nghề phổ thông(lớp 11)',u'....................................')    
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
