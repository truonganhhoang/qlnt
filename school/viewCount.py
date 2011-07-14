# author: luulethe@gmail.com 

# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.utils import *
from django.core.urlresolvers import reverse
import os.path 

def countTotalPractisingInTerm(term_id):
    slList  =[0,0,0,0,0]
    ptslList=[0,0,0,0,0]
    sum=0.0
    string=['T','K','TB','Y',None]
    for i in range(string.__len__()):
        slList[i]=HanhKiem.objects.filter(term_id=term_id,loai=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    
def countTotalLearningInTerm(term_id):
    slList  =[0,0,0,0,0,0]
    ptslList=[0,0,0,0,0,0]
    sum=0.0
    string=['G','K','TB','Y','Kem',None]
    for i in range(string.__len__()):
        slList[i]=TBHocKy.objects.filter(term_id=term_id,hl_hk=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    

def countDanhHieuInTerm(term_id):
    slList  =[0,0,0,0]
    ptslList=[0,0,0,0]
    sum=0.0
    string=['G','TT','K',None]
    for i in range(string.__len__()):
        slList[i]=TBHocKy.objects.filter(term_id=term_id,danh_hieu_hk=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    

def countTotalPractisingInYear(year_id):
    slList  =[0,0,0,0,0]
    ptslList=[0,0,0,0,0]
    sum=0.0
    string=['T','K','TB','Y',None]
    for i in range(string.__len__()):
        slList[i]=TBNam.objects.filter(year_id=year_id,hk_nam=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    
def countTotalLearningInYear(year_id):
    slList  =[0,0,0,0,0,0]
    ptslList=[0,0,0,0,0,0]
    sum=0.0
    string=['G','K','TB','Y','Kem',None]
    for i in range(string.__len__()):
        slList[i]=TBNam.objects.filter(year_id=year_id,hl_nam=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    

def countDanhHieuInYear(year_id):
    slList  =[0,0,0,0]
    ptslList=[0,0,0,0]
    sum=0.0
    string=['G','TT','K',None]
    for i in range(string.__len__()):
        slList[i]=TBNam.objects.filter(year_id=year_id,danh_hieu_nam=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    
def countPassInYear(year_id):
    slList  =[0,0,0,0,0]
    ptslList=[0,0,0,0,0]
    
    sum=0.0
    slList[0]=TBNam.objects.filter(year_id=year_id,len_lop=True).count()
    slList[1]=TBNam.objects.filter(year_id=year_id,len_lop=False).count()
    slList[2]=TBNam.objects.filter(year_id=year_id,thi_lai=True).count()
    slList[3]=TBNam.objects.filter(year_id=year_id,ren_luyen_lai=True).count()
    slList[4]=TBNam.objects.filter(year_id=year_id,len_lop=None).count()
    for i in range(slList.__len__()):
        sum+=slList[i]
    
    
    if sum!=0:    
        for i in range( slList.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList    
    
def countInSchool(request,year_id=None):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))


    
    message=None
    
    if year_id==None:
        year_id=get_current_year(request).id
    
    selectedYear =Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')

    #currentTerm.year_id.school_id.status=1    
    #currentTerm.year_id.school_id.save()
    
    currentTerm= get_current_term(request)
    hkList,pthkList = countTotalPractisingInTerm(currentTerm.id)
    hlList,pthlList = countTotalLearningInTerm(currentTerm.id)
    ddList,ptddList = countDanhHieuInTerm(currentTerm.id)
    
    hkcnList=pthkcnList=hlcnList=pthlcnList=passedList=ptPassedList=ddcnList=ptddcnList=None
    
    if currentTerm.number==2:
        hkcnList,pthkcnList = countTotalPractisingInYear(year_id)
        hlcnList,pthlcnList = countTotalLearningInYear(year_id)
        ddcnList,ptddcnList = countDanhHieuInYear(year_id)
        passedList,ptPassedList  =countPassInYear(year_id) 
    
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
                                 'currentTerm':currentTerm,
                                 
                                 'hkList':hkList,
                                 'pthkList':pthkList,
                                 'hlList':hlList,
                                 'pthlList':pthlList,
                                 'ddList':ddList,
                                 'ptddList':ptddList,
                                 
                                 'hkcnList':hkcnList,
                                 'pthkcnList':pthkcnList,
                                 'hlcnList':hlcnList,
                                 'pthlcnList':pthlcnList,
                                 'ddcnList':ddcnList,
                                 'ptddcnList':ptddcnList,
                                 'passedList':passedList,
                                 'ptPassedList':ptPassedList,                                 
                                }
                       )
    return HttpResponse(t.render(c))

def countPractisingInClassInTerm(class_id,term_id):
    slList  =[0,0,0,0,0]
    ptslList=[0,0,0,0,0]
    sum=0.0
    string=['T','K','TB','Y',None]
    for i in range(string.__len__()):
        slList[i]=HanhKiem.objects.filter(term_id=term_id,student_id__class_id=class_id,loai=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList,sum    
                
def countPractisingInTerm(request,term_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedTerm=Term.objects.get(id=term_id)    
    try:
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) != 4:
       return HttpResponseRedirect('/school')

    
    message=None
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    
    list=[]

    totalSlList=[0,0,0,0,0]
    totalPtList=[0,0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countPractisingInClassInTerm(c.id,term_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))

def countPractisingInClassInYear(class_id,year_id):
    slList  =[0,0,0,0,0]
    ptslList=[0,0,0,0,0]
    sum=0.0
    string=['T','K','TB','Y',None]
    for i in range(string.__len__()):
        slList[i]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,hk_nam=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList,sum    


def countPractisingInYear(request,year_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedYear=Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) != 4:
       return HttpResponseRedirect('/school')

    message=None    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    list=[]
    
    totalSlList=[0,0,0,0,0]
    totalPtList=[0,0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countPractisingInClassInYear(c.id,year_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))


def countLearningInClassInTerm(class_id,term_id):
    slList  =[0,0,0,0,0,0]
    ptslList=[0,0,0,0,0,0]
    sum=0.0
    string=['G','K','TB','Y','Kem',None]
    for i in range(string.__len__()):
        slList[i]=TBHocKy.objects.filter(term_id=term_id,hl_hk=string[i],student_id__class_id=class_id).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList,sum    
                
def countLearningInTerm(request,term_id):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedTerm=Term.objects.get(id=term_id)    
    try:
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
        
    message=None
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    list=[]
    
    totalSlList=[0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countLearningInClassInTerm(c.id,term_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))


def countLearningInClassInYear(class_id,year_id):
    slList  =[0,0,0,0,0,0]
    ptslList=[0,0,0,0,0,0]
    sum=0.0
    string=['G','K','TB','Y','Kem',None]
    for i in range(string.__len__()):
        slList[i]=TBNam.objects.filter(year_id=year_id,hl_nam=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList,sum    

def countLearningInYear(request,year_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedYear=Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    message=None
    selectedYear=Year.objects.get(id=year_id)    
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    list=[]
    
    totalSlList=[0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countLearningInClassInYear(c.id,year_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))


def countAllInClassInTerm(class_id,term_id):
    slList  =[0,0,0,0]
    ptslList=[0,0,0,0]
    sum=0.0
    string=['G','TT','K',None]
    for i in range(string.__len__()):
        slList[i]=TBHocKy.objects.filter(term_id=term_id,student_id__class_id=class_id,danh_hieu_hk=string[i]).count()
        sum+=slList[i]
    if sum!=0:    
        for i in range(string.__len__()):
            ptslList[i]=slList[i]/sum *100
                            
    return slList,ptslList ,sum   
                
def countAllInTerm(request,term_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedTerm=Term.objects.get(id=term_id)    
    try:
        if in_school(request,selectedTerm.year_id.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    message=None
    selectedTerm=Term.objects.get(id=term_id)    
    yearString = str(selectedTerm.year_id.time)+"-"+str(selectedTerm.year_id.time+1)
    
    selectedYear=Year.objects.get(id=selectedTerm.year_id.id)
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    list=[]
    
    totalSlList=[0,0,0,0]
    totalPtList=[0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countAllInClassInTerm(c.id,term_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 "selectedTerm":selectedTerm,
                                 'yearString':yearString,
                                 'totalSlList':totalSlList,
                                 'totalPtList':totalPtList,
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))


def countAllInClassInYear(class_id,year_id):
    slList=[0,0,0,0,0,0,0]
    ptList=[0,0,0,0,0,0,0]

    slList[0]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,danh_hieu_nam='G').count()
    slList[1]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,danh_hieu_nam='TT').count()
    slList[2]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,len_lop=True).count()
    slList[3]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,len_lop=False).count()
    slList[4]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,thi_lai=True).count()
    slList[5]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,ren_luyen_lai=True).count()    
    slList[6]=TBNam.objects.filter(year_id=year_id,student_id__class_id=class_id,len_lop=None,thi_lai=None,ren_luyen_lai=None).count()
                
    sum=0
    for i in range(2,7):
        sum+=slList[i]
        
    if (sum!=0):        
        for i in range(7):
            ptList[i]=float(slList[i])/sum *100
        
    return slList,ptList,sum
                
def countAllInYear(request,year_id):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))

    selectedYear=Year.objects.get(id=year_id)    
    try:
        if in_school(request,selectedYear.school_id) == False:
            return HttpResponseRedirect('/school')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) != 4:
       return HttpResponseRedirect('/school')
    
    message=None
    selectedYear=Year.objects.get(id=year_id)
    yearString = str(selectedYear.time)+"-"+str(selectedYear.time+1)
    
    
    classList=selectedYear.class_set.all().order_by("block_id__number")
    list=[]
    
    totalSlList=[0,0,0,0,0,0,0]
    totalPtList=[0,0,0,0,0,0,0]

    for c in classList:
        aslList,aptList,sum =countAllInClassInYear(c.id,year_id)
        list.append([c.name,sum,zip(aslList,aptList)])
                   
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
                                 'list':list,
                                }
                       )
    return HttpResponse(t.render(c))


