# -*- coding: utf-8 -*-
#from school.views import *

from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
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
from school.templateExcel import *

def normalize(x,checkNx,isRound=None):
    if checkNx==0:
        if isRound:
            return str(x)
        if x-int(x)<e:
            return str(int(x))
        else:
            return str(x)
    else:
        if x>=9:
            return u'G'
        elif x>=7:
            return u'K'
        elif x>=6:
            return u'TB'
        elif x>=4:
            return u'Y'
        elif x>=0:
            return u'Kem'
        else:
            return  u''   
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

def printASubject(class_id,termNumber,s,mon,x,y,ls,number):
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
    
    monList    = Mark .objects.filter(student_id__classes=class_id,subject_id__name=mon,term_id__number=termNumber).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')

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
            s.write(x+i+2,y+3,str4,h61)
            s.write(x+i+2,y+4,str5,h61)
            ls.write(i+3,number+2,str5,h61)
        else:    
            s.write(x+i+2,y,str1,h7)
            s.write(x+i+2,y+1,str2,h7)
            s.write(x+i+2,y+2,str3,h7)
            s.write(x+i+2,y+3,str4,h71)
            s.write(x+i+2,y+4,str5,h71)
            ls.write(i+3,number+2,str5,h71)
            
    for t in range(i+1,56):
        if t % 5!=0:
            for j in range(y,y+5):    
                s.write(x+t+2,j,"",h6)
                ls.write(t+3,number+2,"",h6)
        else:    
            for j in range(y,y+5):    
                s.write(x+t+2,j,"",h7)
                ls.write(t+3,number+2,"",h7)
                
def printName(class_id,s,x,y,mode=0):     
    
    if mode==0 :
        s.write_merge(x,x+2,y,y,u'Số\nTT',h4)
        s.write_merge(x,x+2,y+1,y+2,u'Họ và tên',h4)
    else:    
        s.write_merge(x,x+3,y,y,u'Số\nTT',h4)
        s.write_merge(x,x+3,y+1,y+2,u'Họ và tên',h4)
        x=x+1
    
    pupilList = Pupil.objects.filter(classes=class_id,attend__is_member=True).order_by('index','first_name','last_name','birthday')
    i=0
    for p in pupilList:
        i +=1
        if i % 5 !=0:
            s.write(x+i+2,y,i,h6)
            s.write(x+i+2,y+1,p.last_name,last_name)
            s.write(x+i+2,y+2,p.first_name,first_name)
        else:    
            s.write(x+i+2,y,i,h7)
            s.write(x+i+2,y+1,p.last_name,last_name1)
            s.write(x+i+2,y+2,p.first_name,first_name1)
        
    for t in range(i+1,56):
        if t % 5 !=0:
            s.write(x+t+2,y,t,h6)
            s.write(x+t+2,y+1,"",last_name)
            s.write(x+t+2,y+2,"",first_name)
        else:    
            s.write(x+t+2,y,t,h7)
            s.write(x+t+2,y+1,"",last_name1)
            s.write(x+t+2,y+2,"",first_name1)
                
def printPage13(s,x,y,string):    
    s.write_merge(x+23,x+27,y,y+12,u'PHẦN GHI ĐIỂM',h1)
    s.write_merge(x+28,x+33,y,y+12,string,h2)
    
def printPage14(class_id,s,termNumber,n1,mon1,mon2,x,y,ls):
            
    s.col(0).width = s1
    s.col(1).width = s2
    s.col(2).width = s3
    
    s.col(3).width = m1
    s.col(4).width = m2
    s.col(5).width = m3
    s.col(6).width = m4
    s.col(7).width = m5
    
    s.col(8).width  = m1
    s.col(9).width  = m2
    s.col(10).width = m3
    s.col(11).width = m4
    s.col(12).width = m5
    
    if termNumber==1:
        s.write_merge(x,x,y,y+12,u'HỌC KỲ I',h3)
    else:    
        s.write_merge(x,x,y,y+12,u'HỌC KỲ II',h3)
    
    printName(class_id,s,x+1,y)        
    printASubject(class_id,termNumber,s,mon1,x+1,y+3,ls,2*n1+1)
    printASubject(class_id,termNumber,s,mon2,x+1,y+8,ls,2*n1+2)
    
    max = 55
    str =u'Trong trang này có......... điểm được sửa chữa,'+u' trong đó môn: '+ mon1+u'....... điểm'
    if mon2!=noneSubject:
        str+=', '+ mon2+u'.......điểm'       
    print x+max+5
    print y+max+5          
    s.write_merge(x+max+5,x+max+5,y+0,y+8,str,h8)
    
    s.write_merge(x+max+5,x+max+5,y+9,y+12,u'Ký xác nhận của',h9)
    s.write_merge(x+max+6,x+max+6,y+9,y+12,u'giáo viên chủ nhiệm',h9)
        
def printPage20(class_id,termNumber,s,length,subjectList):
    s.set_paper_size_code(8)
    s.col(0).width = s1
    s.col(1).width = s2
    s.col(2).width = s3
    for i in range(length):
        s.col(i+3).width =d1
        
    s.col(length+3).width = d1
    s.col(length+4).width = d1
    s.col(length+5).width = d1
    s.col(length+6).width = d1+500
    
    if termNumber==1:
        s.write_merge(0,0,0,length+6,u'TỔNG HỢP KẾT QUẢ HỌC KỲ I',h3)
    else:    
        s.write_merge(0,0,0,length+6,u'TỔNG HỢP KẾT QUẢ HỌC KỲ II',h3)
        
    for (i,ss) in enumerate(subjectList):
        if ss.name=='GDCD':
            s.write_merge(1,3,i+3,i+3,'GD\nCD',h10)
        elif ss.name=='GDQP-AN':     
            s.write_merge(1,3,i+3,i+3,'GD\nQP-\nAN',h10)
        else:    
            s.write_merge(1,3,i+3,i+3,ss.name,h10)
            
    s.write_merge(1,3,length+3,length+3,'TB',h10)
    s.write_merge(1,2,length+4,length+6,u'Kết quả xếp loại\n và thi đua',h10)
 
    s.write(3,length+4,u'HL',h10)
    s.write(3,length+5,u'HK',h10)
    s.write(3,length+6,u'TĐ',h10)
    
    
    selectedClass = Class.objects.get(id=class_id)
    
    tbhkList = TBHocKy.objects.filter(student_id__classes=class_id,term_id__number=termNumber)
    hkList   = TBNam.objects.filter(student_id__classes=class_id,year_id=selectedClass.year_id)
    
    i=-1
    for (i,(tbhk,hk)) in enumerate(zip(tbhkList,hkList)):
        str1=""
        if tbhk.tb_hk!=None: str1 = str(tbhk.tb_hk)
        str2=""                                
        if tbhk.tb_hk!=None: str2 = str(tbhk.hl_hk)
        str3=""
        if termNumber==1:
            if hk.term1!=None  : str3 = hk.term1
        else:    
            if hk.term2!=None  : str3 = hk.term2
        str4=""
        if   tbhk.danh_hieu_hk=='G' : str4='HSG'
        elif tbhk.danh_hieu_hk=='TT': str4='HSTT'
        
        if i % 5!=4:            
            s.write(i+4,length+3,str1,h61)                         
            s.write(i+4,length+4,str2,h61)                         
            s.write(i+4,length+5,str3,h61)                         
            s.write(i+4,length+6,str4,h61)
        else:                             
            s.write(i+4,length+3,str1,h71)                         
            s.write(i+4,length+4,str2,h71)                         
            s.write(i+4,length+5,str3,h71)                         
            s.write(i+4,length+6,str4,h71)
    
    for t in range(i+2,56):
        if t % 5!=0:            
            s.write(t+3,length+3,"",h6)                         
            s.write(t+3,length+4,"",h6)                         
            s.write(t+3,length+5,"",h6)                         
            s.write(t+3,length+6,"",h6)
        else:                             
            s.write(t+3,length+3,"",h7)                         
            s.write(t+3,length+4,"",h7)                         
            s.write(t+3,length+5,"",h7)                         
            s.write(t+3,length+6,"",h7)
                 
    printName(class_id,s,1,0)
    max = 55
    str1 =u'Trong trang này có......... điểm được sửa chữa,'+u' trong đó môn:........................................................................... '
    str2 ='........................................................................................................................................................................'
    s.write_merge(max+5,max+5,0,16,str1,h8)
    s.write_merge(max+6,max+6,0,16,str2,h8)
    
    s.write_merge(max+5,max+5,17,21,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,17,21,u'giáo viên chủ nhiệm',h9)

def printPage31(class_id,s,tbNamList,x,y):
        
    s.col(y+0).width = s1
    s.col(y+1).width = s2
    s.col(y+2).width = s3
    for i in range(3,12):
        s.col(y+i).width =d2
        if (i==7) | (i==10):         
            s.col(y+i).width =d2+500

    s.col(y+12).width =d3
    
    printName(class_id,s,x+1,y,1)
                
    s.write_merge(x+0,x+0,y,y+12,u'TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ, XẾP LOẠI CẢ NĂM HỌC',h3)
    s.write_merge(x+1,x+2,y+3,y+4,u'XẾP LOẠI',h10)
    s.write_merge(x+3,x+4,y+3,y+3,'HL',h10)
    s.write_merge(x+3,x+4,y+4,y+4,'HK',h10)
    s.write_merge(x+1,x+4,y+5,y+5,u'TS ngày\n nghỉ học',h10)
    s.write_merge(x+1,x+4,y+6,y+6,u'Được\n lên lớp',h10)
    s.write_merge(x+1,x+4,y+7,y+7,u'Ở lại lớp, KT lại, rèn luyện HK trong hè',h10)
    s.write_merge(x+1,x+2,y+8,y+10,u'Xếp loại lại về HK, HL, sau KT lại các môn học hoặc rèn luyện về HK',h10)
    s.write_merge(x+3,x+4,y+8,y+8,u'HL',h10)
    s.write_merge(x+3,x+4,y+9,y+9,u'HK',h10)
    s.write_merge(x+3,x+4,y+10,y+10,u'Lên lớp, ở lại lớp',h10)    
    s.write_merge(x+1,x+4,y+11,y+11,u'Danh hiệu\n HSG,\nHSTT',h10)
    s.write_merge(x+1,x+4,y+12,y+12,u'TỔNG HỢP CHUNG',h10)
    
    #hanhKiemList =HanhKiem.objects.filter(student_id__classes=class_id).order_by('student_id__index')
    llSauHe=0
    for (i,(tbNam)) in enumerate(tbNamList):
        if i % 5 != 4: h=h6
        else         : h=h7
        str1=''
        if tbNam.hl_nam!=None:           str1 = tbNam.hl_nam
                
        str2=''
        if tbNam.year!=None:   str2= tbNam.year
        
        str3=''
        if tbNam.tong_so_ngay_nghi!=None: str3 =tbNam.tong_so_ngay_nghi
         
        str4=''
        if (tbNam.len_lop==True) &(tbNam.thi_lai==None) & (tbNam.hk_ren_luyen_lai==None):
            str4='Lên lớp'
        
        str5=''
        if   tbNam.thi_lai       :str5='KT lại'
        elif tbNam.ren_luyen_lai    :str5='rèn luyện trong hè' 
        elif tbNam.len_lop==False:str5='Ở lại lớp'
        
        str6=''
        if tbNam.hl_thi_lai    :str6=tbNam.hl_thi_lai
         
        str7=''
        if tbNam.hk_ren_luyen_lai!=None: str7= tbNam.hk_ren_luyen_lai
        
        str8=''
        if (tbNam.ren_luyen_lai!=None) | (tbNam.thi_lai!=None):
            if   tbNam.len_lop==True : 
                str8='Lên lớp'
                llSauHe+=1
            elif tbNam.len_lop==False: str8='Ở lại lớp'
        
        str9=''
        if (tbNam.danh_hieu_nam != None) & (tbNam.danh_hieu_nam != 'K'):
            str9='HS'+tbNam.danh_hieu_nam
        
        
        s.write(x+i+5,y+3,str1,h)
        s.write(x+i+5,y+4,str2,h)
        s.write(x+i+5,y+5,str3,h)
        s.write(x+i+5,y+6,str4,h)
        s.write(x+i+5,y+7,str5,h)
        s.write(x+i+5,y+8,str6,h)
        s.write(x+i+5,y+9,str7,h)
        s.write(x+i+5,y+10,str8,h)
        s.write(x+i+5,y+11,str9,h)
        
    for tt in range(i+1,55):
        if tt % 5 != 4: h=h6
        else         : h=h7        
        for j in range(3,12):
            s.write(x+tt+5,y+j,'',h)
    sl1= tbNamList.filter(len_lop=True ).count()
    sl2= tbNamList.filter(len_lop=False).count()
    
    for i in range(55):
        s.write(x+i+5,y+12,'',h81)
    s.write(x+54+5,y+12,'',h71)    
    s.write(x+7,y+12,'Tổng số học sinh: '+str(len(tbNamList)),h81)
    s.write(x+10,y+12,'-Được lên lớp: '+str(sl1),h81)        
    s.write(x+12,y+12,'-Ở lại lớp:'+str(sl2),h81)
    s.write_merge(x+14,x+17,y+12,y+12,'-Được lên lớp sau khi kiểm tra lại các môn học hoặc rèn luyện trong hè: '+str(llSauHe),h81)        
    s.write(x+20,y+12,'Giáo viên chủ nhiệm',h91)        
    s.write(x+21,y+12,'(Ký và ghi rõ họ, tên)',hh1)        
    s.write(x+30,y+12,'Hiệu trưởng',h91)        
    s.write(x+31,y+12,'(Ký tên, đóng dấu)',hh1)        
    
def printPage30(class_id,book):
    subjectList =Subject.objects.filter(class_id=class_id).order_by("index",'name')
    length = len(subjectList)
    s = book.add_sheet('XL cả năm',True)
    s.set_paper_size_code(8)
    s.col(0).width = s1
    s.col(1).width = s2
    s.col(2).width = s3
    for i in range(length):
        s.col(i+3).width =d1
        
    s.col(length+3).width = d1
    s.col(length+4).width = d1
    s.col(length+5).width = d1
    s.col(length+6).width = d1
    
    s.vert_page_breaks = [(length+8,0,65500)]    
    s.horz_page_breaks = []
    
    s.write_merge(0,0,0,length+6,u'TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ, XẾP LOẠI CẢ NĂM HỌC',h3)

    printName(class_id,s,1,0,1)            
    for (i,ss) in enumerate(subjectList):
        if ss.name=='GDCD':
            s.write_merge(1,4,i+3,i+3,'GD\nCD',h10)
        elif ss.name=='GDQP-AN':     
            s.write_merge(1,4,i+3,i+3,'GD\nQP-\nAN',h10)
        else:    
            s.write_merge(1,4,i+3,i+3,ss.name,h10)
            
    s.write_merge(1,4,length+3,length+3,'TB\ncmcn',h10)
    s.write_merge(1,2,length+4,length+6,u'Điểm KT lại',h10)
    
    s.write_merge(3,4,length+4,length+4,'',h10)
    s.write_merge(3,4,length+5,length+5,'',h10)
    s.write_merge(3,4,length+6,length+6,'',h10)
    
    markList = TKMon.objects.filter(subject_id__class_id=class_id,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    numberPupil = Pupil.objects.filter(classes=class_id,attend__is_member=True).count()
    for (t,m) in enumerate(markList):
        
        i = t % length
        j = int(t/length)
        if i==0 : tt=0
        str1 ="" 
        if m.tb_nam !=None: str1 =str(m.tb_nam)  
        if j % 5!=4:            
            s.write(j+5,i+3,str1,h61)
            if m.diem_thi_lai!=None:
                tt+=1
                s.write(j+5,length+3+tt,str(m.diem_thi_lai),h61)
        else:     
            s.write(j+5,i+3,str1,h71)
            if m.diem_thi_lai!=None:
                tt+=1
                s.write(j+5,length+3+tt,str(m.diem_thi_lai),h71)
        
        if i==length-1:
            if j % 5!=4:            
                for ii in range(tt,3):
                    s.write(j+5,length+4+ii," ",h61)
                    
            else:        
                for ii in range(tt,3):
                    s.write(j+5,length+4+ii," ",h71)
    
    for i in range(numberPupil,55):
        for j in range(length+4):           
           if i % 5!=4:            
               s.write(i+5,j+3,'',h61)
           else:     
               s.write(i+5,j+3,'',h71)
               
    tbNamList = TBNam.objects.filter(student_id__classes=class_id).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    for (i,tbNam) in enumerate(tbNamList):
        str1 ="" 
        if tbNam.tb_nam !=None: str1 =str(tbNam.tb_nam)  
        if i % 5!=4:            
            s.write(i+5,length+3,str1,h61)
        else:     
            s.write(i+5,length+3,str1,h71)

        for tt in range(i+1,55):
            if tt % 5!=4:            
                s.write(tt+5,length+3,'',h61)
            else:     
                s.write(tt+5,length+3,'',h71)
    
    printPage31(class_id,s,tbNamList,0,length+8)
    max = 55
    str1=u'Trong trang này có ... điểm được sửa chữa, trong đó môn:'
    for ss in subjectList:
        str1+=ss.name+u'.......điểm, '
    str1 = str1[:len(str1)-2]+'.'
    s.write_merge(max+5,max+8,0,length,str1,h8)
    
    s.write_merge(max+5,max+5,length+1,length+6,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,length+1,length+6,u'giáo viên chủ nhiệm',h9)
    
def printInTerm(class_id,book,termNumber):

    subjectList = Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber,3,4]).order_by('index','name')    
    length = len(subjectList)
    numberPage = int((length+1)/2+1)
    
    if termNumber ==1:
        s  = book.add_sheet('Điểm HK I',True)
        ls = book.add_sheet('THKQ I',True)
    else:
        s = book.add_sheet('Điểm HK II',True)    
        ls = book.add_sheet('THKQ II',True)
    
             
    if termNumber == 1 :  printPage13(s,0,0,u'HỌC KỲ I')
    else               :  printPage13(s,0,0,u'HỌC KỲ II')
        
    s.set_paper_size_code(8)
    setHorz =[]
    
    for i in range(numberPage):
        setHorz.append(((i+1)*70,0,255))
    s.vert_page_breaks =[]    
    s.horz_page_breaks = setHorz
            
    for i in range(length/2):
        printPage14(class_id,s,termNumber,i,subjectList[2*i].name,subjectList[2*i+1].name,(i+1)*70,0,ls)
    i+=1     
    if length % 2==1:
        printPage14(class_id,s,termNumber,i,subjectList[2*i].name,noneSubject,(i+1)*70,0,ls)
    
    printPage20(class_id,termNumber,ls,length,subjectList)

def markBookClass(class_id):
    tt1 = time.time()
    book = Workbook(encoding = 'utf-8')
        
    printInTerm(class_id,book,1)
    printInTerm(class_id,book,2)
    printPage30(class_id,book)
    book.set_active_sheet(0)
    selectedClass=Class.objects.get(id=class_id)
    response = HttpResponse(mimetype='application/ms-excel')
    name = 'soGhiDiemGoiTen%s.xls' % unicode(selectedClass.name)
    name1=name.replace(' ','_')
    response['Content-Disposition'] = u'attachment; filename=%s' % name1
    book.save(response)
    tt2= time.time()
    print (tt2-tt1)
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
    printSTT(s,55,4,0)
    
    max=55
    
    s.write_merge(max+5,max+5,0,11,u'Trong trang này có......... điểm được sửa chữa,'+
u' trong đó môn: '+ mon1+u'....... điểm, '+ mon2+u'.......điểm, '+mon3+u'.......điểm',h8)

    s.write_merge(max+6,max+6,0,11,u'Ghi chú: số TT ở trang này là số TT ở trang '+str(number+12),h8)
    
    s.write_merge(max+5,max+5,12,15,u'Ký xác nhận của',h9)
    s.write_merge(max+6,max+6,12,15,u'giáo viên chủ nhiệm',h9)


def printSTT(s,max,x,y):
    for t in range(1,max+1):
        if t % 5 !=0:
            s.write(x+t-1,y,t,h6)
        else:    
            s.write(x+t-1,y,t,h7)
        


def markExcel(request,term_id,subject_id):
    tt1 = time.time()

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    
    selectedSubject = Subject.objects.get(id=subject_id)
    try:        
        if in_school(request,selectedSubject.class_id.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    position= get_position(request)
    if position==4:
        pass
    elif position ==3:
        if (selectedSubject.teacher_id.id != request.user.teacher.id):  
            return HttpResponseRedirect('/school')
    else:    
            return HttpResponseRedirect('/school')

    
    selectedTerm   = Term.objects.get(id=term_id)
    book = Workbook(encoding = 'utf-8')
    str1=u'BẢNG ĐIỂM LỚP '+selectedSubject.class_id.name.upper()+u' MÔN '+selectedSubject.name.upper()+u'  HỌC KỲ'    
    if selectedTerm.number==1:
        str1+=' I'
    else:
        str1+=' II'  
              
    str3 =selectedSubject.class_id.name+'_'+selectedSubject.name+'_HK'+str(selectedTerm.number)       
    sstr2='bang_diem_'+str3
    sstr2=sstr2.replace(' ','_')  
    s=book.add_sheet(str3,True)
    if selectedTerm.number==1: numberCol=21
    else                     : numberCol=23
    s.set_portrait(0)
    s.col(0).width=s1
    s.col(1).width=s2
    s.col(2).width=s3
    s.col(3).width=s4
    
    size = (SIZE_PAGE_WIDTH-s1-s2-s3-s4)/(numberCol-4) 
    for i in range(4,numberCol):
        s.col(i).width = size
    s.set_top_margin(0)  
    s.row(0).hidden=True
    s.row(1).hidden=True
    s.row(2).hidden=True
    str2 = 'Năm học '+ str(selectedTerm.year_id.time)+'-'+str(selectedTerm.year_id.time+1)   
    s.write_merge(4,4,0,19,str1,h9 )
    s.write_merge(5,5,0,19,str2,h9 )
    
    s.write_merge(8,10,0,0,u'Số\nTT',h4)
    s.write_merge(8,10,1,2,u'Họ và tên',h4)
    s.write_merge(8,10,3,3,u'Ngày sinh',h4)
    s.write_merge(8,9,4,8,u'Điểm hs 1-Miệng',h4)
    s.write_merge(8,9,9,13,u'Điểm hs 1-Viết',h4)
    s.write_merge(8,9,14,18,u'Điểm hs 2',h4)
    s.write_merge(8,10,19,19,u'Thi ck',h4)
    for i in range(15):
        s.write(10,i+4,(i % 5) +1,h4)
    if selectedTerm.number ==1:
        s.write_merge(8,10,20,20,'TB',h4)
    else:
        s.write_merge(8,9,20,22,'TB',h4)
        s.write(10,20,'HK I',h4)    
        s.write(10,21,'HK II',h4)    
        s.write(10,22,'CN',h4)   
        hk1List =  Mark.objects.filter(subject_id=subject_id,term_id__number=1,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday') 
        cnList  =  TKMon.objects.filter(subject_id=subject_id,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    markList = Mark.objects.filter(subject_id=subject_id,term_id=term_id,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    if selectedSubject.nx==True:
        checkNx=1
    else:
        checkNx=0
            
    for (i,m) in enumerate(markList):
        strs=['']*20
        if i % 5 !=4: h=h61
        else        : h=h71
        
        strs[0] =m.student_id.birthday.strftime('%d/%m/%Y')       
        if m.mieng_1!=None: strs[1]=normalize(m.mieng_1,checkNx)
        if m.mieng_2!=None: strs[2]=normalize(m.mieng_2,checkNx)
        if m.mieng_3!=None: strs[3]=normalize(m.mieng_3,checkNx)
        if m.mieng_4!=None: strs[4]=normalize(m.mieng_4,checkNx)
        if m.mieng_5!=None: strs[5]=normalize(m.mieng_5,checkNx)
        if m.mlam_1 !=None: strs[6]=normalize(m.mlam_1,checkNx)
        if m.mlam_2 !=None: strs[7]=normalize(m.mlam_2,checkNx)
        if m.mlam_3 !=None: strs[8]=normalize(m.mlam_3,checkNx)
        if m.mlam_4 !=None: strs[9]=normalize(m.mlam_4,checkNx)
        if m.mlam_5 !=None: strs[10]=normalize(m.mlam_5,checkNx)
        if m.mot_tiet_1!=None: strs[11]=normalize(m.mot_tiet_1,checkNx)
        if m.mot_tiet_2!=None: strs[12]=normalize(m.mot_tiet_2,checkNx)
        if m.mot_tiet_3!=None: strs[13]=normalize(m.mot_tiet_3,checkNx)
        if m.mot_tiet_4!=None: strs[14]=normalize(m.mot_tiet_4,checkNx)
        if m.mot_tiet_5!=None: strs[15]=normalize(m.mot_tiet_5,checkNx)        
        if m.ck!=None: strs[16]=normalize(m.ck,checkNx)
        if m.tb!=None: strs[17]=normalize(m.tb,checkNx,1)
        
        if selectedTerm.number==2:
            strs[18]=strs[17]
            strs[17]=''
            if hk1List[i].tb!=None    :strs[17]=normalize(hk1List[i].tb,checkNx,1)
            if cnList[i].tb_nam!=None :strs[19]=normalize(cnList[i].tb_nam,checkNx,1)
        
        s.write(11+i,0,i+1,h)
        if i % 5!=4:
            s.write(11+i,1,m.student_id.last_name,last_name)
            s.write(11+i,2,m.student_id.first_name,first_name)
        else:    
            s.write(11+i,1,m.student_id.last_name,last_name1)
            s.write(11+i,2,m.student_id.first_name,first_name1)
            
        for j in range(numberCol-3):
            s.write(11+i,3+j,strs[j],h)
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename=%s.xls' % to_en1(sstr2)
    book.save(response)
    tt2= time.time()
    print (tt2-tt1)
    print to_en1(str1)
    return response

def count1Excel(year_id,number,list,sumsumsum,allList):
    tt1 = time.time()
    
    book = Workbook(encoding = 'utf-8')
    selectedYear = Year.objects.get(id=year_id)
    if number==1:
        str1='HKI'
        str2=u'HỌC KỲ I NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    elif number==2:
        str1='HKII'
        str2=u'HỌC KỲ II NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    else:
        str1='CaNam'        
        str2=u'CẢ NĂM NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    sheetName ='tkHocLuc'+str1+str(selectedYear.time)+'-'+str(selectedYear.time+1) 
    s=book.add_sheet(sheetName,True)
    s.set_portrait(0)
    s.col(0).width=s1    
    s.col(1).width=s2-s1    
    size = (SIZE_PAGE_WIDTH-s2)/23 
    for i in range(2,25):
        if i % 2==1:
            s.col(i).width = size-100
        else:    
            s.col(i).width = size+100
    
    s.write_merge(2,2,0,24,'THỐNG KÊ HỌC LỰC, HẠNH KIỂM, DANH HIỆU',h40)
    s.write_merge(3,3,0,24,str2,h40)
    x=5
    y=1    
    s.write_merge(x,x+2,y-1,y-1,u'STT',h4)    
    s.write_merge(x,x+2,y,y,u'Lớp',h4)    
    s.write_merge(x,x+2,y+1,y+1,u'Sĩ\nSố',h4)    
    s.write_merge(x,x,y+2,y+11,u'Học lực',h4)    
    s.write_merge(x,x,y+12,y+19,u'Hạnh kiểm',h4)    
    s.write_merge(x,x,y+20,y+23,u'Danh hiệu',h4)
        
    s.write_merge(x+1,x+1,y+2,y+3,'Giỏi',h4)
    s.write_merge(x+1,x+1,y+4,y+5,'Khá',h4)
    s.write_merge(x+1,x+1,y+6,y+7,'TB',h4)
    s.write_merge(x+1,x+1,y+8,y+9,'Yếu',h4)
    s.write_merge(x+1,x+1,y+10,y+11,'Kém',h4)
    
    s.write_merge(x+1,x+1,y+12,y+13,'Tốt',h4)
    s.write_merge(x+1,x+1,y+14,y+15,'Khá',h4)
    s.write_merge(x+1,x+1,y+16,y+17,'TB',h4)
    s.write_merge(x+1,x+1,y+18,y+19,'Yếu',h4)
    
    s.write_merge(x+1,x+1,y+20,y+21,'HSTT',h4)
    s.write_merge(x+1,x+1,y+22,y+23,'HSG',h4)
    for i in range(11):
        s.write(x+2,y+2*i+2,'sl',h4)
        s.write(x+2,y+2*i+3,'%' ,h4)
    
    
    i=0
    for b,sum,total,list1 in list:
        stt=0
        for name,ss,l in list1:
            i+=1
            stt+=1                
            s.write(x+i+2,y-1,stt,h82)
            s.write(x+i+2,y,name,h82)
            s.write(x+i+2,y+1,ss,h72)
            j=0
            for u,v in l :
                v=round(v+e, 2)
                s.write(x+i+2,y+2*j+2,u,h72)
                s.write(x+i+2,y+2*j+3,v,h73)
                j+=1
                
        i+=1
        str11=u'Khối '+str(b.number)
        s.write(x+i+2,y-1,'',h41)
        s.write(x+i+2,y,str11,h41)
        s.write(x+i+2,y+1,sum,h72)        
        j=0
        for u,v in total:
            v=round(v+e, 2)                            
            s.write(x+i+2,y+2*j+2,u,h72)
            s.write(x+i+2,y+2*j+3,v,h73)
            j+=1
        i+=1
        s.write(x+i+2,y-1,'',h41)
        s.write(x+i+2,y,'',h5)
        s.write(x+i+2,y+1,'',h72)        
        j=0
        for u,v in total:
            s.write(x+i+2,y+2*j+2,'',h72)
            s.write(x+i+2,y+2*j+3,'',h72)
            j+=1
    i+=1    
    s.write(x+i+2,y,u'Toàn trường',h41)
    s.write(x+i+2,y+1,sumsumsum,h72)
    j=0
    for u,v in allList:
        v=round(v+e, 2)        
        s.write(x+i+2,y+2*j+2,u,h72)
        s.write(x+i+2,y+2*j+3,v,h73)
        j+=1  
        
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename=%s.xls' % sheetName
    book.save(response)
    tt2= time.time()
    print (tt2-tt1)
    return response

def count2Excel(year_id,number,subjectName,type,modeView,list,allList,sumsumsum):
    tt1 = time.time()
    
    book = Workbook(encoding = 'utf-8')
    selectedYear = Year.objects.get(id=year_id)
    if number==1:
        str1='HKI'
        str2=u'HỌC KỲ I NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    elif number==2:
        str1='HKII'
        str2=u'HỌC KỲ II NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    else:
        str1='CaNam'        
        str2=u'CẢ NĂM NĂM HỌC '+str(selectedYear.time)+'-'+str(selectedYear.time+1)
    if   (type==1) & (modeView==1):
        str3='TBTheoLop'        
        titleString=u'THỐNG KÊ ĐIỂM TRUNG BÌNH THEO LỚP-MÔN '+unicode(subjectName.upper()) 
    elif (type==1) & (modeView==2):
        str3='TBTheoGiaoVien'        
        titleString=u'THỐNG KÊ ĐIỂM TRUNG BÌNH THEO GIÁO VIÊN-MÔN '+unicode(subjectName.upper())
    elif (type==2) & (modeView==1):      
        str3='ThiTheoLop'        
        titleString=u'THỐNG KÊ ĐIỂM THI CUỐI KÌ THEO LỚP-MÔN '+unicode(subjectName.upper()) 
    elif (type==2) & (modeView==2):      
        str3='ThiTheoGiaoVien'        
        titleString=u'THỐNG KÊ ĐIỂM THI CUỐI KÌ THEO GIÁO VIÊN-MÔN '+unicode(subjectName.upper())
         
    sheetName ='tkDiem'+str3+str1+str(selectedYear.time)+'-'+str(selectedYear.time+1) 
    s=book.add_sheet('tkDiem',True)
    s.set_portrait(0)
    s.col(0).width=s1    
    size = (SIZE_PAGE_WIDTH-s1)/16 
    s.col(1).width=2*size
    s.col(2).width=size
    s.col(3).width=3*size    
    for i in range(4,13):
        if i % 2==1:
            s.col(i).width = size-100
        else:    
            s.col(i).width = size+100
            
    s.write_merge(2,2,0,12,titleString,h40)
    s.write_merge(3,3,0,12,str2,h40)
    x=5
    y=1    
    s.write_merge(x,x+2,y-1,y-1,u'STT',h4)    
    s.write_merge(x,x+2,y,y,u'Lớp',h4)    
    s.write_merge(x,x+2,y+1,y+1,u'Sĩ\nSố',h4)    
    s.write_merge(x,x+2,y+2,y+2,u'Giáo viên\ngiảng dạy',h4)    
    s.write_merge(x,x,y+3,y+12,u'Học lực',h4)    
        
    s.write_merge(x+1,x+1,y+3,y+4,'Giỏi',h4)
    s.write_merge(x+1,x+1,y+5,y+6,'Khá',h4)
    s.write_merge(x+1,x+1,y+7,y+8,'TB',h4)
    s.write_merge(x+1,x+1,y+9,y+10,'Yếu',h4)
    s.write_merge(x+1,x+1,y+11,y+12,'Kém',h4)
    
    for i in range(5):
        s.write(x+2,y+2*i+3,'sl',h4)
        s.write(x+2,y+2*i+4,'%' ,h4)
    
    
    i=0
    for b,sum,total,list1 in list:
        stt=0
        for name,ss,teacherName,l in list1:
            i+=1
            stt+=1                
            s.write(x+i+2,y-1,stt,h82)
            s.write(x+i+2,y,name,h82)
            s.write(x+i+2,y+1,ss,h72)
            s.write(x+i+2,y+2,teacherName,h82)
            j=0
            for u,v in l :
                v=round(v+e, 2)
                s.write(x+i+2,y+2*j+3,u,h72)
                s.write(x+i+2,y+2*j+4,v,h73)
                j+=1
                
        i+=1
        str11=b
        s.write(x+i+2,y-1,'',h41)
        s.write(x+i+2,y,str11,h41)
        s.write(x+i+2,y+1,sum,h72)        
        s.write(x+i+2,y+2,'',h41)
        j=0
        for u,v in total:
            v=round(v+e, 2)                            
            s.write(x+i+2,y+2*j+3,u,h72)
            s.write(x+i+2,y+2*j+4,v,h73)
            j+=1
        i+=1
        s.write(x+i+2,y-1,'',h41)
        s.write(x+i+2,y,'',h5)
        s.write(x+i+2,y+1,'',h72)        
        s.write(x+i+2,y+2,'',h72)        
        j=0
        for u,v in total:
            s.write(x+i+2,y+2*j+3,'',h72)
            s.write(x+i+2,y+2*j+4,'',h72)
            j+=1
    i+=1    
    s.write(x+i+2,y,u'Toàn trường',h41)
    s.write(x+i+2,y+1,sumsumsum,h72)
    s.write(x+i+2,y+2,'',h72)
    j=0
    for u,v in allList:
        v=round(v+e, 2)        
        s.write(x+i+2,y+2*j+3,u,h72)
        s.write(x+i+2,y+2*j+4,v,h73)
        j+=1  
        
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename=%s.xls' % sheetName
    book.save(response)
    tt2= time.time()
    print (tt2-tt1)
    return response

def printMarkToExcel(termNumber,selectedClass,checkNxList,s,pupilList,markList,tkMonList,ddHKList,tbHKList,TBNamList,schoolName,ddHK1List=None):
    today=datetime.datetime.now()
    if selectedClass.teacher_id!=None:
        nameTeacher=selectedClass.teacher_id.last_name+' '+selectedClass.teacher_id.first_name
    else:
        nameTeacher=''    
    x=4
    y=0
    i=0
    numberLine=50
    print termNumber
    if termNumber==1:
        yearString='Học kỳ I - ' + 'Năm học '+ str(selectedClass.year_id.time)+'-'+str(selectedClass.year_id.time+1)
    else:     
        yearString='Học kỳ II - '+ 'Năm học '+ str(selectedClass.year_id.time)+'-'+str(selectedClass.year_id.time+1)
        
    for p in pupilList:
        
        s.write_merge(i*numberLine,i*numberLine,y,y+9,schoolName,h8)        
        s.write_merge(x+i*numberLine,x+i*numberLine,y,y+9,'PHIẾU BÁO ĐIỂM',h3)        
        s.write_merge(x+i*numberLine+1,x+i*numberLine+1,y,y+9,yearString,h8center)
        nameString =u'Họ và tên: '+unicode(p.last_name)+' '+unicode(p.first_name)
        
        s.write_merge(x+i*numberLine+3,x+i*numberLine+3,y,y+4,nameString,h8)
        birthStr='Ngày sinh: '+p.birthday.strftime('%d/%m/%Y')
        s.write_merge(x+i*numberLine+3,x+i*numberLine+3,y+5,y+6,birthStr,h8)
        classString=u'Lớp: '+selectedClass.name        
        s.write_merge(x+i*numberLine+3,x+i*numberLine+3,y+7,y+9,classString,h8)
        s.write(x+i*numberLine+5,y,'STT',h92)
        s.write(x+i*numberLine+5,y+1,'Môn học',h92)
        s.write_merge(x+i*numberLine+5,x+i*numberLine+5,y+2,y+4,'Điểm hệ số 1',h92)
        s.write_merge(x+i*numberLine+5,x+i*numberLine+5,y+5,y+6,'Điểm hệ số 2',h92)
        s.write(x+i*numberLine+5,y+7,'KTHK',h92)
        s.write(x+i*numberLine+5,y+8,'TB',h92)
        if termNumber==2:
            s.write(x+i*numberLine+5,y+9,'TBCN',h92)            
        i+=1
    j=0
    for l in markList:
        i=0
        j+=1    
        for m in l:     
            s.write(x+i*numberLine+5+j,y,j,h82)        
            s.write(x+i*numberLine+5+j,y+1,m.subject_id.name,h82)
            hs1str=''
            if m.mieng_1: hs1str+=normalize(m.mieng_1,checkNxList[j-1])+' '         
            if m.mieng_2: hs1str+=normalize(m.mieng_2,checkNxList[j-1])+' '         
            if m.mieng_3: hs1str+=normalize(m.mieng_3,checkNxList[j-1])+' '         
            if m.mieng_4: hs1str+=normalize(m.mieng_4,checkNxList[j-1])+' '         
            if m.mieng_5: hs1str+=normalize(m.mieng_5,checkNxList[j-1])+' '
                     
            if m.mlam_1: hs1str+=normalize(m.mlam_1,checkNxList[j-1])+' '
            if m.mlam_2: hs1str+=normalize(m.mlam_2,checkNxList[j-1])+' '
            if m.mlam_3: hs1str+=normalize(m.mlam_3,checkNxList[j-1])+' '
            if m.mlam_4: hs1str+=normalize(m.mlam_4,checkNxList[j-1])+' '
            if m.mlam_5: hs1str+=normalize(m.mlam_5,checkNxList[j-1])+' '
            s.write_merge(x+i*numberLine+5+j,x+i*numberLine+5+j,y+2,y+4,hs1str,h82)
            
            hs2str=''
            if m.mot_tiet_1: hs2str+=normalize(m.mot_tiet_1,checkNxList[j-1])+' '         
            if m.mot_tiet_2: hs2str+=normalize(m.mot_tiet_2,checkNxList[j-1])+' '         
            if m.mot_tiet_3: hs2str+=normalize(m.mot_tiet_3,checkNxList[j-1])+' '         
            if m.mot_tiet_4: hs2str+=normalize(m.mot_tiet_4,checkNxList[j-1])+' '         
            if m.mot_tiet_5: hs2str+=normalize(m.mot_tiet_5,checkNxList[j-1])+' '         
            s.write_merge(x+i*numberLine+5+j,x+i*numberLine+5+j,y+5,y+6,hs2str,h82)
            ckstr=''
            if m.ck: ckstr+=normalize(m.ck,checkNxList[j-1])+' '         
            s.write(x+i*numberLine+5+j,y+7,ckstr,h82)
            tbstr=''
            if m.tb:
                if checkNxList[j-1]==0:
                    tbstr+=str(m.tb)
                else:
                    tbstr=normalize(m.tb,1)
                             
            s.write(x+i*numberLine+5+j,y+8,tbstr,h82)
            i+=1
    if termNumber==2:        
        j=0  
        for aTKMonList in tkMonList:
            i=0
            j+=1      
            for tkMon in aTKMonList:
                tkMonStr=''
                if tkMon.tb_nam!=None:
                    if checkNxList[j-1]==0: 
                        tkMonStr=str(tkMon.tb_nam)
                    else:
                        tkMonStr=normalize(tkMon.tb_nam,1)    
                s.write(x+i*numberLine+5+j,y+9,tkMonStr,h82)
                i+=1
                    
            
    i=0  
    for dd,tbhk,tbNam in zip(ddHKList,tbHKList,TBNamList):
        if termNumber==1:
            s.write_merge(x+i*numberLine+7+j,x+i*numberLine+8+j,y,y+1,'Tổng kết HK I',h82)
        else:    
            s.write_merge(x+i*numberLine+7+j,x+i*numberLine+8+j,y,y+1,'Tổng kết HK II',h82)
        s.write(x+i*numberLine+7+j,y+2,'TB',h82)
        s.write(x+i*numberLine+7+j,y+3,'Học lực',h82)
        s.write(x+i*numberLine+7+j,y+4,'Hạnh kiểm',h82)
        s.write(x+i*numberLine+7+j,y+5,'Danh hiệu',h82)
        s.write(x+i*numberLine+7+j,y+6,'Nghỉ có phép',h82)
        s.write_merge(x+i*numberLine+7+j,x+i*numberLine+7+j,y+7,y+8,'Nghỉ không phép',h82)
        
        s.write(x+i*numberLine+8+j,y+2,tbhk.tb_hk,h82)
        s.write(x+i*numberLine+8+j,y+3,convertHlToVietnamese(tbhk.hl_hk),h82)
        
        if termNumber==1:
            s.write(x+i*numberLine+8+j,y+4,convertHkToVietnamese(tbNam.term1),h82)
        else:    
            s.write(x+i*numberLine+8+j,y+4,convertHkToVietnamese(tbNam.term2),h82)
            
        s.write(x+i*numberLine+8+j,y+5,convertDanhHieu(tbhk.danh_hieu_hk),h82)        
        s.write(x+i*numberLine+8+j,y+6,dd.co_phep,h82)
        s.write_merge(x+i*numberLine+8+j,x+i*numberLine+8+j,y+7,y+8,dd.khong_phep,h82)
        
        s.write_merge(x+i*numberLine+12+j,x+i*numberLine+12+j,y,y+3,'Ý kiến của phụ huynh',h8)    
        s.write_merge(x+i*numberLine+12+j,x+i*numberLine+12+j,y+5,y+8,'Ý kiến của GVCN',h8)
        for t in range(1,6):
            s.write_merge(x+i*numberLine+12+j+t,x+i*numberLine+12+j+t,y,y+3,'......................................................................',h8)    
            s.write_merge(x+i*numberLine+12+j+t,x+i*numberLine+12+j+t,y+5,y+8,'.....................................................................',h8)
        dateStr='Ngày ' + str(today.day)+' tháng '+str(today.month)+' năm '+str(today.year)

        s.write_merge(x+i*numberLine+16+j+t,x+i*numberLine+16+j+t,y+6,y+8,dateStr,h8)
        s.write_merge(x+i*numberLine+17+j+t,x+i*numberLine+17+j+t,y+6,y+8,'Giáo viên chủ nhiệm',h8)
        s.write_merge(x+i*numberLine+21+j+t,x+i*numberLine+21+j+t,y+6,y+8,nameTeacher,h8)
        i+=1
        
            
        
    if termNumber==2:
        print len(ddHK1List)
        print len(ddHKList)
        print len(TBNamList)
        i=0
        for dd1,dd2,tbNam in zip(ddHK1List,ddHKList,TBNamList):
            s.write_merge(x+i*numberLine+9+j,x+i*numberLine+9+j,y,y+1,'Cả năm',h82)
            s.write(x+i*numberLine+9+j,y+2,tbNam.tb_nam,h82)
            s.write(x+i*numberLine+9+j,y+3,convertHlToVietnamese(tbNam.hl_nam),h82)
            s.write(x+i*numberLine+9+j,y+4,convertHkToVietnamese(tbNam.year),h82)
            s.write(x+i*numberLine+9+j,y+5,convertDanhHieu(tbNam.danh_hieu_nam),h82)
            if (dd1.co_phep!=None) & (dd2.co_phep!=None):
                coPhep=dd1.co_phep+dd2.co_phep
            else:
                coPhep=''
                    
            if (dd1.khong_phep!=None) & (dd2.khong_phep!=None):
                khongPhep=dd1.khong_phep+dd2.khong_phep
            else:
                khongPhep=''    
                
            s.write(x+i*numberLine+9+j,y+6,coPhep,h82)
            s.write_merge(x+i*numberLine+9+j,x+i*numberLine+9+j,y+7,y+8,khongPhep,h82)

            if   tbNam.len_lop:
                lenLopStr='Thuộc diện: Được lên lớp.'
            elif tbNam.len_lop==False:
                lenLopStr='Thuộc diện: Không được lên lớp.'
            elif tbNam.thi_lai:
                lenLopStr='Thuộc diện: kiểm tra lại trong hè.'
            elif tbNam.ren_luyen_lai:                         
                lenLopStr='Thuộc diện: rèn luyện thêm trong hè.'
            else:
                lenLopStr='Thuộc diện: Chưa được xếp loại.'        
            s.write_merge(x+i*numberLine+11+j,x+i*numberLine+11+j,y,y+3,lenLopStr,h8)
            i+=1 
    
            
               
        
def setSizeOfMarkClass(s,numberPage):
    s.set_paper_size_code(9)
    setHorz =[]    
    for i in range(numberPage):
        setHorz.append(((i+1)*50,0,255))
   # s.vert_page_breaks =[]    
    s.horz_page_breaks = setHorz
    s1=1000
    s2=3000
    s.col(0).width=s1
    s.col(1).width=s2
    size = int((A4_WIDTH-s1-s2)/8)
    for i in range(2,6):
        s.col(i).width=size
    s.col(4).width=size+200
    s.col(6).width=size+1000
    s.col(7).width=size-500
    s.col(8).width=size-500
    s.col(9).width=size-500
    
    
    
def markForClass(termNumber,class_id):
    print termNumber
    tt1 = time.time()
    if termNumber>2: return
    selectedClass = Class.objects.get(id=class_id)
    book = Workbook(encoding = 'utf-8')
    s    = book.add_sheet('s1',True)
      
      
    markList=[]
    tkMonList=[]
    if termNumber==1:
        subjectList = Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber,3,4]).order_by("index",'name')
    else:    
        subjectList = Subject.objects.filter(class_id=class_id).order_by("index",'name')
    pupilList = Pupil.objects.filter(classes=class_id,attend__is_member=True).order_by('index','first_name','last_name','birthday')
    checkNxList=[]
    for sub in subjectList:
        l = Mark.objects.filter(subject_id=sub.id,term_id__number=termNumber,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
        markList.append(l)
        if termNumber==2:
            tkMon=TKMon.objects.filter(subject_id=sub.id,current=True).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
            tkMonList.append(tkMon)
        if sub.nx:  checkNxList+=[1]
        else     :  checkNxList+=[0]  
    print checkNxList      
    ddHKList=TKDiemDanh.objects.filter(student_id__classes=class_id,term_id__number=termNumber).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    tbHKList=TBHocKy.objects.filter(student_id__classes=class_id,term_id__number=termNumber).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
    TBNamList      =TBNam  .objects.filter(student_id__classes=class_id).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')

    ddHK1List=None
    if termNumber==2:
        ddHK1List=TKDiemDanh.objects.filter(student_id__classes=class_id,term_id__number=1).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
        
    schoolName= selectedClass.year_id.school_id.name
    setSizeOfMarkClass(s,len(pupilList))
    printMarkToExcel(termNumber,selectedClass,checkNxList,s,pupilList,markList,tkMonList,ddHKList,tbHKList,TBNamList,schoolName,ddHK1List)

    response = HttpResponse(mimetype='application/ms-excel')
    
    name = 'phieuBaoDiem%s.xls' % unicode(selectedClass.name)
    name1=name.replace(' ','_')
    response['Content-Disposition'] = u'attachment; filename=%s' % name1
    book.save(response)
    tt2= time.time()
    print (tt2-tt1)
    print "fffffffffffffff"
    return response
         
def printMarkForClass(request,termNumber=None,class_id=-2):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    
    message=None
    currentTerm=get_current_term(request)
    try:
        if in_school(request,currentTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    if termNumber==None:
        if (currentTerm.number>2):
            termNumber=2
        else:
            termNumber=currentTerm.number    
        
    termNumber=int(termNumber)
    class_id  = int(class_id)
    classList =Class.objects.filter(year_id=currentTerm.year_id.id)
     
    if class_id!=-2 :
        return markForClass(termNumber,class_id)
        
    
    t = loader.get_template(os.path.join('school','print_mark_for_class.html'))    
    c = RequestContext(request, {"message":message,
                                 'classList':classList,
                                 'termNumber':termNumber,
                                 'classChoice':class_id,
                                }
                       )
    return HttpResponse(t.render(c))
