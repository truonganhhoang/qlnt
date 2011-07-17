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

import os.path 
LOCK_MARK =False
ENABLE_CHANGE_MARK=True
def thu(request):
               
    t = loader.get_template(os.path.join('school','thu.html'))
    
    c = RequestContext(request, {
                                }
                       )
    

    return HttpResponse(t.render(c))

            
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
        
def checkChangeMark(class_id):
    return (not LOCK_MARK) and ENABLE_CHANGE_MARK

def createTbNam(request,year_id):
    classList = Class.objects.filter(year_id=year_id)
    selectedYear=Year.objects.get(id=year_id)
    allList=[]
    for c in classList :
        studentList=c.pupil_set.all()
        allList.append(studentList)
        for stu in studentList:
            find = stu.tbnam_set.filter(year_id=year_id,student_id=stu.id)
            if not find:
                tbNam=TBNam()
                tbNam.year_id=selectedYear
                tbNam.student_id=stu                
                tbNam.save()
            #pass
               
    t = loader.get_template(os.path.join('school','ll.html'))
    
    c = RequestContext(request, {
                                 "allList":allList,
                                 "classList":classList,
                                }
                       )
    

    return HttpResponse(t.render(c))
   
def createAllInfoInTerm(request,term_id):
    
    selectedTerm=Term.objects.get(id=term_id)
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList = Class.objects.filter(year_id=selectedYear.id)
    for c in classList :
        studentList=c.pupil_set.all()
        subjectList=c.subject_set.all()
        
        for stu in studentList:
            #tao cac bang
            tkDiemDanh=stu.tkdiemdanh_set.filter(term_id=term_id)
            
            if not tkDiemDanh:
                tkDiemDanh=TKDiemDanh(term_id=selectedTerm,student_id=stu)
                tkDiemDanh.save()

            hanhKiem=stu.hanhkiem_set.filter(term_id=term_id)
            if not hanhKiem:            
                hanhKiem  =HanhKiem(term_id=selectedTerm,student_id=stu)
                hanhKiem.save()
                
            
            tbHocKy =stu.tbhocky_set.filter(term_id=term_id)
            if not tbHocKy:
                tbHocKy   =TBHocKy(term_id=selectedTerm,student_id=stu)
                tbHocKy.save()
            
            # tao mark
            
            for sub in subjectList:
                m=sub.mark_set.filter(term_id=selectedTerm,student_id=stu)
                if not m:
                    m=Mark(subject_id=sub,term_id=selectedTerm,student_id=stu)
                    m.save()
                
                tkMon=sub.tkmon_set.filter(student_id=stu.id)
                if not tkMon:
                    tkMon=TKMon(student_id=stu,subject_id=sub)
                    tkMon.save()    
                                    
    t = loader.get_template(os.path.join('school','ll.html'))
    
    c = RequestContext(request, {
                                }
                       )
    

    return HttpResponse(t.render(c))   

                    
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
def getMark(class_id,subjectChoice,selectedTerm):
    pupilList=Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name','birthday')                
    markList=[]
    idList=[]    
    tbhk1ListObjects=[]
    tbnamListObjects=[]

    if selectedTerm.number==1:            
        i=1    
        for p in pupilList:
            print p
            print subjectChoice
            print selectedTerm.id
            print p.mark_set.all()
            m = p.mark_set.get(subject_id=subjectChoice,term_id=selectedTerm.id)
            
            markList.append(m)
        
            k=i*100
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16,k+17,k+18,k+19)
            idList.append(id)
            i=i+1
            
    else:
        i=1
        beforeTerm = Term.objects.get(year_id=selectedTerm.year_id,number=1)
        for p in pupilList:
            m = p.mark_set.get(subject_id=subjectChoice,term_id=selectedTerm.id)                
            markList.append(m)              
            hk1=p.mark_set.get(subject_id=subjectChoice,term_id=beforeTerm)                

            tbhk1ListObjects.append(hk1)                                                       
            k=i*100
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16,k+17,k+18,k+19)
            idList.append(id)
            i=i+1
                            
            tbnam=p.tkmon_set.get(subject_id=subjectChoice)                    
            tbnamListObjects.append(tbnam)
    return   pupilList,markList,tbhk1ListObjects,tbnamListObjects,idList

          
def markTable(request,class_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedClass = Class.objects.get(id__exact = class_id)
    
    try:        
        if in_school(request,selectedClass.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    enableChangeMark=checkChangeMark(class_id)
    message = None            
    subjectChoice=-1
    hsSubject=-1    
    
    pupilList=None    
    markList=[]
    tbnamList=[]
    tbhk1List=[]
    tbhk1ListObjects=[]
    tbnamListObjects=[]
    list=None
    idList=[]
    move=None
        
    selectedClass=Class.objects.get(id=class_id)    
    yearChoice=selectedClass.year_id.id
    enableChangeMark=True
    enableSendSMS   =True
    
    #selectedClass.year_id.school_id.status=2
    """    
    if selectedClass.year_id.school_id.status==1:
        termList=Term.objects.filter(year_id=yearChoice,number=1).order_by('number')
    else:    
        termList=Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')
    
    selectedTerm=termList[termList.__len__()-1]
    termChoice=selectedTerm.id
    """
    selectedTerm=get_current_term(request)    
    termChoice  =selectedTerm.id
    
    termList= Term.objects.filter(year_id=yearChoice,number__lt=3).order_by('number')
    
    
    
    subjectList=Subject.objects.filter(class_id=class_id)

    if request.method == 'POST':  
        if request.POST.get('move'):
             move=request.POST['move']          
        termChoice =int(request.POST['term'])
        subjectChoice=int(request.POST['subject'])                
        selectedTerm=Term.objects.get(id=termChoice)
        hsSubject=int(Subject.objects.get(id=subjectChoice).hs)    

        pupilList,markList,tbhk1ListObjects,tbnamListObjects,idList=getMark(class_id,subjectChoice,selectedTerm)
    
        if (request.POST['submitChoice']=="luulai") & (hsSubject==0):
            saveMarkHasComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects)
                
        if (request.POST['submitChoice']=="luulai") & (hsSubject>0):
            saveMarkNoComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects)
    
        if selectedTerm.number==1:
            list=zip(pupilList,markList,idList)
        else:
            length=pupilList.__len__()            
            for i in range(length):                
                tbhk1List.append(tbhk1ListObjects[i].tb)                
                tbnamList.append(tbnamListObjects[i].tb_nam)
            list=zip(pupilList,markList,tbhk1List,tbnamList,idList)
            
    lengthList=0            
    if pupilList!=None:        
        lengthList=pupilList.__len__()  
          
    t = loader.get_template(os.path.join('school','mark_table.html'))
    
    c = RequestContext(request, { 
                                'message' : message,
                                'enableChangeMark':enableChangeMark,
                                'enableSendSMS':enableChangeMark,
                                'selectedClass':selectedClass,

                                'termList':termList,
                                'subjectList':subjectList,
                                'list':list,
                                  
                                'subjectChoice':subjectChoice,
                                'termChoice':termChoice,                              

                                'selectedTerm':selectedTerm,
                                'class_id':class_id,
                                'hsSubject':hsSubject,
                                'lengthList':lengthList,
                                'move':move,
                                }
                       )
    

    return HttpResponse(t.render(c))

# diem cho mot hoc sinh tai 1 lop nao do
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
        
    subjectList=selectedClass.subject_set.all().order_by("-hs")
    
    
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
    enableChangeMark=True
    enableSendSMS   =True
    if    position ==4: pass
    elif position == 3:
        # kiem tra giao vien chu nhiem
        enableChangeMark=False
        enableSendSMS   =False
        if selectedSubject.class_id.teacher_id:
            if selectedSubject.class_id.teacher_id.user_id.id == request.user.id:
                enableChangeMark=False
                enableSendSMS   =True
          
        if selectedSubject.teacher_id != None:
            if selectedSubject.teacher_id.user_id.id == request.user.id:
                enableChangeMark=True
                enableSendSMS   =True
    elif position == 1:
        enableChangeMark=False
        enableSendSMS   =False
    #enableChangeMark=checkChangeMark(subject_id)
    
    message = None            
    
    subjectChoice=subject_id
    hsSubject=-1    
    
    pupilList=None    
    markList=[]
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
        pupilList,markList,tbhk1ListObjects,tbnamListObjects,idList=getMark(selectedSubject.class_id.id,subjectChoice,selectedTerm)

        if (request.POST['submitChoice']=="luulai") & (hsSubject==0):
            saveMarkHasComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects)
                
        if (request.POST['submitChoice']=="luulai") & (hsSubject>0):
            saveMarkNoComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects)

    else:
        pupilList,markList,tbhk1ListObjects,tbnamListObjects,idList=getMark(selectedSubject.class_id.id,subjectChoice,selectedTerm)
        
    
    
    if selectedTerm.number==1:
        list=zip(pupilList,markList,idList)
    else:
        length=pupilList.__len__()            
        for i in range(length):                
            tbhk1List.append(tbhk1ListObjects[i].tb)                
            tbnamList.append(tbnamListObjects[i].tb_nam)
        list=zip(pupilList,markList,tbhk1List,tbnamList,idList)
            
    lengthList=0            
    if pupilList!=None:        
        lengthList=pupilList.__len__()  
          
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

def update(s):
    strings=s.split(':')
    idMark=int(strings[0])    
    setOfNumber =strings[1].split('*')
    setOfValue  =strings[2].split('*')    
    length = len(setOfNumber)
    
    m = Mark.objects.get(id=idMark)
        
    for i in range(length-1):
        
        if setOfValue[i]=="NaN":
            print "oooooooooooooooooooooooooooooooooooooooooooo" 
            continue
         
        number= int(setOfNumber[i])
        value = float(setOfValue[i].replace(',','.',1))
        
        if value==-1    : value = None
        
        print number
        print value
        
        if   number ==1 :  m.mieng_1=value
        elif number ==2 :  m.mieng_2=value
        elif number ==3 :  m.mieng_3=value
        elif number ==4 :  m.mieng_4=value
        elif number ==5 :  m.mieng_5=value
        
        elif number ==6 :  m.mlam_1=value
        elif number ==7 :  m.mlam_2=value
        elif number ==8 :  m.mlam_3=value
        elif number ==9 :  m.mlam_4=value
        elif number ==10:  m.mlam_5=value
        
        elif number ==11:  m.mot_tiet_1=value
        elif number ==12:  m.mot_tiet_2=value
        elif number ==13:  m.mot_tiet_3=value
        elif number ==14:  m.mot_tiet_4=value
        elif number ==15:  m.mot_tiet_5=value
        elif number ==16:  m.ck        =value
    print m.ck    
    if m.ck==None:
        subject_id = m.subject_id
        student_id = m.student_id
        print "ok3"
        tbcn=TKMon.objects.get(subject_id=subject_id.id,student_id=student_id.id)
        print "ok4"
        tbcn.tb_nam = None
        m.tb        = None  
        tbcn.save()
        print "ok5"
                
    else :   
            sum=m.ck*3
            factor=3
            if m.mieng_1 != None : 
                sum=sum+m.mieng_1 
                factor=factor+1 
            if m.mieng_2 != None : 
                sum=sum+m.mieng_2 
                factor=factor+1 
            if m.mieng_3 != None : 
                sum=sum+m.mieng_3 
                factor=factor+1 
            if m.mieng_4 != None : 
                sum=sum+m.mieng_4 
                factor=factor+1 
            if m.mieng_5 != None : 
                sum=sum+m.mieng_5 
                factor=factor+1 
        
            if m.mlam_1 != None : 
                sum=sum+m.mlam_1
                factor=factor+1 
            if m.mlam_2 != None : 
                sum=sum+m.mlam_2
                factor=factor+1 
            if m.mlam_3 != None: 
                sum=sum+m.mlam_3
                factor=factor+1 
            if m.mlam_4 != None: 
                sum=sum+m.mlam_4
                factor=factor+1 
            if m.mlam_5 != None: 
                sum=sum+m.mlam_5
                factor=factor+1 

            if m.mot_tiet_1 != None : 
                sum=sum+m.mot_tiet_1*2
                factor=factor+2 
            if m.mot_tiet_2 != None: 
                sum=sum+m.mot_tiet_2*2
                factor=factor+2 
            if m.mot_tiet_3 != None: 
                sum=sum+m.mot_tiet_3*2
                factor=factor+2 
            if m.mot_tiet_4 != None: 
                sum=sum+m.mot_tiet_4*2
                factor=factor+2 
            if m.mot_tiet_5 != None: 
                sum=sum+m.mot_tiet_5*2
                factor=factor+2
            print sum
            print factor    
            e=0.00000001    
            m.tb = round(sum/factor + e,1)
            
            print m.term_id.number
            if m.term_id.number==2:
                subject_id = m.subject_id
                student_id = m.student_id
                print "ok3"
                tbk1=Mark.objects.get(subject_id=subject_id.id,student_id=student_id.id,term_id__number=1)
                if tbk1.ck!=None:
                    tbcn=TKMon.objects.get(subject_id=subject_id.id,student_id=student_id.id)
                    tbcn.tb_nam = round((m.tb*2 + tbk1.tb+e)/3 , 1)
                    #print "ooooooooooooooooooooooooooooooooo"
                    #print tbcn.tb_nam
                    tbcn.save()
    print "ok2"                                     
    m.save()    
    
def saveMark(request):
    message = 'hello'

    if request.method == 'POST':
        str = request.POST['str']
        strs=str.split('/')        
        position = get_position(request)
        
        if   position ==4 :pass
        elif position ==3 :
            idTeacher= int(strs[0])
            if idTeacher==-1: return 
            else:
                teacher= Teacher.objects.get(id=idTeacher)
                if request.user.id!=teacher.user_id.id: return
        else: return
                
        #print str
        length= len(strs)
        for i in range(1,length):
                update(strs[i])     
        message='ok'
        data = simplejson.dumps({'message': message})
        return HttpResponse( data, mimetype = 'json')    
                 
def sendSMSForAPupil(s,user):
    #print s
    strings=s.split(':')
    idMark=int(strings[0])    
    setOfNumber =strings[1].split('*')
    setOfValue  =strings[2].split('*')    
    
    length = len(setOfNumber)
    
    m = Mark.objects.get(id=idMark)
    
    markStr1="" 
    markStr2="" 
    markStr3="" 
    markStr4=""
    markStr5=""
    markStr6=""
    markStr7=""
        
    for i in range(length-1):                 
        number= int(setOfNumber[i])
        value = setOfValue[i].replace(',','.',1)
        
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
    print "ok1"    
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
    

