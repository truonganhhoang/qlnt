# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
import os.path 

def countInSchool(request,year_id):
    message=None
    selectedYear=Year.objects.get(id=year_id)
    firstTerm = Term.objects.get(year_id=year_id,number=1)
    secondTerm = Term.objects.get(year_id=year_id,number=2)
    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    t = loader.get_template(os.path.join('school','count_in_school.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'selectedYear':selectedYear,
                                 'firstTerm':firstTerm,
                                 'secondTerm':secondTerm,
                                }
                       )
    return HttpResponse(t.render(c))

def countPractisingInClassInTerm(class_id,term_id):
    slList=[0,0,0,0,0]
    ptList=[0,0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        hanhKiem = stu.hanhkiem_set.get(term_id=term_id)
        if hanhKiem.loai=='T':
            slList[0]+=1
        elif hanhKiem.loai=='K':
            slList[1]+=1
        elif hanhKiem.loai=='TB':
            slList[2]+=1
        elif hanhKiem.loai=='Y':
            slList[3]+=1
        else:
            slList[4]+=1
    sum=0
    for sl in slList:
        sum+=sl
    if (sum!=0):        
        for i in range(5):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList
                
def countPractisingInTerm(request,term_id):
    message=None
    selectedTerm=Term.objects.get(id=term_id)    
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0,0]
    totalPtList=[0,0,0,0,0]

    for c in classList:
        aslList,aptList =countPractisingInClassInTerm(c.id,term_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(5):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(5):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(5):
            totalPtList[i]=float(totalSlList[i])/sum *100             

    t = loader.get_template(os.path.join('school','count_practising_in_term.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'selectedTerm':selectedTerm,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))

def countPractisingInClassInYear(class_id,year_id):
    slList=[0,0,0,0,0]
    ptList=[0,0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        tbNam = stu.tbnam_set.get(year_id=year_id)
        if tbNam.hk_nam=='T':
            slList[0]+=1
        elif tbNam.hk_nam=='K':
            slList[1]+=1
        elif tbNam.hk_nam=='TB':
            slList[2]+=1
        elif tbNam.hk_nam=='Y':
            slList[3]+=1
        else:
            slList[4]+=1
    sum=0
    for sl in slList:
        sum+=sl
    if (sum!=0):        
        for i in range(5):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList


def countPractisingInYear(request,year_id):
    message=None
    
    selectedYear=Year.objects.get(id=year_id)    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0,0]
    totalPtList=[0,0,0,0,0]

    for c in classList:
        aslList,aptList =countPractisingInClassInYear(c.id,year_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(5):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(5):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(5):
            totalPtList[i]=float(totalSlList[i])/sum *100             
    t = loader.get_template(os.path.join('school','count_practising_in_year.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'selectedYear':selectedYear,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))


def countLearningInClassInTerm(class_id,term_id):
    slList=[0,0,0,0,0,0]
    ptList=[0,0,0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        tbHocKy = stu.tbhocky_set.get(term_id=term_id)
        if tbHocKy.hl_hk=='G':
            slList[0]+=1
        elif tbHocKy.hl_hk=='K':
            slList[1]+=1
        elif tbHocKy.hl_hk=='TB':
            slList[2]+=1
        elif tbHocKy.hl_hk=='Y':
            slList[3]+=1
        elif tbHocKy.hl_hk=='Kem':
            slList[4]+=1
        else:    
            slList[5]+=1
    sum=0
    for sl in slList:
        sum+=sl
    if (sum!=0):        
        for i in range(6):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList
                
def countLearningInTerm(request,term_id):
    message=None
    selectedTerm=Term.objects.get(id=term_id)    
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0]

    for c in classList:
        aslList,aptList =countLearningInClassInTerm(c.id,term_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(6):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(6):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(6):
            totalPtList[i]=float(totalSlList[i])/sum *100             

    t = loader.get_template(os.path.join('school','count_learning_in_term.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'selectedTerm':selectedTerm,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))


def countLearningInClassInYear(class_id,year_id):
    slList=[0,0,0,0,0,0]
    ptList=[0,0,0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        tbNam = stu.tbnam_set.get(year_id=year_id)
        if tbNam.hl_nam=='G':
            slList[0]+=1
        elif tbNam.hl_nam=='K':
            slList[1]+=1
        elif tbNam.hl_nam=='TB':
            slList[2]+=1
        elif tbNam.hl_nam=='Y':
            slList[3]+=1
        elif tbNam.hl_nam=='Kem':
            slList[4]+=1
        else:    
            slList[5]+=1
    sum=0
    for sl in slList:
        sum+=sl
    if (sum!=0):        
        for i in range(6):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList
                
def countLearningInYear(request,year_id):
    message=None
    
    selectedYear=Year.objects.get(id=year_id)    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0]

    for c in classList:
        aslList,aptList =countLearningInClassInYear(c.id,year_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(6):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(6):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(6):
            totalPtList[i]=float(totalSlList[i])/sum *100             

    t = loader.get_template(os.path.join('school','count_learning_in_year.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))


def countAllInClassInTerm(class_id,term_id):
    slList=[0,0,0,0]
    ptList=[0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        tbHocKy = stu.tbhocky_set.get(term_id=term_id)
        if tbHocKy.danh_hieu_hk=='G':
            slList[0]+=1
        elif tbHocKy.danh_hieu_hk=='TT':
            slList[1]+=1
        elif tbHocKy.danh_hieu_hk=='K':
            slList[2]+=1
        else:    
            slList[3]+=1
    sum=0
    for sl in slList:
        sum+=sl
    if (sum!=0):        
        for i in range(4):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList
                
def countAllInTerm(request,term_id):
    message=None
    selectedTerm=Term.objects.get(id=term_id)    
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0]
    totalPtList=[0,0,0,0]

    for c in classList:
        aslList,aptList =countAllInClassInTerm(c.id,term_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(4):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(4):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(4):
            totalPtList[i]=float(totalSlList[i])/sum *100             

    t = loader.get_template(os.path.join('school','count_all_in_term.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'selectedTerm':selectedTerm,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))


def countAllInClassInYear(class_id,year_id):
    slList=[0,0,0,0,0,0,0]
    ptList=[0,0,0,0,0,0,0]

    studentList = Pupil.objects.filter(class_id=class_id)
    for stu in studentList :
        tbNam = stu.tbnam_set.get(year_id=year_id)
        if tbNam.danh_hieu_nam=='G':
            slList[0]+=1
        elif tbNam.danh_hieu_nam=='TT':
            slList[1]+=1
            
        if tbNam.len_lop==True:
            slList[2]+=1
        elif tbNam.len_lop==False:
            slList[3]+=1
        elif tbNam.thi_lai==True:
            slList[4]+=1
        elif tbNam.ren_luyen_lai==True:
            slList[5]+=1
        else:
            slList[6]+=1            
                
    sum=0
    for i in range(2,7):
        sum+=slList[i]
        
    if (sum!=0):        
        for i in range(7):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList
                
def countAllInYear(request,year_id):
    message=None
    selectedYear=Year.objects.get(id=year_id)
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    slList=[]
    ptList=[]
    
    totalSlList=[0,0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0,0]

    for c in classList:
        aslList,aptList =countAllInClassInYear(c.id,year_id)
        slList.append([c,aslList])
        ptList.append([c,aptList])
                   
        for i in range(7):
            totalSlList[i]+=aslList[i]
    sum=0
    for i in range(2,7):
      sum+=totalSlList[i]
    if sum!=0:  
        for i in range(7):
            totalPtList[i]=float(totalSlList[i])/sum *100             

    t = loader.get_template(os.path.join('school','count_all_in_year.html'))    
    c = RequestContext(request, {"message":message,
                                 'yearString':yearString,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'slList':slList,
                                 'ptList':ptList,
                                }
                       )
    return HttpResponse(t.render(c))


