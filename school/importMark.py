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
                value = str(s.cell(i,j).value)
                
                if len(value) !=0:
                    value1 = float(value)
                    
                    if (value1<0) | (value1>10):
                        return  u'Điểm ở ô '+cellname(i,j)+u' không nằm trong [0,10] '
                    
            except Exception as e:
                return u'Điểm ở ô '+cellname(i,j)+u' không hợp lệ'
    return ''       
        
def importMark(request,term_id,subject_id):
    t1= time.time()
    t2= time.time()
    print "fuck"
    absentMessage=''
    if request.method=='POST':
                
        filename = save_file(request.FILES.get('file'), request.session)
        filepath = os.path.join(TEMP_FILE_LOCATION, filename)       
        book = xlrd.open_workbook(filepath)                
        s = book.sheet_by_index(0)        
        validateMessage = validate(s)        
        if validateMessage=='': 
            selectedSubject = Subject.objects.get(id=subject_id)
            markList  = Mark.objects.filter(subject_id=subject_id,term_id=term_id).order_by("student_id__index")
            pupilList = Pupil.objects.filter(class_id=selectedSubject.class_id).order_by("index")
            
            x=11
            y=0
            list = zip(pupilList,markList)
            for i in range(x,s.nrows):
                
                lastName  = s.cell(i,y+1).value
                firstName = s.cell(i,y+2).value
                birthday  = s.cell(i,y+3).value
                
                print to_en1(lastName)
                print to_en1(firstName)
                print birthday
                #p=pupilList.filter()
                ok=False
                for p,m in list:
                    if (p.last_name==lastName) & (p.first_name==firstName) & (p.birthday.strftime('%d/%m/%Y')== birthday):
                        ok=True
                        value = str(s.cell(i,y+4).value)            
                        if (len(value)==0): m.mieng_1=None
                        else              : m.mieng_1=float(value)
                        
                        value = str(s.cell(i,y+5).value)            
                        if (len(value)==0): m.mieng_2=None
                        else              : m.mieng_2=float(value)
            
                        value = str(s.cell(i,y+6).value)            
                        if (len(value)==0): m.mieng_3=None
                        else              : m.mieng_3=float(value)
    
                        value = str(s.cell(i,y+7).value)            
                        if (len(value)==0): m.mieng_4=None
                        else              : m.mieng_4=float(value)
    
                        value = str(s.cell(i,y+8).value)            
                        if (len(value)==0): m.mieng_5=None
                        else              : m.mieng_5=float(value)
    
                        value = str(s.cell(i,y+9).value)            
                        if (len(value)==0): m.mlam_1=None
                        else              : m.mlam_1=float(value)
    
                        value = str(s.cell(i,y+10).value)            
                        if (len(value)==0): m.mlam_2=None
                        else              : m.mlam_2=float(value)
    
                        value = str(s.cell(i,y+11).value)            
                        if (len(value)==0): m.mlam_3=None
                        else              : m.mlam_3=float(value)
    
                        value = str(s.cell(i,y+12).value)            
                        if (len(value)==0): m.mlam_4=None
                        else              : m.mlam_4=float(value)
                        
                        value = str(s.cell(i,y+13).value)            
                        if (len(value)==0): m.mlam_5=None
                        else              : m.mlam_5=float(value)
    
                        value = str(s.cell(i,y+14).value)            
                        if (len(value)==0): m.mot_tiet_1=None
                        else              : m.mot_tiet_1=float(value)
    
                        value = str(s.cell(i,y+15).value)            
                        if (len(value)==0): m.mot_tiet_2=None
                        else              : m.mot_tiet_2=float(value)
    
                        value = str(s.cell(i,y+16).value)            
                        if (len(value)==0): m.mot_tiet_3=None
                        else              : m.mot_tiet_3=float(value)
    
                        value = str(s.cell(i,y+17).value)            
                        if (len(value)==0): m.mot_tiet_4=None
                        else              : m.mot_tiet_4=float(value)
    
                        value = str(s.cell(i,y+18).value)            
                        if (len(value)==0): m.mot_tiet_5=None
                        else              : m.mot_tiet_5=float(value)
                        
                        value = str(s.cell(i,y+19).value)            
                        if (len(value)==0): m.ck=None
                        else              : m.ck=float(value)
                        
                                                
                        m.save()
                        break
                if not ok:
                    absentMessage+='<tr>'+u'<td>' +lastName+' '+firstName+u'</td>'+u'<td>'+unicode(birthday)+u'</td>'+'</tr>'
            
                                               
    print (t2-t1)
    data=[{"absentMessage":absentMessage,
           'validateMessage':validateMessage,
           }]
    #print (t2-t1)

    return HttpResponse( simplejson.dumps( data ))

