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
noneSubject="............................."
e=0.00000001
s1=1000
s2=5000
s3=2000
s4=3000
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
d1=1400
d2=2000 # kick thuoc cot o trang 31  
d3=6000
d4=1200 # kich thuoc 1 o diem
SIZE_PAGE_WIDTH=36200
h1 = easyxf(
    'font:name Arial, bold on,height 1000 ;align: vert centre, horz center')
h2 = easyxf(
    'font:name Times New Roman, bold on,height 1000 ;align: vert centre, horz center')
h3 = easyxf(
    'font:name Times New Roman, bold on,height 400 ;align: vert centre, horz center')
h4 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;'
'borders : top thin ,right thin, left thin, bottom thin')
h41 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, horz left;'
'borders : top thin ,right thin, left thin, bottom thin')
h40 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;')

h5 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on, vert centre, horz center;'
'borders: top thin,right thin,left thin,bottom thin')
h6 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on;'
'borders: right thin,left thin,bottom dotted')
h61 = easyxf(
'font:name Times New Roman ,height 240 ;align:horz right;'
'borders: right thin,left thin,bottom dotted')
h7 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on;'
'borders: right thin,left thin,bottom thin')
h71 = easyxf(
'font:name Times New Roman ,height 240 ;align:horz right;'
'borders: right thin,left thin,bottom thin')

h72 = easyxf(
'font:name Times New Roman ,height 220 ;align:horz right;'
'borders: right thin,left thin,bottom thin,top thin',
)
h73 = easyxf(
'font:name Times New Roman ,height 220 ;align:horz right;'
'borders: right thin,left thin,bottom thin,top thin',
num_format_str='0.00' )

h8 = easyxf(
'font:name Times New Roman ,height 240 ; align:wrap on,horz left')
h81 = easyxf(                                    
'font:name Times New Roman ,height 240 ; align:wrap on,horz left;'# trang 31
'borders: right thin,left thin')

h82 = easyxf(                                    
'font:name Times New Roman ,height 240 ; align:wrap on,horz left;'# trang 31
'borders: right thin,left thin,bottom thin,top thin')

h9 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre')# xac nhan
h91 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre;'
'borders: right thin,left thin')

h10 = easyxf(
'font:name Times New Roman,bold on ,height 200 ;align:wrap on,horz centre,vert centre ;'
'borders: top thin,right thin,left thin,bottom thin')

hh1 = easyxf(
'font:name Times New Roman,italic on ,height 240 ;align:horz centre;'
'borders: right thin,left thin')
 
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
    
    monList    = Mark .objects.filter(student_id__class_id=class_id,subject_id__name=mon,term_id__number=termNumber).order_by("student_id__index")

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
    
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('index')
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
    
    tbhkList = TBHocKy.objects.filter(student_id__class_id=class_id,term_id__number=termNumber)
    hkList   = HanhKiem.objects.filter(student_id__class_id=class_id,year_id=selectedClass.year_id)
    
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
    
    hanhKiemList =HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    llSauHe=0
    for (i,(tbNam,hk)) in enumerate(zip(tbNamList,hanhKiemList)):
        if i % 5 != 4: h=h6
        else         : h=h7
        str1=''
        if tbNam.hl_nam!=None:           str1 = tbNam.hl_nam
                
        str2=''
        if hk.year!=None:   str2= hk.year
        
        str3=''
        if tbNam.tong_so_ngay_nghi!=None: str3 =tbNam.tong_so_ngay_nghi
         
        str4=''
        if (tbNam.len_lop==True) &(tbNam.thi_lai==None) & (hk.hk_ren_luyen_lai==None):
            str4='Lên lớp'
        
        str5=''
        if   tbNam.thi_lai       :str5='KT lại'
        elif hk.ren_luyen_lai    :str5='rèn luyện trong hè' 
        elif tbNam.len_lop==False:str5='Ở lại lớp'
        
        str6=''
        if tbNam.hl_thi_lai    :str6=tbNam.hl_thi_lai
         
        str7=''
        if hk.hk_ren_luyen_lai!=None: str7= hk.hk_ren_luyen_lai
        
        str8=''
        if (hk.ren_luyen_lai!=None) | (tbNam.thi_lai!=None):
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
    subjectList =Subject.objects.filter(class_id=class_id).order_by("index")
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
    
    markList = TKMon.objects.filter(subject_id__class_id=class_id).order_by('student_id__index','subject_id__index')
    numberPupil = Pupil.objects.filter(class_id=class_id).count()
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
               
    tbNamList = TBNam.objects.filter(student_id__class_id=class_id).order_by("student_id__index")
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

    subjectList = Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber,3,4]).order_by("index")    
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
        hk1List =  Mark.objects.filter(subject_id=subject_id,term_id__number=1).order_by('student_id__index') 
        cnList  =  TKMon.objects.filter(subject_id=subject_id).order_by('student_id__index')
    markList = Mark.objects.filter(subject_id=subject_id,term_id=term_id).order_by('student_id__index')
    
    for (i,m) in enumerate(markList):
        strs=['']*20
        if i % 5 !=4: h=h61
        else        : h=h71
        
        strs[0] =m.student_id.birthday.strftime('%d/%m/%Y')       
        if m.mieng_1!=None: strs[1]=m.mieng_1
        if m.mieng_2!=None: strs[2]=m.mieng_2
        if m.mieng_3!=None: strs[3]=m.mieng_3
        if m.mieng_4!=None: strs[4]=m.mieng_4
        if m.mieng_5!=None: strs[5]=m.mieng_5
        if m.mlam_1 !=None: strs[6]=m.mlam_1
        if m.mlam_2 !=None: strs[7]=m.mlam_2
        if m.mlam_3 !=None: strs[8]=m.mlam_3
        if m.mlam_4 !=None: strs[9]=m.mlam_4
        if m.mlam_5 !=None: strs[10]=m.mlam_5
        if m.mot_tiet_1!=None: strs[11]=m.mot_tiet_1
        if m.mot_tiet_2!=None: strs[12]=m.mot_tiet_2
        if m.mot_tiet_3!=None: strs[13]=m.mot_tiet_3
        if m.mot_tiet_4!=None: strs[14]=m.mot_tiet_4
        if m.mot_tiet_5!=None: strs[15]=m.mot_tiet_5        
        if m.ck!=None: strs[16]=m.ck
        if m.tb!=None: strs[17]=str(m.tb)
        
        if selectedTerm.number==2:
            strs[18]=strs[17]
            strs[17]=''
            if hk1List[i].tb!=None    :strs[17]=str(hk1List[i].tb)
            if cnList[i].tb_nam!=None :strs[19]=str(cnList[i].tb_nam)
        
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
