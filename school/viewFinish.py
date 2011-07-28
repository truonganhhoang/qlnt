"""
    t1= time.time()
    list = Mark.objects.all()
    for m in list:
        m.tb=9;
        m.save()
               
    t = loader.get_template(os.path.join('school','ll.html'))
    t2=time.time()
    c = RequestContext(request, {'list':list,
"""

# author: luulethe@gmail.com 

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
import time
import os.path 
ENABLE_CHANGE_MARK=True
e=0.00000001
def finish(request):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    
    if (get_position(request) != 4):
        return HttpResponseRedirect('/school')
    
    message=None
    
    currentTerm=get_current_term(request)
    
    yearString = str(currentTerm.number)+"-"+str(currentTerm.number+1)
    firstTerm  =Term.objects.get(year_id=currentTerm.year_id,number=1)
    secondTerm  =Term.objects.get(year_id=currentTerm.year_id,number=2)
    
    
    t = loader.get_template(os.path.join('school','finish.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'firstTerm':firstTerm,
                                 'secondTerm':secondTerm,
                                 'currentTerm':currentTerm,
                                }
                       )
    return HttpResponse(t.render(c))
        
# tinh diem tong ket cho 1 lop theo hoc ky
def defineHl(tb,monChuyen,monToan,monVan,minMark):
    if monChuyen:
        firstMark=monChuyen.tb+e
    elif monToan.tb<monVan.tb:
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
    if monChuyen:
        firstMark=monChuyen.tb_nam+e
    elif monToan.tb_nam>monVan.tb_nam:
        firstMark=monToan.tb_nam+e
    else:
        firstMark=monVan.tb_nam+e                
    
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
#def overallForAStudentInTerm(markList,tbHocKy,vtMonChuyen,vtMonToan,vtMonVan):
@transaction.commit_on_success
def calculateOverallMarkTerm(class_id,termNumber):

    pupilNoSum =0
    subjectList=Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber])    
    markList = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=termNumber,subject_id__primary__in=[0,termNumber]).order_by('student_id__first_name','student_id__last_name','student_id__birthday','subject_id') 
    tbHocKyList = TBHocKy.objects.filter(student_id__class_id=class_id,term_id__number=termNumber).order_by('student_id__first_name','student_id__last_name','student_id__birthday')
    
    length=len(subjectList)
    i=0   
    vtMonChuyen=-1
    for s in subjectList:
        if s.hs==3:  vtMonChuyen=i
                    
        if    s.name.lower().__contains__(u'toán'):
            vtMonToan=i
        elif  s.name.lower().__contains__(u'văn'):
            vtMonVan=i    
        i+=1    
    i=0
    j=0  
    # cam xoa dong nay
    for tt in tbHocKyList:
        pass

    for m in markList:
        #print i
        t= i % length
        if t==0:
            ok=True
            monChuyen=None
            monToan  =None
            monVan   =None
            minMark  =10
            markSum=0
            factorSum=0   
            tbHocKy=tbHocKyList[j]
            j+=1                       
             
        if t==vtMonChuyen  :  monChuyen=m
             
        if   t==vtMonToan  :
            monToan=m
        elif t==vtMonVan   :  
            monVan =m
             
        if m.tb !=None:
            markSum += m.tb*subjectList[t].hs
            factorSum +=subjectList[t].hs 
              
            if m.tb<minMark:
                minMark=m.tb
        else:
            ok=False
        if (t==length-1): 
            if  ok:
                if factorSum==0:     
                    tbHocKy.tb_hk=None
                    tbHocKy.hl_hk=None
                else:
                    tbHocKy.tb_hk=round(markSum/factorSum+e,1)                                
                    tbHocKy.hl_hk=defineHl(tbHocKy.tb_hk+e,monChuyen,monToan,monVan,minMark+e)
            else:
                tbHocKy.tb_hk=None
                tbHocKy.hl_hk=None
                pupilNoSum+=1
                
            #tbHocKy.save()                    
        i+=1
    for tb in tbHocKyList:
        tb.save()                       
       
    return pupilNoSum    
@transaction.commit_on_success
def calculateOverallMarkYear(class_id=7):

    pupilNoSum =0
    subjectList= Subject.objects.filter(class_id=class_id,primary__in=[0,1,2])    
    markList   = TKMon.objects.filter(subject_id__class_id=class_id).order_by('student_id__first_name','student_id__last_name','student_id__birthday','subject_id') 
    tbNamList  = TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__first_name','student_id__last_name','student_id__birthday')

    length = len(subjectList)
    
    i=0   
    vtMonChuyen=-1
    for s in subjectList:
        if s.hs==3:  vtMonChuyen=i
                    
        if    s.name.lower().__contains__(u'toán'):
            vtMonToan=i
        elif  s.name.lower().__contains__(u'văn'):
            vtMonVan=i    
        i+=1    
    i=0
    j=0  
    # cam xoa dong nay
    for t in tbNamList:
        pass
        
    for m in markList:
        #print i
        t= i % length
        if t==0:
            ok=True
            monChuyen=None
            monToan  =None
            monVan   =None
            minMark  =10
            markSum=0
            factorSum=0   
            tbNam=tbNamList[j]
            j+=1                       
             
        if t==vtMonChuyen  :  monChuyen=m
             
        if   t==vtMonToan  :
            monToan=m
        elif t==vtMonVan   :  
            monVan =m
             
        if m.tb_nam !=None:
            markSum += m.tb_nam*subjectList[t].hs
            factorSum +=subjectList[t].hs 
              
            if m.tb_nam<minMark:
                minMark=m.tb_nam
        else:
            ok=False
        if (t==length-1): 
            if  ok:
                if factorSum==0:     
                    tbNam.tb_nam=None
                    tbNam.hl_nam=None
                else:
                    tbNam.tb_nam=round(markSum/factorSum+e,1)                                
                    tbNam.hl_nam=defineHlNam(tbNam.tb_nam+e,monChuyen,monToan,monVan,minMark+e)                
            else:
                tbNam.tb_nam=None
                tbNam.hl_nam=None
                pupilNoSum+=1
        i+=1
    for tb in tbNamList:
        tb.save()                       
       
    return pupilNoSum    
# xep loai hoc ky cua mot lop
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

def xepLoaiHlTheoLop(request,class_id,termNumber):
    t1=time.time()
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedClass = Class.objects.get(id__exact = class_id)
    
    try:
        if in_school(request,selectedClass.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    ok=False
    position = get_position(request)
    if position ==4: ok=True
    #kiem tra xem giao vien nay co phai chu nhiem lop nay khong
    if position ==3:
        if selectedClass.teacher_id != None:
            if selectedClass.teacher_id.user_id.id == request.user.id:
                ok=True
                 
    if (not ok):
        return HttpResponseRedirect('/school')


    message=None
    
    #idYear = request.user.selectedClass.year_id
    
    #classList     =Class.objects.filter(year_id=idYear)    
    selectedYear  =selectedClass.year_id
    pupilList     =Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name','birthday')    

    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    tempList=[]
    list=[]
    # neu la hk1 hoac hk2
    termNumber=int(termNumber)
    
    if request.method=="POST":
        if termNumber <3 : calculateOverallMarkTerm(class_id,termNumber)
        else         : calculateOverallMarkYear(class_id)    
        
    if termNumber<3:        

        subjectList=Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber])    
        markList = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=termNumber,subject_id__primary__in=[0,termNumber]).order_by('student_id__first_name','student_id__last_name','student_id__birthday','subject_id') 
        tbHocKyList = TBHocKy.objects.filter(student_id__class_id=class_id,term_id__number=termNumber).order_by('student_id__first_name','student_id__last_name','student_id__birthday')

        length = len(subjectList)

        i=0    
        for m in markList:
            if i % length ==0:
                markOfAPupil=[]
            if m.tb==None:    
                  markOfAPupil.append("")
            else: markOfAPupil.append(m.tb)        
            
            if i % length==0:            
                tempList.append(markOfAPupil) 
            i+=1
 
        #markOfAPupil.append(convertHlToVietnamese(tbHocKy.hl_hk))
                                    
        list=zip(pupilList,tempList,tbHocKyList)    
    else:
        idYear = selectedYear.id
        subjectList=Subject.objects.filter(class_id=class_id,primary__in=[0,1,2])    
        markList   =TKMon.objects.filter(subject_id__class_id=class_id).order_by('student_id__first_name','student_id__last_name','student_id__birthday','subject_id') 
        tbNamList = TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__first_name','student_id__last_name','student_id__birthday')

        length = len(subjectList)

        i=0    
        for m in markList:
            if i % length ==0:
                markOfAPupil=[]
            if m.tb_nam==None:    
                  markOfAPupil.append("")
            else: markOfAPupil.append(m.tb_nam)        
            
            if i % length==0:            
                tempList.append(markOfAPupil) 
            i+=1
 
        #markOfAPupil.append(convertHlToVietnamese(tbHocKy.hl_hk))
                                    
        list=zip(pupilList,tempList,tbNamList)    
        
    

    t = loader.get_template(os.path.join('school','xep_loai_hl_theo_lop.html'))

    t2=time.time()
    print (t2-t1)
    c = RequestContext(request, {"message":message, 
                                 "subjectList":subjectList,
                                 "list":list,
                                 "selectedClass":selectedClass,
                                 "number":termNumber,
                                 "yearString":yearString,
                                 #"classList" :classList,
                                }
                       )
    

    return HttpResponse(t.render(c))

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
              
         
def xlCaNamTheoLop(request,class_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedClass = Class.objects.get(id__exact = class_id)
    try:
        if in_school(request,selectedClass.year_id.school_id) == False:
            return HttpResponseRedirect('/school')

    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    ok=False
    position = get_position(request)
    if position ==4: ok=True
    #kiem tra xem giao vien nay co phai chu nhiem lop nay khong
    if position ==3:
        if selectedClass.teacher_id != None:
            if selectedClass.teacher_id.user_id.id == request.user.id:
                ok=True
                 
    if (not ok):
        return HttpResponseRedirect('/school')

    
    message=None

    pupilNoSum=0
    
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

#------------------------------------------------------------------------------

# tong ket hoc ky, tinh lai toan bo hoc luc cua hoc sinh trong toan truong
# xem xet lop nao da tinh xong, lop nao chua xong de hieu truong co the chi dao
# co chuc nang ket thuc hoc ky
#-----------------------------------------------------------------------------



# liet ke danh sach cac lop da tinh xong hoc luc va cac  lop chua xong
def finishTermByLearning(term_id):
    
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

def calculateNumberPractisingInTerm(class_id,term_id):
    
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        hanhKiem=stu.hanhkiem_set.get(term_id=term_id)
        if hanhKiem.loai==None:
            pupilSum+=1
    return pupilSum
# liet ke cac lop da tinh xong hanh kiem va chua xong        
def finishTermByPractising(term_id):
    
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        numberStudents=calculateNumberPractisingInTerm(c.id,selectedTerm.id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList        


# tinh so luong hoc sinh chua tinh xong danh hieu
def  calculateNumberAllInTerm(class_id,term_id):
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        
        hanhKiem=stu.hanhkiem_set.get(term_id=term_id)
        tbHocKy =stu.tbhocky_set.get(term_id=term_id)
        if (hanhKiem.loai==None) |(tbHocKy.hl_hk==None):
            tbHocKy.danh_hieu_hk=None
            tbHocKy.save()
            pupilSum+=1
        else:            
            if (tbHocKy.hl_hk=='G') & (hanhKiem.loai=='T'):
                tbHocKy.danh_hieu_hk='G'
            elif ((tbHocKy.hl_hk=='G') | (tbHocKy.hl_hk=='K') ) & ((hanhKiem.loai=='T') | (hanhKiem.loai=='K')):
                tbHocKy.danh_hieu_hk='TT'
            else:
                tbHocKy.danh_hieu_hk='K'
            
            tbHocKy.save()
                
    return pupilSum

# liet ke cac lop da tinh xong danh hieu va chua xong danh hieu
def finishTermAll(term_id=None):
    finishList=[]
    notFinishList=[]
    
    selectedTerm=Term.objects.get(id=term_id)
    classList   =Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        numberStudents=calculateNumberAllInTerm(c.id,selectedTerm.id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList
        
# thong ke sinh vien ve hoc luc ,hanh kiem, va xep loai chung theo hoc ky
def finishTerm(request,term_id=None):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedTerm = Term.objects.get(id__exact = term_id)
    try:
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if (get_position(request) != 4):
        return HttpResponseRedirect('/school')
    
    
    message=None
    selectedTerm= Term.objects.get(id=term_id)
    yearString=str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    finishLearning,notFinishLearning    = finishTermByLearning(term_id)
    finishPractising,notFinishPractising= finishTermByPractising(term_id)
    finishAll,notFinishAll              = finishTermAll(term_id)
    
    hkList,pthkList = countTotalPractisingInTerm(term_id)
    hlList,pthlList = countTotalLearningInTerm(term_id)
    ddList,ptddList = countDanhHieuInTerm(term_id)

    if request.method == 'POST':
        if request.POST.get('finishTerm'):
            if request.POST['finishTerm']==u'click vào đây để kết thúc học kỳ':                
                selectedTerm.year_id.school_id.status=selectedTerm.number+1 
            else:
                selectedTerm.year_id.school_id.status=selectedTerm.number
                
            selectedTerm.year_id.school_id.save()
    currentTerm=get_current_term(request)            
    t = loader.get_template(os.path.join('school','finish_term.html'))    
    c = RequestContext(request, {"message":message,
                                 "selectedTerm":selectedTerm,
                                 "currentTerm":currentTerm,
                                 "yearString":yearString,
                                 "finishLearning":finishLearning,
                                 "notFinishLearning":notFinishLearning,
                                 "finishPractising":finishPractising,
                                 "notFinishPractising":notFinishPractising,
                                 "finishAll":finishAll,
                                 "notFinishAll":notFinishAll,
                                 
                                 "hlList":hlList,
                                 "pthlList":pthlList,
                                 "hkList":hkList,
                                 "pthkList":pthkList,
                                 "ddList":ddList,
                                 "ptddList":ptddList,
                                }
                       )
    return HttpResponse(t.render(c))
#------------------------------------------------------------------------------

# tong ket nam hoc, tinh lai toan bo hoc luc cua hoc sinh trong toan truong
# xem xet lop nao da tinh xong, lop nao chua xong de hieu truong co the chi dao
# co chuc nang ket thuc nam hoc
#-----------------------------------------------------------------------------



# thong ke hoc sinh trong mot nam hoc
def finishYearByLearning(year_id):
    
    finishList=[]
    notFinishList=[]
    
    selectedYear=Year.objects.get(id=year_id)
    classList   =Class.objects.filter(year_id=year_id)
    
    for c in classList:
        numberStudents=calculateOverallMarkYear(c.id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList        

def calculateNumberPractisingInYear(class_id,year_id):
    
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        tbNam=stu.tbnam_set.get(year_id=year_id)
        if tbNam.hk_nam==None:
            pupilSum+=1
    return pupilSum
# liet ke cac lop da tinh xong hanh kiem va chua xong        
def finishYearByPractising(year_id):
    
    finishList=[]
    notFinishList=[]
    
    selectedYear=Year.objects.get(id=year_id)
    classList   =Class.objects.filter(year_id=year_id)
    
    for c in classList:
        numberStudents=calculateNumberPractisingInYear(c.id,year_id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList        


# tinh so luong hoc sinh chua tinh xong danh hieu
def  calculateNumberAllInYear(class_id,year_id):
    studentList=Pupil.objects.filter(class_id=class_id)
    pupilSum=0
    for stu in studentList:
        
        tbNam =stu.tbnam_set.get(year_id=year_id)
        if (tbNam.hk_nam==None) |(tbNam.hl_nam==None):
            tbNam.danh_hieu_nam==None
            tbNam.save()
            pupilSum+=1
        else:            
            if (tbNam.hl_nam=='G') & (tbNam.hk_nam=='T'):
                tbNam.danh_hieu_nam='G'
            elif ((tbNam.hl_nam=='G') | (tbNam.hl_nam=='K') ) & ((tbNam.hk_nam=='T') | (tbNam.hk_nam=='K')):
                tbNam.danh_hieu_nam='TT'
            else:
                tbNam.danh_hieu_nam='K'
            
            tbNam.save()
                
    return pupilSum

# liet ke cac lop da tinh xong danh hieu va chua xong danh hieu
def finishYearAll(year_id):
    finishList=[]
    notFinishList=[]
    
    selectedYear=Year.objects.get(id=year_id)
    classList   =Class.objects.filter(year_id=year_id)
    
    for c in classList:
        numberStudents=calculateNumberAllInYear(c.id,year_id)
        if numberStudents==0:
            finishList.append(c.name)
        else:
            notFinishList.append((c.name,numberStudents))    
                         
    return finishList,notFinishList



def finishYear(request,year_id):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedTerm=Term.objects.get(year_id=year_id,number=2)
    try:
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if (get_position(request) != 4):
        return HttpResponseRedirect('/school')

    
    message=None
    
    yearString=str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    finishLearning,notFinishLearning    = finishYearByLearning(year_id)
    finishPractising,notFinishPractising= finishYearByPractising(year_id)
    finishAll,notFinishAll              = finishYearAll(year_id)
    
    hkList,pthkList = countTotalPractisingInYear(year_id)
    hlList,pthlList = countTotalLearningInYear(year_id)
    ddList,ptddList = countDanhHieuInYear(year_id)
    
    if request.method == 'POST':
        if request.POST.get('finishTerm'):
           if request.POST['finishTerm']==u'click vào đây để kết thúc học kỳ':
                selectedTerm.year_id.school_id.status=3
           else:
                selectedTerm.year_id.school_id.status=selectedTerm.number
           selectedTerm.year_id.school_id.save()     
                    
    t = loader.get_template(os.path.join('school','finish_year.html'))    
    c = RequestContext(request, {"message":message,
                                 "selectedTerm":selectedTerm,
                                 "yearString":yearString,
                                 "finishLearning":finishLearning,
                                 "notFinishLearning":notFinishLearning,
                                 "finishPractising":finishPractising,
                                 "notFinishPractising":notFinishPractising,
                                 "finishAll":finishAll,
                                 "notFinishAll":notFinishAll,
                                 
                                 "hlList":hlList,
                                 "pthlList":pthlList,
                                 "hkList":hkList,
                                 "pthkList":pthkList,
                                 "ddList":ddList,
                                 "ptddList":ptddList,
                                }
                       )
    return HttpResponse(t.render(c))
