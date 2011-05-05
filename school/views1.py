# -*- coding: utf-8 -*-
#from school.views import *

from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
import os.path 


class MarkID:
    def __init__(self,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16):
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


#cac chuc nang:
#hien thu bang diem cua mot lop, cho edit roi save lai
def mark_table(request,class_id=4):
    message = None    
    selectedClass=Class.objects.get(id=class_id)
    yearChoice=selectedClass.year_id.id
    
    school_id=selectedClass.year_id.school_id.id
    
    subjectChoice=-1
    selectedTerm=None


    #find currentTerm
    currentTerm=None
        
    termList=Term.objects.filter(year_id__school_id=school_id).order_by('-year_id__time','number')
    if termList.__len__()>0:
        currentTerm=termList[0]        
        for term in termList:
            if term.year_id.time==currentTerm.year_id.time:
                currentTerm=term
            else:
                break
            
    if (yearChoice==currentTerm.year_id.id):
        termChoice=currentTerm.id
    else:
        termChoice=-1
    hsSubject=-1
    termList= Term.objects.filter(year_id=yearChoice).order_by('number')
    subjectList=Subject.objects.filter(class_id=class_id)

    if request.method == 'POST':
        termChoice =int(request.POST['term'])
        subjectChoice=int(request.POST['subject'])                
        selectedTerm=Term.objects.get(id=termChoice)
        if subjectChoice !=-1:    
            hsSubject=int(Subject.objects.get(id=subjectChoice).hs)    
    #currentYear  =yearList.latest()
   # currentTerm=selectedTerm         
    pupilList=None    
    markList=[]
    tbnamList=[]
    tbhk1List=[]
    tbhk1ListObjects=[]
    tbnamListObjects=[]
    list=None
    idList=[]    
    
    ttt=2
    beforeTerm=None
    #subjectChoice=-1
    ttt1=subjectChoice
    if ( subjectChoice!=-1) & ( termChoice!=-1) :
        ttt=322;
    
        pupilList = Pupil.objects.filter(class_id=class_id)
        
        if currentTerm.number==1:            
            i=1    
            for p in pupilList:
                m = p.mark_set.get(subject_id=subjectChoice,term_id=termChoice)
                markList.append(m)
            
                k=i*100
                id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
                idList.append(id)
                i=i+1
            
        else:
            beforeTerm=Term.objects.get(year_id=yearChoice,number=1).id            
            i=1
            for p in pupilList:
                m = p.mark_set.get(subject_id=subjectChoice,term_id=termChoice)                
                markList.append(m)
                
                hk1=p.mark_set.get(subject_id=subjectChoice,term_id=beforeTerm)
                
                tbhk1ListObjects.append(hk1)                                        
                k=i*100
                id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
                idList.append(id)
                i=i+1

                tbnam=p.tkmon_set.get(subject_id=subjectChoice)
                    
                tbnamListObjects.append(tbnam)
    ttt=1    
    ttt1=None
    ttt2=None        
    if request.method == 'POST':
        ttt=233            
        if (request.POST['submitChoice']=="luulai") & (hsSubject==0):
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

                if (currentTerm.number==2):
                    
                    t1=str(id.d5)    
                    t3=request.POST[t1]
                    ttt1=t1
                    ttt2=t3
                    ttt=45
                    if t3.isspace() or (len(t3)==0) :
                        ttt=3333                
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()
                    else:
                        ttt=555
                        tt=float(t3)
                        tbnamListObjects[i].tb_nam=tt
                        tbnamListObjects[i].save()
                
                
                    
                m.save()
                i=i+1    
                #diem mieng 2
                
                
        if (request.POST['submitChoice']=="luulai") & (hsSubject>0):
            #for m in markList:
            i=0;            
            for m in markList:
                sum=0
                factorSum=0
                id=idList[i]
                
                #diem mieng 1
                t1=str(id.d1)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_1=None
                else:
                    tt=float(t3)
                    m.mieng_1=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d2)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_2=None
                else:
                    tt=float(t3)
                    m.mieng_2=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d3)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_3=None
                else:
                    tt=float(t3)
                    m.mieng_3=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2

                t1=str(id.d4)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_4=None
                else:
                    tt=float(t3)
                    m.mieng_4=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d5)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_5=None
                else:
                    tt=float(t3)
                    m.mieng_5=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                t1=str(id.d6)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_1=None
                else:
                    tt=float(t3)
                    m.mlam_1=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d7)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_2=None
                else:
                    tt=float(t3)
                    m.mlam_2=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d8)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_3=None
                else:
                    tt=float(t3)
                    m.mlam_3=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2
                
                t1=str(id.d9)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_4=None
                else:
                    tt=float(t3)
                    m.mlam_4=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d10)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_5=None
                else:
                    tt=float(t3)
                    m.mlam_5=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2
                t1=str(id.d11)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_1=None
                else:
                    tt=float(t3)
                    m.mot_tiet_1=tt
                    sum=sum+tt*2
                    factorSum+=2
                    
                #diem mieng 2
                
                t1=str(id.d12)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_2=None
                else:
                    tt=float(t3)
                    m.mot_tiet_2=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d13)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_3=None
                else:
                    tt=float(t3)
                    m.mot_tiet_3=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d14)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_4=None
                else:
                    tt=float(t3)
                    m.mot_tiet_4=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d15)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_5=None
                else:
                    tt=float(t3)
                    m.mot_tiet_5=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d16)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.ck=None
                else:
                    tt=float(t3)
                    m.ck=tt
                    sum=sum+tt*3
                    factorSum+=3
                
                e=0.00000000001    
                if m.ck!=None:
                    if factorSum==0:
                        m.tb=0
                    else:                        
                        m.tb=round(sum/factorSum+e,1)
                else:
                    m.tb=None            
                if (currentTerm.number==2):
                    if (tbhk1ListObjects[i].tb!=None) & (m.tb!=None):
                        tbnamListObjects[i].tb_nam=round((tbhk1ListObjects[i].tb+m.tb*2)/3+e,1)
                        tbnamListObjects[i].save()
                    else:
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()        
                m.save()
                i=i+1                            
    

        if currentTerm.number==1:            
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

                                'termList':termList,
                                'subjectList':subjectList,
                                'markList':markList,
                                'list':list,
                                
                                'termChoice':termChoice,                                
                                'subjectChoice':subjectChoice,

                                'currentTerm':currentTerm,
                                'selectedTerm':selectedTerm,
                                'class_id':class_id,
                                'hsSubject':hsSubject,
                                'lengthList':lengthList,
                                'ttt':ttt,
                                'ttt1':ttt1,
                                'ttt2':ttt2
                                }
                       )
    

    return HttpResponse(t.render(c))

# diem cho mot hoc sinh tai 1 lop nao do
def markForAStudent(request,class_id=7,student_id=1):
    message = None
    student=Pupil.objects.get(id=student_id)
    studentName=student.last_name+" "+student.first_name
    
    selectedClass=Class.objects.get(id=class_id)    
    yearChoice=selectedClass.year_id.id
    termList= Term.objects.filter(year_id=yearChoice).order_by('-number')
    termChoice=termList[0].id
    selectedTerm=termList[0]
    termList= Term.objects.filter(year_id=yearChoice).order_by('number')
    
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
def markForASubject(request,subject_id=2):

    message = None       
    
    subjectChoice=subject_id
    selectedSubject=Subject.objects.get(id=subject_id)
        
    class_id=selectedSubject.class_id.id    
        
     
    selectedClass=Class.objects.get(id=class_id)
    yearChoice=selectedClass.year_id.id
    
    school_id=selectedClass.year_id.school_id.id
    
    selectedTerm=None


    #find currentTerm
    currentTerm=None
        
    termList=Term.objects.filter(year_id__school_id=school_id).order_by('-year_id__time','number')
    if termList.__len__()>0:
        currentTerm=termList[0]        
        for term in termList:
            if term.year_id.time==currentTerm.year_id.time:
                currentTerm=term
            else:
                break
            
    if (yearChoice==currentTerm.year_id.id):
        termChoice=currentTerm.id
        selectedTerm=currentTerm
    else:
        termChoice=-1
        
    hsSubject=int(Subject.objects.get(id=subjectChoice).hs)  
      
    termList= Term.objects.filter(year_id=yearChoice).order_by('number')


    if request.method == 'POST':
        termChoice =int(request.POST['term'])
#        subjectChoice=int(request.POST['subject'])                
        selectedTerm=Term.objects.get(id=termChoice)
    #currentYear  =yearList.latest()
#    currentTerm=selectedTerm         

    pupilList=None    
    markList=[]
    tbnamList=[]
    tbhk1List=[]
    tbhk1ListObjects=[]
    tbnamListObjects=[]
    list=None
    idList=[]    
    
    ttt=2
    beforeTerm=None

    ttt1=subjectChoice
    if ( subjectChoice!=-1) & ( termChoice!=-1) :
        ttt=322;
    
        pupilList = Pupil.objects.filter(class_id=class_id)
        
        if currentTerm.number==1:            
            i=1    
            for p in pupilList:
                m = p.mark_set.get(subject_id=subjectChoice,term_id=termChoice)
                markList.append(m)
            
                k=i*100
                id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
                idList.append(id)
                i=i+1
            
        else:
            beforeTerm=Term.objects.get(year_id=yearChoice,number=1).id            
            i=1
            for p in pupilList:
                m = p.mark_set.get(subject_id=subjectChoice,term_id=termChoice)                
                markList.append(m)
                
                hk1=p.mark_set.get(subject_id=subjectChoice,term_id=beforeTerm)
                
                tbhk1ListObjects.append(hk1)                                        
                k=i*100
                id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
                idList.append(id)
                i=i+1

                tbnam=p.tkmon_set.get(subject_id=subjectChoice)
                    
                tbnamListObjects.append(tbnam)
    ttt=1    
    ttt1=None
    ttt2=None        
    if request.method == 'POST':
        ttt=233            
        if (request.POST['submitChoice']=="luulai") & (hsSubject==0):
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

                if (currentTerm.number==2):
                    
                    t1=str(id.d5)    
                    t3=request.POST[t1]
                    ttt1=t1
                    ttt2=t3
                    ttt=45
                    if t3.isspace() or (len(t3)==0) :
                        ttt=3333                
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()
                    else:
                        ttt=555
                        tt=float(t3)
                        tbnamListObjects[i].tb_nam=tt
                        tbnamListObjects[i].save()
                
                
                    
                m.save()
                i=i+1    
                #diem mieng 2
                
                
        if (request.POST['submitChoice']=="luulai") & (hsSubject>0):
            #for m in markList:
            i=0;            
            for m in markList:
                sum=0
                factorSum=0
                id=idList[i]
                
                #diem mieng 1
                t1=str(id.d1)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_1=None
                else:
                    tt=float(t3)
                    m.mieng_1=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d2)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_2=None
                else:
                    tt=float(t3)
                    m.mieng_2=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d3)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_3=None
                else:
                    tt=float(t3)
                    m.mieng_3=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2

                t1=str(id.d4)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_4=None
                else:
                    tt=float(t3)
                    m.mieng_4=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d5)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mieng_5=None
                else:
                    tt=float(t3)
                    m.mieng_5=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                t1=str(id.d6)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_1=None
                else:
                    tt=float(t3)
                    m.mlam_1=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d7)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_2=None
                else:
                    tt=float(t3)
                    m.mlam_2=tt
                    sum=sum+tt
                    factorSum+=1
                    
                #diem mieng 2
                
                t1=str(id.d8)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_3=None
                else:
                    tt=float(t3)
                    m.mlam_3=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2
                
                t1=str(id.d9)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_4=None
                else:
                    tt=float(t3)
                    m.mlam_4=tt
                    sum=sum+tt
                    factorSum+=1

                #diem mieng 2
                
                t1=str(id.d10)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mlam_5=None
                else:
                    tt=float(t3)
                    m.mlam_5=tt
                    sum=sum+tt
                    factorSum+=1
                #diem mieng 2
                t1=str(id.d11)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_1=None
                else:
                    tt=float(t3)
                    m.mot_tiet_1=tt
                    sum=sum+tt*2
                    factorSum+=2
                    
                #diem mieng 2
                
                t1=str(id.d12)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_2=None
                else:
                    tt=float(t3)
                    m.mot_tiet_2=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d13)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_3=None
                else:
                    tt=float(t3)
                    m.mot_tiet_3=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d14)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_4=None
                else:
                    tt=float(t3)
                    m.mot_tiet_4=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d15)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.mot_tiet_5=None
                else:
                    tt=float(t3)
                    m.mot_tiet_5=tt
                    sum=sum+tt*2
                    factorSum+=2
                #diem mieng 2
                
                t1=str(id.d16)    
                t2=request.POST[t1]
                t3=t2.replace(',','.',1)

                if t3.isspace() or (len(t3)==0) :                
                    m.ck=None
                else:
                    tt=float(t3)
                    m.ck=tt
                    sum=sum+tt*3
                    factorSum+=3
                
                e=0.00000000001    
                if m.ck!=None:
                    if factorSum==0:
                        m.tb=0
                    else:                        
                        m.tb=round(sum/factorSum+e,1)
                else:
                    m.tb=None            
                if (currentTerm.number==2):
                    if (tbhk1ListObjects[i].tb!=None) & (m.tb!=None):
                        tbnamListObjects[i].tb_nam=round((tbhk1ListObjects[i].tb+m.tb*2)/3+e,1)
                        tbnamListObjects[i].save()
                    else:
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()        
                m.save()
                i=i+1                            
    

    if currentTerm.number==1:            
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

                                'termList':termList,

                                'markList':markList,
                                'list':list,
                                
                                'termChoice':termChoice,                                
                                'subjectChoice':subjectChoice,

                                'currentTerm':currentTerm,
                                'selectedTerm':selectedTerm,
                                'class_id':class_id,
                                'hsSubject':hsSubject,
                                'lengthList':lengthList,
                                'selectedSubject':selectedSubject,
                                'ttt':ttt,
                                'ttt1':ttt1,
                                'ttt2':ttt2
                                }
                       )
    

    return HttpResponse(t.render(c))


#convert diem sang hoc luc
        
# tinh diem tong ket cho 1 lop theo hoc ky
def defineHl(tb,monChuyen,monToan,monVan,minMark):
    e=0.0000001
    if monChuyen:
        firstMark=monChuyen.tb+e
    elif monToan.tb>monVan.tb:
        firstMark=monVan.tb+e
    else:
        firstMark=monToan.tb+e                
    
    if (tb>=8.0) & (firstMark>=8.0) & (minMark>=6.5):
        return 'G'
    elif (tb>=8.0) & (minMark>=5):
        return 'K'
    elif (tb>=8.0):
        return 'TB'
    elif (tb>=6.5) & (firstMark>=6.5) & (minMark>=5):
        return 'K'
    elif (tb>=6.5) & (minMark>=3.5):
        return 'TB'
    elif (tb>=6.5): 
        return 'Y'
    elif (tb>=5) & (firstMark>=5) & (minMark>=3.5):
        return 'TB'
    elif (tb>=3.5) & (minMark>=2):
        return 'Y'
    else:
        return 'Kem'

def defineHlNam(tb,monChuyen,monToan,monVan,minMark):
    e=0.0000001
    if monChuyen:
        firstMark=monChuyen.tb_nam+e
    elif monToan.tb>monVan.tb_nam:
        firstMark=monVan.tb_nam+e
    else:
        firstMark=monToan.tb_nam+e                
    
    if (tb>=8.0) & (firstMark>=8.0) & (minMark>=6.5):
        return 'G'
    elif (tb>=8.0) & (minMark>=5):
        return 'K'
    elif (tb>=8.0):
        return 'TB'
    elif (tb>=6.5) & (firstMark>=6.5) & (minMark>=5):
        return 'K'
    elif (tb>=6.5) & (minMark>=3.5):
        return 'TB'
    elif (tb>=6.5): 
        return 'Y'
    elif (tb>=5) & (firstMark>=5) & (minMark>=3.5):
        return 'TB'
    elif (tb>=3.5) & (minMark>=2):
        return 'Y'
    else:
        return 'Kem'
#tinh diem tong ket cua mot lop theo hoc ky
def calculateOverallMarkTerm(class_id=7,termNumber=1):
    print "chao"
    e=0.0000000001
    pupilNoSum=0
    
    subjectList=Subject.objects.filter(class_id=class_id)
    pupilList=Pupil.objects.filter(class_id=class_id)
    for p in pupilList:
        tbHocKy=p.tbhocky_set.get(term_id__number=termNumber)
            
        markSum=0
        factorSum=0
        ok=True
        monChuyen=None
        monToan  =None
        monVan   =None
        minMark  =10
        for s in subjectList:
            
            m=s.mark_set.get(student_id=p.id,term_id__number=termNumber)
            if s.hs==3:
                monChuyen=m
            if    s.name.lower().__contains__(u'toán'):
                monToan=m
            elif  s.name.lower().__contains__(u'văn'):
                monVan=m    
                    
                
            if m.tb !=None:
                markSum += m.tb*s.hs;
                factorSum += s.hs
                if m.tb<minMark:
                    minMark=m.tb
            else:
                ok=False
                break
        if ok:
            if factorSum==0:     
                tbHocKy.tb_hk=None
                tbHocKy.hl_hk=None
            else:
                tbHocKy.tb_hk=round(markSum/factorSum+e,1)
                                
                tbHocKy.hl_hk=defineHl(markSum/factorSum+e,monChuyen,monToan,monVan,minMark+e)
            tbHocKy.save()
        else:
            tbHocKy.tb_hk=None
            tbHocKy.hl_hk=None
            tbHocKy.save()
            pupilNoSum+=1
                
     #hien message thong bao
    selectedClass=Class.objects.get(id=class_id)
    
    return pupilNoSum    
# tinh diem tong ket cho ca nam hoc
def calculateOverallMarkYear(class_id=7):
    e=0.0000000001
    pupilNoSum=0
    selectedClass=Class.objects.get(id=class_id)
    subjectList=Subject.objects.filter(class_id=class_id)
    pupilList=Pupil.objects.filter(class_id=class_id)
    
    for p in pupilList:
        tbNam=p.tbnam_set.get(year_id=selectedClass.year_id)
            
        markSum=0
        factorSum=0
        ok=True
        monChuyen=None
        monToan  =None
        monVan   =None
        minMark  =10
        for s in subjectList:
            
            m=s.tkmon_set.get(student_id=p.id)
            if s.hs==3:
                monChuyen=m
            if    s.name.lower().__contains__(u'toán'):
                monToan=m
            elif  s.name.lower().__contains__(u'văn'):
                monVan=m    
                    
                
            if m.tb_nam !=None:
                markSum += m.tb_nam*s.hs;
                factorSum += s.hs
                if m.tb_nam<minMark:
                    minMark=m.tb_nam
            else:
                ok=False
                break
        if ok:
            if factorSum==0:     
                tbNam.tb_nam=None
                tbNam.hl_nam=None
            else:
                tbNam.tb_nam=round(markSum/factorSum+e,1)
                tbNam.hl_nam=defineHlNam(markSum/factorSum+e,monChuyen,monToan,monVan,minMark+e)
            tbNam.save()
        else:
            tbNam.tb_nam=None
            tbNam.hl_nam=None
            tbNam.save()
            pupilNoSum+=1
     
     #hien message thong bao
    if pupilNoSum==0:
        message=None
    else:      
        message=u'lớp '+selectedClass.__unicode__()+u' có ' +str(pupilNoSum)+ u' học sinh chưa được tổng kết cuối năm' 
    return message    
    
# xep loai hoc ky cua mot lop
def getCurrentTerm(class_id):

    selectedClass=Class.objects.get(id=class_id)    
    school_id=selectedClass.year_id.school_id.id
    currentTerm=None
    termChoice=-1
    
    termList=Term.objects.filter(year_id__school_id=school_id).order_by('-year_id__time','-number')
    if termList.__len__()>0:
        currentTerm=termList[0]        
        termChoice =currentTerm.id

    #neu la nam hien hien thi chon ky la ki hien tai        
    return termChoice,currentTerm
def convertMarkToCharacter(x):
    if x==9:
        return u'Giỏi'
    elif x==7:
        return u'Khá'
    elif x==6:
        return u'TB'
    elif x==4:
        return u'Yếu'
    elif x==1:
        return u'Kém'
    else:
        return  u''   
def convertHlToVietnamese(x):
    if x=='G':
        return u'Giỏi'
    elif x=='K':
        return u'Khá'
    elif x=='TB':
        return u'TB'
    elif x=='Y':
        return u'Yếu'
    elif x=='Kem':
        return u'Kém'
    else:
        return u'Chưa đủ điểm'                                                             
def xepLoaiHlTheoLop(request,class_id=7):
    ttt=None
    message=None
    selectedClass=Class.objects.get(id=class_id)  
    yearChoice  =selectedClass.year_id.id      
    termChoice,currentTerm=getCurrentTerm(class_id)
    
        
    termList= Term.objects.filter(year_id=selectedClass.year_id).order_by('number')    
    subjectList=selectedClass.subject_set.all().order_by("-hs")
    pupilList  =Pupil.objects.filter(class_id=class_id)
    
    selectedTerm=currentTerm
    selectedYear=None
    if request.method == 'POST':
        termChoice =int(request.POST['term'])
        if termChoice>0:
            termNumber=Term.objects.get(id=termChoice).number
            message = calculateOverallMarkTerm(class_id,termNumber)
        else: 
            message = calculateOverallMarkYear(class_id)
                  
        if termChoice>0:
            selectedTerm=Term.objects.get(id=termChoice)
        else:   
            ttt=termChoice         
            selectedTerm=None
                
    markList=[]

    list=[]
    if selectedTerm!=None:
        termNumber=term_id__number=selectedTerm.number
        for p in pupilList:
            markOfAPupil=[]    
            for s in subjectList:
                m=s.mark_set.get(student_id=p.id,term_id__number=termNumber)


                if s.hs!=0:                                        
                    if m.tb!=None:                                    
                        markOfAPupil.append(m.tb)
                    else:    
                        markOfAPupil.append('')
                else:
                    markOfAPupil.append(convertMarkToCharacter(m.tb))    
            
            tbHocKy=p.tbhocky_set.get(term_id__number=termNumber)

 
            if tbHocKy.tb_hk==None:
                markOfAPupil.append('')
            else:    
                markOfAPupil.append(tbHocKy.tb_hk)    
            markOfAPupil.append(convertHlToVietnamese(tbHocKy.hl_hk))
                            
            markList.append(markOfAPupil)    
        list=zip(pupilList,markList)    
    else:
        for p in pupilList:
            markOfAPupil=[]    
            for s in subjectList:
                m=s.tkmon_set.get(student_id=p.id)
                if s.hs!=0:    
                    if m.tb_nam!=None:                                    
                        markOfAPupil.append(m.tb_nam)
                    else:    
                        markOfAPupil.append('')
                else:
                    markOfAPupil.append(convertMarkToCharacter(m.tb_nam))    
            
            tbCaNam=p.tbnam_set.get(year_id=yearChoice)
            if tbCaNam.tb_nam==None:
                markOfAPupil.append('')
            else:        
                markOfAPupil.append(tbCaNam.tb_nam)    
            markOfAPupil.append(convertHlToVietnamese(tbCaNam.hl_nam))
                            
            markList.append(markOfAPupil)    
        list=zip(pupilList,markList)    
    


    t = loader.get_template(os.path.join('school','xep_loai_hl_theo_lop.html'))
    
    c = RequestContext(request, {"message":message, 
                                 "termList":termList,
                                 "subjectList":subjectList,
                                 "list":list,
                                 "selectedClass":selectedClass,
                                 "termChoice":termChoice,
                                 "selectedTerm":selectedTerm,
                                 "class_id":class_id,
                                 "ttt":ttt
                                }
                       )
    

    return HttpResponse(t.render(c))
# tinh diem tong ket cua hoc ky va tinh hoc luc cua tat ca hoc sinh trong toan truong theo hoc ky
def finishTermByLearning1(request,term_id=8):
    
    message=None
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        tempMessage=calculateOverallMarkTerm(c.id,selectedTerm.number)
        if tempMessage!=None:
            notFinishList.append(tempMessage)
        else:
            finishList.append(c.name)    
                         
        
    ttt=None    
    yearString=str(selectedTerm.year_id.time)+'-'+str(selectedTerm.year_id.time+1)
    t = loader.get_template(os.path.join('school','finish_term_by_learning.html'))
    c = RequestContext(request, {"message":message, 
                                 "finishList":finishList,
                                 "notFinishList":notFinishList,
                                 "selectedTerm":selectedTerm,
                                 "yearString":yearString,
                                }
                       )
    

    return HttpResponse(t.render(c))





def getCurrentTerm(class_id):

    selectedClass=Class.objects.get(id=class_id)    
    school_id=selectedClass.year_id.school_id.id
    currentTerm=None
    termChoice=-1
    
    termList=Term.objects.filter(year_id__school_id=school_id).order_by('-year_id__time','-number')
    if termList.__len__()>0:
        currentTerm=termList[0]        
        termChoice =currentTerm.id

    #neu la nam hien hien thi chon ky la ki hien tai        
    return termChoice,currentTerm
def definePass(tbNam,p):
    try:
        hk1_id=Term.objects.get(year_id=tbNam.year_id,number=1).id
        hk2_id=Term.objects.get(year_id=tbNam.year_id,number=2).id
    
        absentSum =  p.tkdiemdanh_set.get(term_id=hk1_id).tong_so+p.tkdiemdanh_set.get(term_id=hk2_id).tong_so
        tbNam.tong_so_ngay_nghi=absentSum
        #hoc sinh nay truot
        if (absentSum>45):
            tbNam.len_lop=False
            return

    except Exception as e:
        print e

        if (tbNam.hl_nam!='Y') & (tbNam.hl_nam!='Kem') & (tbNam.hk_nam!='Y'):
            tbNam.len_lop=True
            return
        
        if ((tbNam.hk_nam!='Y') & (tbNam.hl_nam=='Y')):
            tbNam.len_lop=None
            tbNam.thi_lai=True
        elif  ((tbNam.hk_nam=='Y')  & (tbNam.hl_nam!='Y') & (tbNam.hl_nam!='Kem')):
            tbNam.thi_lai=None
            tbNam.len_lop=None
            tbNam.ren_luyen_lai=True
        else:
        # hoc sinh nay truot luon va khong cho phep thi lai
            tbNam.len_lop=False
              
         
def xlCaNamTheoLop(request,class_id=7):
    message=None

    pupilNoSum=0
    
    selectedClass=Class.objects.get(id=class_id)
    pupilList=Pupil.objects.filter(class_id=class_id)
    notDefinedList=[]
    passedList=[]
    notPassedList=[]
    #danh sach thi lai
    retakenList=[]
    allList=[]
    # danh sach ren luyen lai
    repractisedList=[]
    for p in pupilList:
        aPupil=[]
        aPupil.append(p.last_name+" " +p.first_name)
        aPupil.append(p.birthday)
        
        tbNam=p.tbnam_set.get(year_id=selectedClass.year_id)
        
        # xet danh hieu thi dua
        if (tbNam.hl_nam==None) |(tbNam.hk_nam==None):
            tbNam.danh_hieu_nam=None
            tbNam.save()
            aPupil.append(tbNam)
            
            notDefinedList.append(aPupil)
            allList.append(aPupil)
            continue        
        else:
            if (tbNam.hl_nam=='G') & (tbNam.hk_nam=='T'):
                tbNam.danh_hieu_nam='G'
            elif ((tbNam.hl_nam=='G') | (tbNam.hl_nam=='K') ) & ((tbNam.hk_nam=='T') | (tbNam.hk_nam=='K')):
                tbNam.danh_hieu_nam='TT'
            else:
                tbNam.danh_hieu_nam='K'
            
            
        # xet len lop va hoc lai    
                
            definePass(tbNam,p)
            
        tbNam.save()
        aPupil.append(tbNam)  
              
        if (tbNam.len_lop==True):
            passedList.append(aPupil)
        elif (tbNam.len_lop==False):
            notPassedList.append(aPupil)
        elif (tbNam.thi_lai==True):
            retakenList.append(aPupil)
        else:
            repractisedList.append(aPupil)
        allList.append(aPupil)                
    yearString=str(selectedClass.year_id.time)+"-"+str(selectedClass.year_id.time+1)
    t = loader.get_template(os.path.join('school','xl_ca_nam_theo_lop.html'))
    
    c = RequestContext(request, {"message":message,
                                 "selectedClass":selectedClass,
                                 "yearString":yearString,
                                 "notDefinedList":notDefinedList,
                                 "passedList":passedList,
                                 "notPassedList":notPassedList,
                                 "retakenList":retakenList,
                                 "repractisedList":repractisedList,
                                 "allList":allList 
                                }
                       )
    

    return HttpResponse(t.render(c))


def finishTermByLearning(term_id=8):
    
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        numberStudents=calculateOverallMarkTerm(c.id,selectedTerm.number)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList        

def calculateNumberPractising(class_id,term_id):
    
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        hanhKiem=stu.hanhkiem_set.get(term_id=term_id)
        if hanhKiem.loai==None:
            pupilSum+=1
    return pupilSum
        
def finishTermByPractising(term_id=8):
    
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        numberStudents=calculateNumberPractising(c.id,selectedTerm.id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList        


# tinh diem tong ket va tinh hoc luc cua tat ca hoc sinh trong toan truong theo nam
def  calculateNumberAll(class_id,term_id):
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        
        hanhKiem=stu.hanhkiem_set.get(term_id=term_id)
        tbHocKy =stu.tbhocky_set.get(term_id=term_id)
        if (hanhKiem.loai==None) |(tbHocKy.hl_hk==None):
            tbHocKy.danh_hieu_hk==None
            tbHocKy.save()
            pupilSum+=1
        else:            
            if (tbHocKy.hl_nam=='G') & (hanhKiem.loai=='T'):
                tbHocKy.danh_hieu_nam='G'
            elif ((tbHocKy.hl_hk=='G') | (tbHocKy.hl_hk=='K') ) & ((hanhkiem.loai=='T') | (hanhkiem.loai=='K')):
                tbHocKy.danh_hieu_nam='TT'
            else:
                tbHocKy.danh_hieu_nam='K'
            
            tbHocKy.save()
                
    return pupilSum

def finishTermAll(term_id=1):
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        numberStudents=calculateNumberAll(c.id,selectedTerm.id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList
        
def finishYear(request,year_id=8):
    
    message=None
    finishList=[]
    notFinishList=[]
    selectedYear=Year.objects.get(id=year_id)
    classList   =Class.objects.filter(year_id=year_id)
    
    for c in classList:
        tempMessage=calculateOverallMarkYear(c.id)
        if tempMessage!=None:
            notFinishList.append(tempMessage)
        else:
            finishList.append(c.name)    
                         
        
    ttt=None    
    yearString=str(selectedYear.time)+'-'+str(selectedYear.time+1)
    t = loader.get_template(os.path.join('school','finish_year.html'))
    c = RequestContext(request, {"message":message, 
                                 "finishList":finishList,
                                 "notFinishList":notFinishList,
                                 "yearString":yearString,
                                }
                       )
    

    return HttpResponse(t.render(c))


def finishTerm(request,term_id=1):
    message=None
    selectedTerm=Term.objects.get(id=term_id)
    yearString=str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    finishLearning,notFinishLearning    =finishTermByLearning(term_id)
    finishPractising,notFinishPractising=finishTermByPractising(term_id)
    finishAll,notFinishAll              =finishTermAll(term_id)

    if request.method == 'POST':
        if request.POST['finishTerm']==u'click vào đây để kết thúc học kỳ':
            selectedTerm.active=False
        else:
            selectedTerm.active=True
                
    
    t = loader.get_template(os.path.join('school','finish_term.html'))    
    c = RequestContext(request, {"message":message,
                                 "selectedTerm":selectedTerm,
                                 "yearString":yearString,
                                 "finishLearning":finishLearning,
                                 "notFinishLearning":notFinishLearning,
                                 "finishPractising":finishPractising,
                                 "notFinishPractising":notFinishPractising,
                                 "finishAll":finishAll,
                                 "notFinishAll":notFinishAll,
                                 "value":3
                                }
                       )
    return HttpResponse(t.render(c))
