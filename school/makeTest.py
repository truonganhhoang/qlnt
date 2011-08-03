from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.utils import *
from django.core.urlresolvers import reverse
from django.db import transaction

import os.path 
import time 
import datetime
import random
LOCK_MARK =False
ENABLE_CHANGE_MARK=True

@transaction.commit_on_success                                                              
def thu1(request):
    t1= time.time()
    
    diemdanh = DiemDanh.objects.all()
    print diemdanh.count()
    diemdanh.delete()
    
    """
    sum = Pupil.objects.filter(class_id=1).count()    
    pupilList = Pupil.objects.filter(class_id=1)
    sum = pupilList.count()
    termList= Term.objects.all()
    datet =datetime.datetime.now()
    date = datet.date 
    for i in range(100000):
        try:
            dd = DiemDanh()
            dd.loai       ="co phep"
            dd.term_id    = termList[random.randrange( 1,3)]
            dd.student_id = pupilList[random.randrange( 1,sum)]
            date = datetime.datetime(random.randrange( 1,2007),random.randrange( 1,13),random.randrange( 1,28))
            dd.time =date  
            dd.save()
            if i % 100==0: print i
        except Exception as e:
            print e   
    """    
    t2=time.time()
    
    
    print (t2-t1)
    t = loader.get_template(os.path.join('school','ll.html'))
    
    c = RequestContext(request, {'list':list,
                                }
                       )
    
    #print (t2-t1)

    return HttpResponse(t.render(c))

@transaction.commit_on_success                                                              
def thu(request):
    t1= time.time()
    """
    list1 = TKMon.objects.filter(student_id__class_id=1)
    for m in list1:
        m.tb_nam=random.randrange( 6,11 )
       # m.save()
    for m in list1:
        m.save()
           
    list = Mark.objects.filter(student_id__class_id=1)
    for m in list:
        m.tb=random.randrange( 7,11 )
       # m.save()
    for m in list:
        m.save()
           
    hanhKiemList =HanhKiem.objects.filter(student_id__class_id=1)
    for hk in hanhKiemList:
        t =random.randrange( 1,5 )
        if   t==1: hk.year='T'
        elif t==2: hk.year='K'
        elif t==3: hk.year='TB'
        elif t==4: hk.year='Y'

        t =random.randrange( 1,5 )
        if   t==1: hk.term1='T'
        elif t==2: hk.term1='K'
        elif t==3: hk.term1='TB'
        elif t==4: hk.term1='Y'

        t =random.randrange( 1,3 )
        if   t==1: hk.term2='T'
        elif t==2: hk.term2='K'
        elif t==3: hk.term2='TB'
        elif t==4: hk.term2='Y'
        
        hk.save()
    
    """
    t = loader.get_template(os.path.join('school','ll.html'))
    t2=time.time()
    print (t2-t1)
    c = RequestContext(request, {'list':list,
                                }
                       )

    #print (t2-t1)
    return HttpResponse(t.render(c))
