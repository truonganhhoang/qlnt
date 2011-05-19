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

import os.path 
ENABLE_CHANGE_MARK=True

def finish(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    
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
def calculateOverallMarkTerm(class_id=7,termNumber=1):

    e=0.0000000001
    pupilNoSum =0
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
                                                             
def xepLoaiHlTheoLop(request,class_id):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedClass = Class.objects.get(id__exact = class_id)
    
    if in_school(request,selectedClass.year_id.school_id) == False:
        return HttpResponseRedirect('/school')
    
    message=None    
    yearChoice  =selectedClass.year_id.id
          
    currentTerm=get_current_term(request)
    termChoice= currentTerm.id
    
    if (currentTerm.number==2):    
        termList= Term.objects.filter(year_id=selectedClass.year_id,number__lt=3).order_by('number')
    else:    
        termList= Term.objects.filter(year_id=selectedClass.year_id,number=1).order_by('number')
        
    subjectList=selectedClass.subject_set.all().order_by("-hs")
    pupilList  =Pupil.objects.filter(class_id=class_id)
    
    selectedTerm=currentTerm
    selectedYear=None
    
    message = calculateOverallMarkTerm(class_id,currentTerm.number)
    
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
    # hoc ky 1
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
                                 "currentTerm":currentTerm,
                                }
                       )
    

    return HttpResponse(t.render(c))
# tinh diem tong ket cua hoc ky va tinh hoc luc cua tat ca hoc sinh trong toan truong theo hoc ky
def finishTermByLearning1(request,term_id):
    
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
    
    if in_school(request,selectedClass.year_id.school_id) == False:
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
    
    if in_school(request,selectedTerm.year_id.school_id) == False:
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
    
    if in_school(request,selectedTerm.year_id.school_id) == False:
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
