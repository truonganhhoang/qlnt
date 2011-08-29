# -*- coding: utf-8 -*-
# author: luulethe@gmail.com 

from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.utils import *
from django.core.urlresolvers import reverse
from django.utils import simplejson
from school.sms_views import sendSMS
from django.db import transaction

import os.path 
import time 
import datetime
import random
from viewFinish import *
LOCK_MARK =False
ENABLE_CHANGE_MARK=True
e=0.00000001

"""


def thu(request):

    t1=time.time()
    for i in range(20000000):
        j=1
    t2=time.time()    
    print (t2-t1)
    t = loader.get_template(os.path.join('school','thu.html'))
    
    c = RequestContext(request, {
                                }
                       )
    

    return HttpResponse(t.render(c))
"""
class MarkID:
    def __init__(self,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19):
        self.d1=d1
        self.d2=d2
        self.d3=d3
        self.d4=d4
        self.d5=d5
        self.d6=d6
        self.d7=d7
        self.d8=d8
        self.d9=d9
        self.d10=d10
        self.d11=d11
        self.d12=d12
        self.d13=d13
        self.d14=d14
        self.d15=d15
        self.d16=d16
        self.d17=d17
        self.d18=d18
        self.d19=d19
        
class Editable:
    def __init__(self,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16):
        self.a1=a1
        self.a2=a2
        self.a3=a3
        self.a4=a4
        self.a5=a5
        self.a6=a6
        self.a7=a7
        self.a8=a8
        self.a9=a9
        self.a10=a10
        self.a11=a11
        self.a12=a12
        self.a13=a13
        self.a14=a14
        self.a15=a15
        self.a16=a16
        
def checkChangeMark(class_id):
    return (not LOCK_MARK) and ENABLE_CHANGE_MARK

                    
def saveMarkHasComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects):
            i=0
            for m in markList:
                id=idList[i]

                t1=str(id.d1)    
                t3=request.POST[t1]

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_1=None
                else:
                    tt=float(t3)
                    m.mieng_1=tt
                    
                t1=str(id.d2)    
                t3=request.POST[t1]

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_1=None
                else:
                    tt=float(t3)
                    m.mot_tiet_1=tt

                t1=str(id.d3)    
                t3=request.POST[t1]

                if t3.isspace() or (len(t3)==0) :                
                    m.ck=None
                else:
                    tt=float(t3)
                    m.ck=tt

                t1=str(id.d4)    
                t3=request.POST[t1]

                if t3.isspace() or (len(t3)==0) :                
                    m.tb=None
                else:
                    tt=float(t3)
                    m.tb=tt

                if (selectedTerm.number==2):
                    
                    t1=str(id.d5)    
                    t3=request.POST[t1]

                    if t3.isspace() or (len(t3)==0) :
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()
                    else:

                        tt=float(t3)
                        tbnamListObjects[i].tb_nam=tt
                        tbnamListObjects[i].save()
                
                
                    
                m.save()
                i=i+1    
#cac chuc nang:
#hien thu bang diem cua mot lop, cho edit roi save lai

def defineEdit(mt,timeToEdit):
    timeNow =datetime.datetime.now()
    if mt==None:
        return Editable(0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0 ,0)
    else:
        if mt.mieng_1!=None:
            if (timeNow-mt.mieng_1).total_seconds()/60 > timeToEdit: a1=0
            else: a1=1
        else: a1=1
            
        if mt.mieng_2!=None:
            if (timeNow-mt.mieng_2).total_seconds()/60 > timeToEdit: a2=0
            else: a2=1
        else: a2=1

        if mt.mieng_3!=None:
            if (timeNow-mt.mieng_3).total_seconds()/60 > timeToEdit: a3=0
            else: a3=1
        else: a3=1    
            
        if mt.mieng_4!=None:
            if (timeNow-mt.mieng_4).total_seconds()/60 > timeToEdit: a4=0
            else: a4=1
        else: a4=1    

        if mt.mieng_5!=None:
            if (timeNow-mt.mieng_5).total_seconds()/60 > timeToEdit: a5=0
            else: a5=1
        else: a5=1
        ###########################################################    
            
        if mt.mlam_1!=None:
            if (timeNow-mt.mlam_1).total_seconds()/60 > timeToEdit: a6=0
            else: a6=1
        else: a6=1
            
        if mt.mlam_2!=None:
            if (timeNow-mt.mlam_2).total_seconds()/60 > timeToEdit: a7=0
            else: a7=1
        else: a7=1

        if mt.mlam_3!=None:
            if (timeNow-mt.mlam_3).total_seconds()/60 > timeToEdit: a8=0
            else: a8=1
        else: a8=1    
            
        if mt.mlam_4!=None:
            if (timeNow-mt.mlam_4).total_seconds()/60 > timeToEdit: a9=0
            else: a9=1
        else: a9=1    

        if mt.mlam_5!=None:
            if (timeNow-mt.mlam_5).total_seconds()/60 > timeToEdit: a10=0
            else: a10=1
        else: a10=1
        ###########################################################    
        if mt.mot_tiet_1!=None:
            if (timeNow-mt.mot_tiet_1).total_seconds()/60 > timeToEdit: a11=0
            else: a11=1
        else: a11=1
            
        if mt.mot_tiet_2!=None:
            if (timeNow-mt.mot_tiet_2).total_seconds()/60 > timeToEdit: a12=0
            else: a12=1
        else: a12=1

        if mt.mot_tiet_3!=None:
            if (timeNow-mt.mot_tiet_3).total_seconds()/60 > timeToEdit: a13=0
            else: a13=1
        else: a13=1    
            
        if mt.mot_tiet_4!=None:
            if (timeNow-mt.mot_tiet_4).total_seconds()/60 > timeToEdit: a14=0
            else: a14=1
        else: a14=1    

        if mt.mot_tiet_5!=None:
            if (timeNow-mt.mot_tiet_5).total_seconds()/60 > timeToEdit: a15=0
            else: a15=1
        else: a15=1
        
        if mt.ck!=None:
            if (timeNow-mt.ck).total_seconds()/60 > timeToEdit: a16=0
            else: a16=1
        else: a16=1
        
        return Editable(a1,a2,a3,a4,a5, a6,a7,a8,a9,a10, a11,a12,a13,a14,a15 ,a16)
        ###########################################################    
    
        
        
        
        
def getMark(subjectChoice,selectedTerm):
    
    selectedSubject = Subject.objects.get(id= subjectChoice)
    class_id = selectedSubject.class_id.id
    timeToEdit = 0    
    pupilList=Pupil.objects.filter(class_id=class_id).order_by('index')                
    editList=[]    
    idList=[]    
    tbhk1List=[]
    tbnamList=[]
    if selectedTerm.number==1:            
        i=1   
        markList     =Mark.objects.filter(term_id=selectedTerm.id,subject_id=subjectChoice).order_by('student_id__index')
        markTimeList =MarkTime.objects.filter(mark_id__term_id=selectedTerm.id,mark_id__subject_id=subjectChoice).order_by('mark_id__student_id__index') 

        for mt in markTimeList: 
            ea=defineEdit(mt,timeToEdit)            
            editList.append(ea)                
            k=i*100
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16,k+17,k+18,k+19)
            idList.append(id)
            i=i+1
        list=zip(pupilList,markList,editList,idList)  
                 
    else:
        i=1
        beforeTerm   =Term.objects.get(year_id=selectedTerm.year_id,number=1).id
        markList     =Mark.objects.filter(term_id=selectedTerm.id,subject_id=subjectChoice).order_by('student_id__index')
        markTimeList =MarkTime.objects.filter(mark_id__term_id=selectedTerm.id,mark_id__subject_id=subjectChoice).order_by('mark_id__student_id__index') 
        tbhk1List    =Mark.objects.filter(term_id=beforeTerm,subject_id=subjectChoice).order_by('student_id__index')
        tbnamList    =TKMon.objects.filter(subject_id=subjectChoice).order_by('student_id__index')
        
        for mt in markTimeList:                      
            ea=defineEdit(mt,timeToEdit)                
            editList.append(ea)                                                                                                               
            k=i*100
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16,k+17,k+18,k+19)
            idList.append(id)
            i=i+1
            
        list=zip(pupilList,markList,editList,tbhk1List,tbnamList,idList)
    return   list

    
def markForASubject(request,subject_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedSubject = Subject.objects.get(id=subject_id)
    try:
        if in_school(request,selectedSubject.class_id.year_id.school_id) == False:
            return HttpResponseRedirect('/school')

    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    ok=False        
    position = get_position(request)
    """
    if position ==4: ok=True
    #kiem tra xem giao vien nay co phai day lop nay khong ?
    if position ==3:
        if selectedSubject.teacher_id != None:
            if selectedSubject.teacher_id.user_id.id == request.user.id:
                ok=True
                                
    if (not ok):
        return HttpResponseRedirect('/school')

    """
    enableChangeMark=2
    enableSendSMS   =True
    if    position ==4: pass
    elif position == 3:
        # kiem tra giao vien chu nhiem
        enableChangeMark=0
        enableSendSMS   =False
        if selectedSubject.class_id.teacher_id:
            if selectedSubject.class_id.teacher_id.user_id.id == request.user.id:
                enableChangeMark=0
                enableSendSMS   =True
          
        if selectedSubject.teacher_id != None:
            if selectedSubject.teacher_id.user_id.id == request.user.id:
                enableChangeMark=1
                enableSendSMS   =True
    elif position == 1:
        enableChangeMark=0
        enableSendSMS   =False
    #enableChangeMark=checkChangeMark(subject_id)
    
    print "fffffffffffffffff",enableChangeMark
    message = None                
    subjectChoice=subject_id
    hsSubject=-1    
        
    markList=[]
    editList=[]    
    tbnamList=[]
    
    tbhk1List=[]
    tbhk1ListObjects=[]
    tbnamListObjects=[]
    list=None
    idList=[]
    move=None    
    selectedClass=Class.objects.get(id=selectedSubject.class_id.id)    
    yearChoice=selectedClass.year_id.id
    
    #selectedClass.year_id.school_id.status=2
        
    selectedTerm=get_current_term(request)    
    termChoice  =selectedTerm.id    
    termList= Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')
    
    
    hsSubject=int(Subject.objects.get(id=subjectChoice).hs)    
    

    if request.method == 'POST':        
        if request.POST.get('move'):
             move=request.POST['move']          
        termChoice =int(request.POST['term'])
        selectedTerm=Term.objects.get(id=termChoice)
        list=getMark(selectedSubject.class_id.id,subjectChoice,selectedTerm)

        if (request.POST['submitChoice']=="luulai") & (hsSubject==0):
            saveMarkHasComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects)
                

    else:
        list=getMark(selectedSubject.class_id.id,subjectChoice,selectedTerm)
        
                        
    if list!=None:        
        lengthList=list.__len__() 
         
    t = loader.get_template(os.path.join('school','mark_for_a_subject.html'))
    
    c = RequestContext(request, { 
                                'message' : message,
                                'enableChangeMark':enableChangeMark,
                                'enableSendSMS':enableSendSMS,
                                'selectedClass':selectedClass,

                                'termList':termList,
                                'list':list,
                                                                  
                                'termChoice':termChoice,                              
                                'subjectChoice':subjectChoice,
                                'selectedTerm':selectedTerm,
                                'selectedSubject':selectedSubject,
                                'hsSubject':hsSubject,
                                'lengthList':lengthList,
                                'move':move,
                                }
                       )
    

    return HttpResponse(t.render(c))

#@transaction.commit_on_success          
def markTable(request,term_id=-1,class_id=-1,subject_id=-1,move=None):
    tt1=time.time()
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))


    termChoice    = term_id
    classChoice   = class_id    
    subjectChoice = subject_id
    if termChoice==-1:
        selectedTerm=get_current_term(request)
        if selectedTerm.number ==3:
            selectedTerm=Term.objects.get(year_id=selectedTerm.year_id,number=2)
            
    else             :  selectedTerm=Term.objects.get(id=termChoice) 


    try:        
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')


    enableChangeMark=checkChangeMark(class_id)
    enableChangeMark=True
    enableSendSMS   =True    
    message = None            
    list=None
    hsSubject=-1
    subjectList=None
    
    
            
    termChoice = selectedTerm.id    
    yearChoice = selectedTerm.year_id.id
            
    termList= Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')    
    classList = Class.objects.filter(year_id=yearChoice)
    

    """    
    if selectedClass.year_id.school_id.status==1:
        termList=Term.objects.filter(year_id=yearChoice,number=1).order_by('number')
    else:    
        termList=Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')    
    """
    selectedClass=None
    if classChoice !=-1: 
        subjectList=Subject.objects.filter(class_id=classChoice,primary__in=[0,selectedTerm.number,3]).order_by("index")
        selectedClass=Class.objects.get(id=classChoice)   
   
    selectedSubject=None
    
    if subjectChoice!=-1:
        selectedSubject=Subject.objects.get(id=subjectChoice)    
        list=getMark(subjectChoice,selectedTerm)
    
    lengthList=0            
    if list!=None:        
        lengthList=list.__len__()  
          
    t = loader.get_template(os.path.join('school','mark_table.html'))
    
    c = RequestContext(request, { 
                                'message' : message,
                                'enableChangeMark':enableChangeMark,
                                'enableSendSMS':enableChangeMark,

                                'classList':classList,
                                'subjectList':subjectList,
                                'termList':termList,
                                'list':list,
                                
                                'classChoice':classChoice,
                                'subjectChoice':subjectChoice,
                                'termChoice':termChoice,            
                                                  
                                'selectedTerm':selectedTerm,
                                'selectedClass':selectedClass,
                                'selectedSubject':selectedSubject,
                                'class_id':class_id,
                                
                                'lengthList':lengthList,
                                'move':move,
                                }
                       )
    
    tt2=time.time()
    print (tt2-tt1)

    return HttpResponse(t.render(c))

def markForTeacher(request,term_id=-1,subject_id=-1,move=None):
    tt1=time.time()
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    try:
        idTeacher =request.user.teacher.id
        classChoice   =-1
        termChoice    = term_id
        subjectChoice = subject_id     
        selectedSubject=None
        if subjectChoice!=-1:
            selectedSubject=Subject.objects.get(id=subjectChoice)    
            if idTeacher != selectedSubject.teacher_id.id:
                return HttpResponseRedirect('/school')
        
    except Exception as e:
        return HttpResponseRedirect('/school')
        
    
    #enableChangeMark=checkChangeMark(class_id)
    enableChangeMark=True
    enableSendSMS   =True    
    
    message = None            
    list=None
    hsSubject=-1
    subjectList=None
    
    currentTerm =get_current_term(request) 
    
    if termChoice==-1:  
        selectedTerm=currentTerm
        if selectedTerm.number ==3:
            selectedTerm=Term.objects.get(year_id=selectedTerm.year_id,number=2)

    else             :  selectedTerm=Term.objects.get(id=termChoice)
    
    if (selectedTerm.year_id.time<currentTerm.year_id.time) | ((selectedTerm.year_id.time==currentTerm.year_id.time) & (selectedTerm.number<currentTerm.number)):
        enableChangeMark=False
                    
    termChoice = selectedTerm.id    
    yearChoice = selectedTerm.year_id.id
            
    termList= Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')    
    
    subjectList=Subject.objects.filter(teacher_id=idTeacher,class_id__year_id=yearChoice,primary__in=[0,selectedTerm.number,3])
    
    if subjectChoice!=-1:
        list=getMark(subjectChoice,selectedTerm)    
    lengthList=0            
    if list!=None:        
        lengthList=list.__len__()  
          
    t = loader.get_template(os.path.join('school','mark_table.html'))    
    c = RequestContext(request, { 
                                'message' : message,
                                'enableChangeMark':enableChangeMark,
                                'enableSendSMS':enableChangeMark,

                                'subjectList':subjectList,
                                'termList':termList,
                                'list':list,
                                
                                'subjectChoice':subjectChoice,
                                'termChoice':termChoice,
                                'classChoice':classChoice,            
                                                  
                                'selectedSubject':selectedSubject,
                                'selectedTerm':selectedTerm,
                                
                                'lengthList':lengthList,
                                'move':move,
                                }
                       )
    
    tt2=time.time()
    print (tt2-tt1)

    return HttpResponse(t.render(c))




def markForAStudent(request,class_id,student_id):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedClass = Class.objects.get(id__exact = class_id)
    try:
        if in_school(request,selectedClass.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    message = None
    student=Pupil.objects.get(id=student_id)

    ok=False    
    
    position = get_position(request)
    """
    if position ==4: ok=True
    #kiem tra xem giao vien nay co phai chu nhiem lop nay khong
    if position ==3:
        if selectedClass.teacher_id != None:
            if selectedClass.teacher_id.user_id.id == request.user.id:
                ok=True
                
    if request.user.id==student.user_id.id: ok =True                 
    if (not ok):
        return HttpResponseRedirect('/school')
    """
    
    
    studentName=student.last_name+" "+student.first_name
    
    yearChoice=selectedClass.year_id.id

    selectedTerm=get_current_term(request)    
    termChoice  =selectedTerm.id
    
    termList= Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')
    
    if request.method == 'POST':
        termChoice =int(request.POST['term'])
        selectedTerm=Term.objects.get(id=termChoice)
        
    subjectList=selectedClass.subject_set.all().order_by("index")
    
    
    markList=[]
    tbnamList=[]
    tbhk1List=[]
    list=[]
    tbhk1=None
    tbhk2=None    
    tbCaNam=None
    if selectedTerm.number==2:    
        for s in subjectList:
            m=s.mark_set.get(student_id=student_id,term_id__number=2)            
            markList.append(m)
            
            tbnam=s.tkmon_set.get(student_id=student_id).tb_nam
            tbnamList.append(tbnam)
                
            hk1=s.mark_set.get(student_id=student_id,term_id__number=1).tb
            
            tbhk1List.append(hk1)
            
        list=zip(subjectList,markList,tbhk1List,tbnamList)
        tbhk1  =student.tbhocky_set.get(term_id__year_id=yearChoice,term_id__number=1)
        tbhk2  =student.tbhocky_set.get(term_id__year_id=yearChoice,term_id__number=2)
        tbCaNam=student.tbnam_set.get(year_id=yearChoice)    
    else:
        if     selectedTerm.number==1:    
            for s in subjectList:
                m=s.mark_set.get(student_id=student_id,term_id=termChoice)
                
                markList.append(m)
                
            list=zip(subjectList,markList)        
            tbhk1=student.tbhocky_set.get(term_id=termChoice)
                                    
        
    t = loader.get_template(os.path.join('school','mark_for_a_student.html'))
    
    c = RequestContext(request, { 
                                'message' : message,
                                'class_id':class_id,
                                'student_id':student_id,
                                'list':list,
                                'termList':termList,
                                'selectedTerm':selectedTerm,
                                'termChoice':termChoice,
                                'subjectList':subjectList,
                                'markList':markList,
                                'studentName':studentName,
                                'selectedClass':selectedClass,
                                'tbhk1':tbhk1,
                                'tbhk2':tbhk2,
                                'tbCaNam':tbCaNam,
                                }
                       )
    

    return HttpResponse(t.render(c))

# diem cho 1 mon

def update(s,primary):
    strings=s.split(':')
    idMark=int(strings[0])    
    setOfNumber =strings[1].split('*')
    setOfValue  =strings[2].split('*')    
    length = len(setOfNumber)
    
    timeNow = datetime.datetime.now()
    
    m = Mark.objects.get(id=idMark)
    mt= m.marktime    
    number=0
    for i in range(length-1):
        
        number= int(setOfNumber[i])
        value = float(setOfValue[i])
                    
        if value==-1    : 
            value = None
            time  = None
        else: time=timeNow    
        """
        if number ==1   :
            if (m.mieng_1==None) or (value==None):
                mt.mieng_1=time                                
            m.mieng_1 =value
        """    
        if number ==1   :
            mt.mieng_1=time                                
            m.mieng_1 =value
                                
        elif number ==2 :  
            mt.mieng_2=time                                
            m.mieng_2 =value
            
        elif number ==3 : 
            mt.mieng_3=time 
            m.mieng_3=value
            
        elif number ==4 :  
            mt.mieng_4=time                                
            m.mieng_4=value
            
        elif number ==5 :  
            mt.mieng_5=time                                
            m.mieng_5=value
                    

        elif number ==6 :  
            mt.mlam_1=time                                
            m.mlam_1=value
            
        elif number ==7 :  
            mt.mlam_2=time                                
            m.mlam_2=value
            
        elif number ==8 :  
            mt.mlam_3=time                                
            m.mlam_3=value
            
        elif number ==9 :  
            mt.mlam_4=time                                
            m.mlam_4 =value
            
        elif number ==10:  
            mt.mlam_5=time                                
            m.mlam_5 =value
            
                    
        elif number ==11:  
            mt.mot_tiet_1=time                                
            m.mot_tiet_1 =value
            
        elif number ==12:  
            mt.mot_tiet_2=time                                
            m.mot_tiet_2 =value
            
        elif number ==13:  
            mt.mot_tiet_3=time                                
            m.mot_tiet_3 =value
            
        elif number ==14:  
            mt.mot_tiet_4=time                                
            m.mot_tiet_4 =value
            
        elif number ==15:  
            mt.mot_tiet_5=time                                
            m.mot_tiet_5 =value
            
        elif number ==16:  
            mt.ck=time                                
            m.ck  =value
            
        elif (number==17):                    
            m.tb = value
            subject_id = m.subject_id
            student_id = m.student_id
            
            tbk2=Mark.objects.get(subject_id=subject_id.id,student_id=student_id.id,term_id__number=2)
            tbcn=TKMon.objects.get(subject_id=subject_id.id,student_id=student_id.id)
            if (tbk2.tb==None) | (value==None):
                tbcn.tb_nam = None
            else:     
                tbcn.tb_nam = round((m.tb + tbk2.tb*2+e)/3 , 1)            
            tbcn.save()
            
        elif (number==18):                 
            m.tb = value
        elif (number==19): 
            subject_id = m.subject_id
            student_id = m.student_id
            tbcn=TKMon.objects.get(subject_id=subject_id.id,student_id=student_id.id)

            if (primary==0)| (primary==3)| (primary==4):
                tbcn.tb_nam   = value
            elif (primary==1) | (primary==2):
                tbcn.tb_nam   =m.tb      
            tbcn.save()
            
    m.save()  
    mt.save()  
@transaction.commit_on_success    
def saveMark(request):
    
    t1=time.time()
    message = 'hello'
    if request.method == 'POST':
        str = request.POST['str']
        strs=str.split('/')        
        position = get_position(request)
        if   position ==4 :pass
        elif position ==3 :
            idTeacher= int(strs[1])
            teacher= Teacher.objects.get(id=idTeacher)
            if request.user.id!=teacher.user_id.id: return
        else: return
        length = len(strs)
        primary= int(strs[2])
        print str
        print length
        for i in range(3,length):
                update(strs[i],primary)
                     
        message=strs[0]
        
        data = simplejson.dumps({'message': message})
        t2=time.time()
        print (t2-t1)
        return HttpResponse( data, mimetype = 'json')    
                 
def sendSMSForAPupil(s,user):
    #print s
    strings=s.split(':')
    
    idMark=int(strings[0])    
    setOfNumber =strings[1].split('*')
    setOfValue  =strings[2].split('*')    
    
    length = len(setOfNumber)
    
    m = Mark.objects.get(id=idMark)
    termNumber = m.term_id.number
    markStr1="" 
    markStr2="" 
    markStr3="" 
    markStr4=""
    markStr5=""
    markStr6=""
    markStr7=""
    for i in range(length-1):                 
        number= int(setOfNumber[i])
        value = setOfValue[i]
        m.sent_mark=m.sent_mark[:number-1]+'1'+m.sent_mark[number:]
                
        if  (termNumber==2) & (number==17) : number=18
        elif (termNumber==2) & (number==18): number=17  
        if   number <6  : markStr1+=value+" "
        elif number <11 : markStr2+=value+" " 
        elif number <16 : markStr3+=value+" " 
        elif number ==16: markStr4+=value+" " 
        elif number ==17: markStr5+=value+" " 
        elif number ==18: markStr6+=value+" " 
        elif number ==19: markStr7+=value+" "
        
    smsString=u'Diem mon '+to_en1(m.subject_id.name)+ u' cua hs '
    smsString+=to_en1(m.student_id.last_name)+" "+to_en1(m.student_id.first_name)+" nhu sau: "    
    termNumber = m.term_id.number
     
    if markStr1 !="":  smsString+="Mieng:" + markStr1     
    if markStr2 !="":  smsString+="diem 15 phut:" + markStr2     
    if markStr3 !="":  smsString+="diem 45 phut:" + markStr3     
    if markStr4 !="":  smsString+="Thi cuoi ky:" + markStr4
    
    if markStr5 !="":
        if (termNumber==2):     
            smsString+="TBHK II:" + markStr5
        else:         
            smsString+="TBHK I:" + markStr5

    if markStr6 !="":  smsString+="TBHK I:" + markStr6         
    if markStr7 !="":  smsString+="TB ca nam:" + markStr7
    
    if m.student_id.sms_phone != None:
        sendSMS(m.student_id.sms_phone,smsString,user)
    m.save()    
    print smsString    
    print len(smsString)
    print user
        
def sendSMSMark(request):
    message = 'hello'
    print "hello"
    if request.method == 'POST':
        print "hello1"    
        str = request.POST['str']
        strs=str.split('/')
        print str
        for s in strs:
            if s!="":
                sendSMSForAPupil(s,request.user)
                                                            
        message='ok'
        data = simplejson.dumps({'message': message})
        return HttpResponse( data, mimetype = 'json')    
    
def capNhapMienGiam(request,class_id, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    pos = get_position(request)
    if (pos==1) and (get_student(request).id==int(student_id)):
        pos = 4
    if (get_position(request) < 1):
        return HttpResponseRedirect('/')
    
    
    # nho order
    subjectList = Subject.objects.filter(class_id=class_id,name__in=['GDQP-AN',u'Thể dục',u'Âm nhạc',u'Mĩ thuật','GDQP']).order_by('index')
    term1Mark   = Mark.objects.filter(subject_id__class_id=class_id,student_id=student_id,term_id__number=1,subject_id__name__in=['GDQP-AN',u'Thể dục',u'Âm nhạc',u'Mĩ thuật','GDQP']).order_by('subject_id__index')
    term2Mark   = Mark.objects.filter(subject_id__class_id=class_id,student_id=student_id,term_id__number=2,subject_id__name__in=['GDQP-AN',u'Thể dục',u'Âm nhạc',u'Mĩ thuật','GDQP']).order_by('subject_id__index')
    tkMonList   = TKMon.objects.filter(subject_id__class_id=class_id,student_id=student_id,subject_id__name__in=['GDQP-AN',u'Thể dục',u'Âm nhạc',u'Mĩ thuật','GDQP']).order_by('subject_id__index')
    # cam xoa  2 dong nay. Xoa se sai ngay
    for term1,term2,tkMon,s in zip(term1Mark,term2Mark,tkMonList,subjectList):
        pass
    
    if request.method=='POST':
        str = request.POST['str']
        strs= str.split(':')
        index =int(strs[0])-1
        type  =int(strs[1])
        if type==0:
            term1Mark[index].mg=False
            term2Mark[index].mg=False
            tkMonList[index].mg=False
        elif type==3:
            term1Mark[index].mg=True
            term2Mark[index].mg=True
            tkMonList[index].mg=True
        elif type==1:
            term1Mark[index].mg=True
            term2Mark[index].mg=False
            tkMonList[index].mg=False
            if subjectList[index].primary==1:
                tkMonList[index].mg=True
            
        elif type==2:
            term1Mark[index].mg=False
            term2Mark[index].mg=True
            tkMonList[index].mg=False
            if subjectList[index].primary==2:
                tkMonList[index].mg=True
        
        term1Mark[index].save()    
        term2Mark[index].save()
        tkMonList[index].save()
                                            
    mgList=[]
    coMienGiam =False
    for term1,term2,tkMon in zip(term1Mark,term2Mark,tkMonList):
        if    (tkMon.mg) & (term1.mg) & (term2.mg) : 
            mgList.append(3)
        elif  term1.mg : mgList.append(1)
        elif  term2.mg : mgList.append(2)
        else: mgList.append(0)
        
        print term1.mg,' ',term2.mg,' ',tkMon.mg
    for m in mgList:
        if m !=0:
            coMienGiam=True
                
    
    list = zip(subjectList,mgList)     
    message = None
    t = loader.get_template(os.path.join('school', 'cap_nhap_mien_giam.html'))
    c = RequestContext(request, { 
                                 'list':list,
                                 'class_id':class_id,
                                 'student_id':student_id,
                                 'coMienGiam':coMienGiam,
                                }
                       )
    return HttpResponse(t.render(c))
def convertMarkToCharacter1():
    return 'chao'
