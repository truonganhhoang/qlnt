# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.utils import *
from django.core.urlresolvers import reverse
from django.db import transaction
from  views import save_file
from django.utils import simplejson

import xlrd  
from xlrd import cellname 
import os.path 
import time 
import datetime
import random
LOCK_MARK =False
ENABLE_CHANGE_MARK=True
def validate(s):
    x=11
    y=4
    for i in range(x,s.nrows):
        for j in range(4,20):
            try:
                print "ffffffffffffffffffffffff"
                value = str(s.cell(i,j).value)
                value = value.replace(' ','')
                if len(value) !=0:
                    value1 = float(value)
                    
                    if (value1<0) | (value1>10):
                        return  u'Điểm ở ô '+cellname(i,j)+u' không nằm trong [0,10] '
                    
            except Exception as e:
                return u'Điểm ở ô '+cellname(i,j)+u' không hợp lệ'

            
            
    return '' 
def process(s,x,y,mark,time,timeNow,timeToEdit,position):
    value = str(s.cell(x,y).value)
    if (time!=None) & (position!=4) :
        if (timeNow-time).total_seconds()/60 > timeToEdit:
            if (float(value)!=mark):
                print "ffff"
                return u" Ô "+cellname(x,y)+ u' không được sửa điểm.',None,None
                
    if (len(value)==0):
        return '',None,None                    
    else              : 
        return '',float(value),timeNow
@transaction.commit_on_success            
def importMark(request,term_id,subject_id):
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
    
    t1= time.time()
    timeToEdit = int(selectedSubject.class_id.year_id.school_id.get_setting('lock_time'))*60

    timeNow =datetime.datetime.now()
       
    absentMessage=''
    editMarkMessage=''
    numberOk =0
    if request.method=='POST':
                
        filename = save_file(request.FILES.get('file'), request.session)
        filepath = os.path.join(TEMP_FILE_LOCATION, filename)       
        book = xlrd.open_workbook(filepath)                
        s = book.sheet_by_index(0)        
        validateMessage = validate(s)
                
        if validateMessage=='': 
            markList  = Mark.objects.filter(subject_id=subject_id,term_id=term_id).order_by('student_id__index','student_id__first_name','student_id__last_name','student_id__birthday')
            pupilList = Pupil.objects.filter(class_id=selectedSubject.class_id).order_by('index','first_name','last_name','birthday')
            markTimeList =MarkTime.objects.filter(mark_id__term_id=term_id,mark_id__subject_id=subject_id).order_by('mark_id__student_id__index','mark_id__student_id__first_name','mark_id__student_id__last_name','mark_id__student_id__birthday') 
            x=11
            y=0
            list = zip(pupilList,markList,markTimeList)
            for p,m,mt in list:
                print mt.id
                pass
            
            for i in range(x,s.nrows):
                
                lastName  = s.cell(i,y+1).value
                firstName = s.cell(i,y+2).value
                birthday  = s.cell(i,y+3).value
                
                #p=pupilList.filter()
                ok=False
                for p,m,mt in list:
                    if (p.last_name==lastName) & (p.first_name==firstName) & (p.birthday.strftime('%d/%m/%Y')== birthday):
                        ok=True                        
                        editMarkMessage,m.mieng_1,mt.mieng_1=process(s,i,y+4,m.mieng_1,mt.mieng_1,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mieng_2,mt.mieng_2=process(s,i,y+5,m.mieng_2,mt.mieng_2,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mieng_3,mt.mieng_3=process(s,i,y+6,m.mieng_3,mt.mieng_3,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mieng_4,mt.mieng_4=process(s,i,y+7,m.mieng_4,mt.mieng_4,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mieng_5,mt.mieng_5=process(s,i,y+8,m.mieng_5,mt.mieng_5,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                           
                        editMarkMessage,m.mlam_1,mt.mlam_1=process(s,i,y+9,m.mlam_1,mt.mlam_1,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mlam_2,mt.mlam_2=process(s,i,y+10,m.mlam_2,mt.mlam_2,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mlam_3,mt.mlam_3=process(s,i,y+11,m.mlam_3,mt.mlam_3,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mlam_4,mt.mlam_4=process(s,i,y+12,m.mlam_4,mt.mlam_4,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mlam_5,mt.mlam_5=process(s,i,y+13,m.mlam_5,mt.mlam_5,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        
                        editMarkMessage,m.mot_tiet_1,mt.mot_tiet_1=process(s,i,y+14,m.mot_tiet_1,mt.mot_tiet_1,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mot_tiet_2,mt.mot_tiet_2=process(s,i,y+15,m.mot_tiet_2,mt.mot_tiet_2,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mot_tiet_3,mt.mot_tiet_3=process(s,i,y+16,m.mot_tiet_3,mt.mot_tiet_3,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mot_tiet_4,mt.mot_tiet_4=process(s,i,y+17,m.mot_tiet_4,mt.mot_tiet_4,timeNow,timeToEdit,position)        
                        if editMarkMessage !='': break
                        editMarkMessage,m.mot_tiet_5,mt.mot_tiet_5=process(s,i,y+18,m.mot_tiet_5,mt.mot_tiet_5,timeNow,timeToEdit,position)                    
                        if editMarkMessage !='': break
                        editMarkMessage,m.ck,mt.ck=process(s,i,y+19,m.ck,mt.ck,timeNow,timeToEdit,position)
                        break
                    
                if (editMarkMessage!=''): break    
                if not ok:
                    absentMessage+='<tr>'+u'<td>' +lastName+' '+firstName+u'</td>'+u'<td>'+unicode(birthday)+u'</td>'+'</tr>'
                else:
                    numberOk+=1    
            
            if (editMarkMessage==''):
                for m,mt in zip(markList,markTimeList):
                    m.save()
                    mt.save()
    message='Lỗi'                 
    if (validateMessage=='') & (editMarkMessage==''):
        if numberOk==len(markList):
            message="Đã nhập thành công cả lớp"
        else:
            message="Đã nhập được "+str(numberOk)+"/"+str(len(markList))+" học sinh."
                                                       
    t2= time.time()
    print (t2-t1)
    data=[{"absentMessage":absentMessage,
           'validateMessage':validateMessage,
           'editMarkMessage':editMarkMessage,
           'message':message,
           }]
    #print (t2-t1)

    return HttpResponse( simplejson.dumps( data ))

