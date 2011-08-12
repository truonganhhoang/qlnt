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
from django.utils import simplejson
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
    markList = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=termNumber,subject_id__primary__in=[0,termNumber]).order_by('student_id__index','subject_id__index') 
    tbHocKyList = TBHocKy.objects.filter(student_id__class_id=class_id,term_id__number=termNumber).order_by('student_id__index')
    hkList      = HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
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
    NN2List = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=termNumber,subject_id__primary=3).order_by('student_id__index')
    if len(NN2List)>0:
        for nn2,tbHocKy in zip(NN2List,tbHocKyList):
            if    nn2.tb+e>=8  : tbHocKy.tb_hk+=0.3
            elif  nn2.tb+e>=6.5: tbHocKy.tb_hk+=0.2
            elif  nn2.tb+e>=5  : tbHocKy.tb_hk+=0.1
    
    for hk in hkList :
        pass
    
    noHanhKiem = 0
    for hk,tbHocKy in zip(hkList,tbHocKyList):
        if termNumber==1: loaiHk=hk.term1
        else            : loaiHk=hk.term2
        
        if loaiHk==None: noHanhKiem+=1
        if (loaiHk==None) | (tbHocKy.hl_hk==None):
            tbHocKy.danh_hieu_hk=None
        elif (loaiHk=='T') & (tbHocKy.hl_hk=='G'): 
            tbHocKy.danh_hieu_hk='G'
        elif ((loaiHk=='T') | (loaiHk=='K')) & ((tbHocKy.hl_hk=='G') | (tbHocKy.hl_hk=='K')):
            tbHocKy.danh_hieu_hk='TT'
        else: tbHocKy.danh_hieu_hk='K'                                         
    
    
    
              
    for tb in tbHocKyList:
        tb.save()                       
       
    return pupilNoSum,noHanhKiem
@transaction.commit_on_success
def calculateTKMon(class_id):
    
    cnList = TKMon.objects.filter(subject_id__class_id=class_id,subject_id__primary=1).order_by('student_id__index','subject_id__index') 
    hk1List = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=1,subject_id__primary=1).order_by('student_id__index','subject_id__index') 

    #print cnList
    for hk1,cn in zip(hk1List,cnList):
        cn.tb_nam = hk1.tb

    cn1List = TKMon.objects.filter(subject_id__class_id=class_id,subject_id__primary=2).order_by('student_id__index','subject_id__index') 
    hk2List = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=2,subject_id__primary=2).order_by('student_id__index','subject_id__index') 

    #print cn1List
    for hk2,cn in zip(hk2List,cn1List):
        cn.tb_nam = hk2.tb

        
    for cn in cnList:
        cn.save()

    for cn in cn1List:
        cn.save()

          
@transaction.commit_on_success
def calculateOverallMarkYear(class_id=7):

    pupilNoSum =0
    subjectList= Subject.objects.filter(class_id=class_id,primary__in=[0,1,2]).order_by("index")    
    markList   = TKMon.objects.filter(subject_id__class_id=class_id,subject_id__primary__in=[0,1,2]).order_by('student_id__index','subject_id__index') 
    tbNamList  = TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    hkList     = HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')

    #calculateTKMon(class_id)

    length = len(subjectList)
    print length
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
    NN2List= TKMon.objects.filter(subject_id__class_id=class_id,subject_id__primary=3).order_by('student_id__index','subject_id__index') 

    if len(NN2List)>0:
        for nn2,tbNam in zip(NN2List,tbNamList):
            if (nn2.tb_nam!=None) & (tbNam.tb_nam!=None): 
                if  nn2.tb_nam+e>=8    : tbNam.tb_nam+=0.3
                elif  nn2.tb_nam+e>=6.5: tbNam.tb_nam+=0.2
                elif  nn2.tb_nam+e>=5  : tbNam.tb_nam+=0.1
        
    noHanhKiem = 0            
    for hk,tbNam in zip(hkList,tbNamList):
        loaiHk=hk.year
        if loaiHk==None: noHanhKiem+=1
        
        if (loaiHk==None) | (tbNam.hl_nam==None):
            tbNam.danh_hieu_nam=None
        elif (loaiHk=='T') & (tbNam.hl_nam=='G'): 
            tbNam.danh_hieu_nam='G'
        elif ((loaiHk=='T') | (loaiHk=='K')) & ((tbNam.hl_nam=='G') | (tbNam.hl_nam=='K')):
            tbNam.danh_hieu_nam='TT'
        else: tbNam.danh_hieu_nam='K'                                         
                
    for tb in tbNamList:
        tb.save()                       
       
    return pupilNoSum,noHanhKiem    
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
    pupilList     =Pupil.objects.filter(class_id=class_id).order_by('index')    

    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    tempList=[]
    list=[]
    # neu la hk1 hoac hk2
    termNumber=int(termNumber)
    
    if request.method=="POST":
        if termNumber <3 : noHl,noHk=calculateOverallMarkTerm(class_id,termNumber)
        else         : noHl,noHk=calculateOverallMarkYear(class_id)
        
        if (noHl==0) & (noHk==0):
            message="Đã có đủ điểm và hạnh kiểm của cả lớp"
        elif (noHl==0):
            message="Còn "+str(noHanhKiem)+" học sinh chưa có hạnh kiểm"
        elif (noHk==0):    
            message="Còn "+str(noHl)+" học sinh chưa đủ điểm "
        else:
            message="Còn "+str(noHl)+" học sinh chưa đủ điểm và "+str(noHk)+" học sinh chưa có hạnh kiểm"
                   
          
        
    if termNumber<3:        

        subjectList=Subject.objects.filter(class_id=class_id,primary__in=[0,termNumber,3])    
        markList = Mark.objects.filter(subject_id__class_id=class_id,term_id__number=termNumber,subject_id__primary__in=[0,termNumber,3]).order_by('student_id__index','subject_id__index') 
        tbHocKyList = TBHocKy.objects.filter(student_id__class_id=class_id,term_id__number=termNumber).order_by('student_id__index')
        hkList      = HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
        hkList1 =[]
        if termNumber==1:
            for hk in hkList:
                hkList1.append(hk.term1)
        else:
            for hk in hkList:
                hkList1.append(hk.term2)
                                        
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
                                    
        list=zip(pupilList,tempList,tbHocKyList,hkList1)    
    else:
        calculateTKMon(class_id)
        idYear = selectedYear.id
        subjectList=Subject.objects.filter(class_id=class_id)    
        markList   =TKMon.objects.filter(subject_id__class_id=class_id).order_by('student_id__index','subject_id__index') 
        tbNamList = TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
        hkList      = HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
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
                                    
        list=zip(pupilList,tempList,tbNamList,hkList)    
        
    

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

@transaction.commit_on_success                                                              
def xepLoaiLop(class_id):
    
    
    tbNamList    =TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    ddhk1List    =TKDiemDanh.objects.filter(student_id__class_id=class_id,term_id__number=1).order_by('student_id__index')
    ddhk2List    =TKDiemDanh.objects.filter(student_id__class_id=class_id,term_id__number=2).order_by('student_id__index')
    hanhKiemList =HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    repr(tbNamList)
    noHk=0
    noHl=0
    #for tt in tbNamList:
    #    pass
    i=0
    for tbNam,ddhk1,ddhk2,hk in zip(tbNamList,ddhk1List,ddhk2List,hanhKiemList):
        i+=1
        
        ddhk1.tong_so=DiemDanh.objects.filter(student_id=tbNam.student_id,term_id__number=1).count()
        ddhk2.tong_so=DiemDanh.objects.filter(student_id=tbNam.student_id,term_id__number=2).count()
        if hk.year==None     : noHk+=1
        if tbNam.hl_nam==None: noHl+=1
        
                        
        if (tbNam.hl_nam==None) |(hk.year==None):
            tbNam.danh_hieu_nam=None            
            tbNam.tong_so_ngay_nghi=ddhk1.tong_so+ddhk2.tong_so
            if tbNam.tong_so_ngay_nghi>45:
                tbNam.len_lop=False
                tbNam.thi_lai=None
                hk.ren_luyen_lai=None
            else:    
                tbNam.len_lop=None
                tbNam.thi_lai=None
                hk.ren_luyen_lai=None
                
        else:
            if (tbNam.hl_nam=='G') & (hk.year=='T'):
                tbNam.danh_hieu_nam='G'
            elif ((tbNam.hl_nam=='G') | (tbNam.hl_nam=='K') ) & ((hk.year=='T') | (hk.year=='K')):
                tbNam.danh_hieu_nam='TT'
            else:
                tbNam.danh_hieu_nam='K'
        
            tbNam.tong_so_ngay_nghi=ddhk1.tong_so+ddhk2.tong_so
            
            if tbNam.tong_so_ngay_nghi>45:
                tbNam.len_lop=False
                hk.ren_luyen_lai=None
                tbNam.thi_lai=None
                continue        

            if (tbNam.hl_nam!='Y') & (tbNam.hl_nam!='Kem') & (hk.year!='Y'):
                tbNam.len_lop=True
                tbNam.thi_lai=None
                hk.ren_luyen_lai=None
                continue
    
            if ((hk.year!='Y') & (tbNam.hl_nam=='Y')):
                tbNam.len_lop=None
                tbNam.thi_lai=True
                hk.ren_luyen_lai=None
            elif  ((hk.year=='Y')  & (tbNam.hl_nam!='Y') & (tbNam.hl_nam!='Kem')):
                tbNam.thi_lai=None
                tbNam.len_lop=None
                hk.ren_luyen_lai=True
                #if i==7: print "ddddee"    
            else:
                tbNam.len_lop=False
                tbNam.thi_lai=None
                hk.ren_luyen_lai=None
    """            
    for tb,hk1,hk2 in zip(tbNamList,ddhk1List,ddhk2List):
        tb.save()
        hk1.save()
        hk2.save()
    """
    for tb in tbNamList:
        tb.save()
    for dd in ddhk1List:
        dd.save()
    for dd in ddhk2List:
        dd.save()
    for hk in hanhKiemList:
        hk.save()            
    return noHl,noHk    
@transaction.commit_on_success                                                                                  
def xlCaNamTheoLop(request,class_id,type):
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
    if request.method=="POST":
        noHl,noHk=xepLoaiLop(class_id)
        if (noHl==0) & (noHk==0):
            message="Đã xếp loại xong cả lớp"
        elif (noHl==0):
            message="Còn "+str(noHanhKiem)+" học sinh chưa có hạnh kiểm"
        elif (noHk==0):    
            message="Còn "+str(noHl)+" học sinh chưa có học lực "
        else:
            message="Còn "+str(noHl)+" học sinh chưa có học lực và "+str(noHk)+" học sinh chưa có hạnh kiểm"
    

    pupilNoSum=0
    
    pupilList    =Pupil.objects.filter(class_id=class_id).order_by('index')
    tbNamList    =TBNam.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    hanhKiemList =HanhKiem.objects.filter(student_id__class_id=class_id).order_by('student_id__index')
    
    pupilList1=[]
    tbNamList1=[]
    hanhKiemList1=[]
    type=int(type)
    for p,tbNam,hk in zip(pupilList,tbNamList,hanhKiemList):
        ok=False
        if   type==1: ok=True
        elif type==2:
            if (tbNam.len_lop==None) & (tbNam.thi_lai==None) & (hk.ren_luyen_lai==None): ok=True
        elif type==3:
            if tbNam.danh_hieu_nam=='G': ok=True
        elif type==4:
            if tbNam.danh_hieu_nam=='TT': ok=True
        elif type==5:
            if tbNam.len_lop==True: ok=True
        elif type==6:
            if tbNam.len_lop==False: ok=True
        elif type==7:
            if tbNam.thi_lai==True: ok=True            
        elif type==8:
            if hk.ren_luyen_lai==True: ok=True
        if ok:    
            pupilList1.append(p)
            tbNamList1.append(tbNam)
            hanhKiemList1.append(hk)
            
    list= zip(pupilList1,tbNamList1,hanhKiemList1)             
    #print list
    yearString=str(selectedClass.year_id.time)+"-"+str(selectedClass.year_id.time+1)
    t = loader.get_template(os.path.join('school','xl_ca_nam_theo_lop.html'))
    t2=time.time()
    print (t2-t1)
    
    c = RequestContext(request, {"message":message,
                                 "selectedClass":selectedClass,
                                 "yearString":yearString,
                                 "list":list 
                                }
                       )
    

    return HttpResponse(t.render(c))

#------------------------------------------------------------------------------

# tong ket hoc ky, tinh lai toan bo hoc luc cua hoc sinh trong toan truong
# xem xet lop nao da tinh xong, lop nao chua xong de hieu truong co the chi dao
# co chuc nang ket thuc hoc ky
#-----------------------------------------------------------------------------



# liet ke danh sach cac lop da tinh xong hoc luc va cac  lop chua xong
def finishTermInSchool(term_id):
    selectedTerm = Term.objects.get(id=term_id)
    classList=Class.objects.filter(year_id=selectedTerm.year_id)
    termNumber = selectedTerm.number
    for c in classList:
        calculateOverallMarkTerm(c.id, termNumber)
    
def countDetailTerm(term_id):
    finishLearning=[]
    notFinishLearning=[]
    finishPractising=[]
    notFinishPractising=[]
    finishAll=[]
    notFinishAll=[]
    
    selectedTerm = Term.objects.get(id=term_id)
    classList=Class.objects.filter(year_id=selectedTerm.year_id)
    
    for c in classList:
        number = TBHocKy.objects.filter(term_id=term_id,student_id__class_id=c.id,hl_hk=None).count()
        if number==0:   finishLearning.append(c.name)
        else        :  notFinishLearning.append([c.name,number])
        
        if selectedTerm.number==1:        
            number = HanhKiem.objects.filter(year_id=selectedTerm.year_id,student_id__class_id=c.id,term1=None).count()
            if number==0:  finishPractising.append(c.name)
            else        :  notFinishPractising.append([c.name,number])
        else:
            number = HanhKiem.objects.filter(year_id=selectedTerm.year_id,student_id__class_id=c.id,term2=None).count()
            if number==0:  finishPractising.append(c.name)
            else        :  notFinishPractising.append([c.name,number])
                
        number = TBHocKy.objects.filter(term_id=term_id,student_id__class_id=c.id,danh_hieu_hk=None).count()
        if number==0:  finishAll.append(c.name)
        else        :  notFinishAll.append([c.name,number])
    return  finishLearning,notFinishLearning,finishPractising,notFinishPractising,finishAll,notFinishAll       

#@transaction.commit_on_success                                                                                  
def finishTerm(request,term_id=None):
    t1=time.time()
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
    
    if request.method == 'POST':
        if request.POST.get('finishTerm'):
            if request.POST['finishTerm']!=u'Khôi phục về trạng thái học kỳ trước':                
                request.user.userprofile.organization.status+=1 
            else:
                request.user.userprofile.organization.status=selectedTerm.number
                
            request.user.userprofile.organization.save()    
        if request.POST.get('tongKet'):
            finishTermInSchool(term_id)
            message="Đã tính tổng kết xong. Mời bạn xem kết quả phía dưới."
        
    
    selectedTerm= Term.objects.get(id=term_id)
    yearString=str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    finishLearning,notFinishLearning,finishPractising,notFinishPractising,finishAll,notFinishAll= countDetailTerm(term_id)
    
    hlList,pthlList = countTotalLearningInTerm(term_id)
    hkList,pthkList = countTotalPractisingInTerm(term_id)
    ddList,ptddList = countDanhHieuInTerm(term_id)

    currentTerm=get_current_term(request)            
    t = loader.get_template(os.path.join('school','finish_term.html'))
        
    t2=time.time()
    print (t2-t1)
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

def finishYearInSchool(year_id):
    
    classList=Class.objects.filter(year_id=year_id)
    for c in classList:
        calculateOverallMarkYear(c.id)
        xepLoaiLop(c.id)
        
def countDetailYear(year_id):
    finishLearning=[]
    notFinishLearning=[]
    finishPractising=[]
    notFinishPractising=[]
    finishAll=[]
    notFinishAll=[]
    
    classList=Class.objects.filter(year_id=year_id)
    
    for c in classList:
        
        number = TBNam.objects.filter(year_id=year_id,student_id__class_id=c.id,hl_nam=None).count()
        if number==0:   finishLearning.append(c.name)
        else        :  notFinishLearning.append([c.name,number])
        
        number = HanhKiem.objects.filter(year_id=year_id,student_id__class_id=c.id,year=None).count()
        if number==0:  finishPractising.append(c.name)
        else        :  notFinishPractising.append([c.name,number])
                
        number = TBNam.objects.filter(year_id=year_id,student_id__class_id=c.id,danh_hieu_nam=None).count()
        if number==0:  finishAll.append(c.name)
        else        :  notFinishAll.append([c.name,number])

    return  finishLearning,notFinishLearning,finishPractising,notFinishPractising,finishAll,notFinishAll       

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
    if request.method == 'POST':
        if request.POST.get('finishTerm'):
           if request.POST['finishTerm']!=u'Khôi phục về học kỳ II':
                request.user.userprofile.organization.status=3
           else:
                request.user.userprofile.organization.status=2
                
           request.user.userprofile.organization.save()
        if request.POST.get('tongKet'):
            finishYearInSchool(year_id)
            
            message="Đã tính tổng kết xong. Mời bạn xem kết quả phía dưới."
    
    yearString=str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    finishLearning,notFinishLearning,finishPractising,notFinishPractising,finishAll,notFinishAll= countDetailYear(year_id)
    
    
    hkList,pthkList = countTotalPractisingInYear(year_id)
    hlList,pthlList = countTotalLearningInYear(year_id)
    ddList,ptddList = countDanhHieuInYear(year_id)
    
    currentTerm = get_current_term(request)
                    
    t = loader.get_template(os.path.join('school','finish_year.html'))    
    c = RequestContext(request, {"message":message,
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

def thilai(request,class_id):
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
    tbNamList=TBNam.objects.filter(student_id__class_id=class_id,thi_lai=True).order_by('student_id__index')
    tbMonList=[]
    aTKMonList=[]
    for tbNam in tbNamList:
        aTKMonList = TKMon.objects.filter(subject_id__class_id=class_id,student_id=tbNam.student_id,subject_id__primary__in=[0,1,2])
        for tbMon in aTKMonList:
            if tbMon.tb_nam==None: message="Chưa tổng kết xong điểm của cả lớp"
            
            elif tbMon.tb_nam <5   : tbMon.thi_lai=True
            
        tbMonList.append(aTKMonList)
        print tbNam.hl_thi_lai
        
        if   tbNam.hl_thi_lai=='G'  : tbNam.hl_thi_lai='Giỏi'
        elif tbNam.hl_thi_lai=='K'  : tbNam.hl_thi_lai='Khá'
        elif tbNam.hl_thi_lai=='TB' : tbNam.hl_thi_lai='TB'
        elif tbNam.hl_thi_lai=='Y'  : tbNam.hl_thi_lai=u'Yếu'
        elif tbNam.hl_thi_lai=='Kem' : tbNam.hl_thi_lai='Kém'
        
        
        
    vtMonChuyen = -1
    vtMonToan   = -1
    vtMonVan    = -1

    
    i=0    
    for tkMon in aTKMonList:
        if tkMon.subject_id.hs==3: vtMonChuyen =i
        if    tkMon.subject_id.name.lower().__contains__(u'toán'):
            vtMonToan=i
        elif  tkMon.subject_id.name.lower().__contains__(u'văn'):
            vtMonVan=i   
        i+=1     

    
    list= zip(tbMonList,tbNamList)
    lengthList = len(list)
    if lengthList==0:
        message="Lớp chưa tổng kết xong hoặc không có học sinh nào phải thi lại"
    numberSubject= len(aTKMonList)
    
    yearString=str(selectedClass.year_id.time)+"-"+str(selectedClass.year_id.time+1)
    
    print message
    t = loader.get_template(os.path.join('school','thi_lai.html'))
    t2=time.time()
    print (t2-t1)
    
    c = RequestContext(request, {"message":message,
                                 "selectedClass":selectedClass,
                                 "yearString":yearString,
                                 'lengthList':lengthList,
                                 'numberSubject':numberSubject,
                                 'aTKMonList':aTKMonList,
                                 'vtMonChuyen':vtMonChuyen,
                                 'vtMonToan':vtMonToan,
                                 'vtMonVan':vtMonVan,
                                 "list":list,
                                }
                       )
    

    return HttpResponse(t.render(c))
def updateHocLai(str):
    strs = str.split('*')
    if   (strs[0]=='0'):
        print "f1"
        id = int(strs[1])
        tkMon = TKMon.objects.get(id=id)
        
        if strs[2]!='-1':
            tkMon.thi_lai=True        
            tkMon.diem_thi_lai = float(strs[2])
        else:
            tkMon.thi_lai=False        
            tkMon.diem_thi_lai = None
                
        tkMon.save()
        
    elif (strs[0]=='1'):
        print "f2"
        id = int(strs[1])
        tbNam = TBNam.objects.get(id=id)
        
        if strs[2]!='-1':
            tbNam.tb_thi_lai=float(strs[2])
        else:  
            tbNam.tb_thi_lai=None    
        tbNam.save()
    else:    
        print "f3"
        id = int(strs[1])
        tbNam = TBNam.objects.get(id=id)

        if strs[2]!='-1':
            tbNam.hl_thi_lai=strs[2]
            if (strs[2]!='Y') & (strs[2]!='Kem'): 
                tbNam.len_lop=True
            else:                                 
                tbNam.len_lop=False
        else:
            tbNam.hl_thi_lai=None
            tbNam.len_lop=None
                 
        tbNam.save()
                                 
def saveHocLai(request):
    message = 'hello'
    if request.method == 'POST':

        str = request.POST['str']
        strs=str.split(':')
        print str
        length = len(strs)
        for i in range(1,length):
            updateHocLai(strs[i])
                                                            
        message='ok'
        data = simplejson.dumps({'message': message})
        return HttpResponse( data, mimetype = 'json')   

def renluyenthem(request,class_id):
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
    hkList=HanhKiem.objects.filter(student_id__class_id=class_id,ren_luyen_lai=True).order_by('student_id__index')
    
    lengthList = len(hkList)
    if lengthList==0:
        message="Lớp chưa có hạnh kiểm cuối năm hoặc không có học sinh nào phải rèn luyện thêm"
    
    yearString=str(selectedClass.year_id.time)+"-"+str(selectedClass.year_id.time+1)
    
    print message
    t = loader.get_template(os.path.join('school','ren_luyen_them.html'))
    t2=time.time()
    print (t2-t1)
    
    c = RequestContext(request, {"message":message,
                                 "selectedClass":selectedClass,
                                 "yearString":yearString,
                                 'lengthList':lengthList,
                                 "hkList":hkList,
                                }
                       )
    

    return HttpResponse(t.render(c))
def saveRenLuyenThem(request):
    message = 'hello'
    if request.method == 'POST':

        str  = request.POST['str']
        strs =str.split(':')
        print str
        id = int(strs[0])
        
        hk = HanhKiem.objects.get(id=id)
        if strs[1]!='No':
            hk.hk_ren_luyen_lai= strs[1]
        else:     
            hk.hk_ren_luyen_lai= None
        
        tbNam = TBNam.objects.get(year_id=hk.year_id, student_id=hk.student_id)
        if strs[1]=='No':
            tbNam.len_lop=None
        elif strs[1]=='Y':
            tbNam.len_lop=False
        else:
            tbNam.len_lop=True       
            
        hk.save()
        tbNam.save()                                                         
        message='ok'
        data = simplejson.dumps({'message': message})
        return HttpResponse( data, mimetype = 'json')   
