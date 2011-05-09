from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
import os.path 

LOCK_MARK =False
ENABLE_CHANGE_MARK=True


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

def saveMarkNoComment(request,selectedTerm,markList,idList,tbhk1ListObjects,tbnamListObjects):
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
                               
                if (selectedTerm.number==2):
                    if (tbhk1ListObjects[i].tb!=None) & (m.tb!=None):
                        tbnamListObjects[i].tb_nam=round((tbhk1ListObjects[i].tb+m.tb*2)/3+e,1)
                        tbnamListObjects[i].save()
                    else:
                        tbnamListObjects[i].tb_nam=None
                        tbnamListObjects[i].save()        
                m.save()
                i=i+1                            
                    
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
    pupilList=Pupil.objects.filter(class_id=class_id)                
    markList=[]
    idList=[]    
    tbhk1ListObjects=[]
    tbnamListObjects=[]

    if selectedTerm.number==1:            
        i=1    
        for p in pupilList:
            m = p.mark_set.get(subject_id=subjectChoice,term_id=selectedTerm.id)
            markList.append(m)
        
            k=i*100
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
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
            id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
            idList.append(id)
            i=i+1
                            
            tbnam=p.tkmon_set.get(subject_id=subjectChoice)                    
            tbnamListObjects.append(tbnam)
    return   pupilList,markList,tbhk1ListObjects,tbnamListObjects,idList
      
def markTable(request,class_id=4):
    
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
        
    selectedClass=Class.objects.get(id=class_id)    
    yearChoice=selectedClass.year_id.id
    
    selectedClass.year_id.school_id.status=2
        
    if selectedClass.year_id.school_id.status==1:
        termList=Term.objects.filter(year_id=yearChoice,number=1).order_by('number')
    else:    
        termList=Term.objects.filter(year_id=yearChoice).order_by('number')
    
    selectedTerm=termList[termList.__len__()-1]
    termChoice=selectedTerm.id
    subjectList=Subject.objects.filter(class_id=class_id)

    if request.method == 'POST':        
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
    enableChangeMark=checkChangeMark(subject_id)
    message = None            
    
    selectedSubject = Subject.objects.get(id=subject_id)
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
        
    selectedClass=Class.objects.get(id=selectedSubject.class_id.id)    
    yearChoice=selectedClass.year_id.id
    
    selectedClass.year_id.school_id.status=2
        
    if selectedClass.year_id.school_id.status==1:
        termList=Term.objects.filter(year_id=yearChoice,number=1).order_by('number')
    else:    
        termList=Term.objects.filter(year_id=yearChoice).order_by('number')
    
    selectedTerm=termList[termList.__len__()-1]
    termChoice=selectedTerm.id
    hsSubject=int(Subject.objects.get(id=subjectChoice).hs)    
    

    if request.method == 'POST':        
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
                                'selectedClass':selectedClass,

                                'termList':termList,
                                'list':list,
                                                                  
                                'termChoice':termChoice,                              
                                'subjectChoice':subjectChoice,
                                'selectedTerm':selectedTerm,
                                'selectedSubject':selectedSubject,
                                'hsSubject':hsSubject,
                                'lengthList':lengthList,
                                }
                       )
    

    return HttpResponse(t.render(c))

