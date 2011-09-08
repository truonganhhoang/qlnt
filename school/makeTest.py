from django.http import HttpResponse, HttpResponseRedirect
from school.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from school.utils import *
from django.core.urlresolvers import reverse
from django.db import transaction
import xlrd  
from  views import save_file 
import os.path 
import time 
import datetime
import random
LOCK_MARK =False
ENABLE_CHANGE_MARK=True

def thu(request):
    t1= time.time()
    t2= time.time()
    if request.method=='POST':
        print "chao"
        s=request.FILES.get('file')
        print s.name
        print s.size 
                       
        filename = save_file(request.FILES.get('file'), request.session)
        filepath = os.path.join(TEMP_FILE_LOCATION, filename)
       
        book = xlrd.open_workbook(filepath)
        sheet = book.sheet_by_index(0)
        
        print to_en1(sheet.cell(13,1).value)
        print book
        print sheet
        print "ffffffffffffff"
        
        
    print (t2-t1)
    t = loader.get_template(os.path.join('school','ll.html'))
    
    c = RequestContext(request, {
                                }
                       )
    
    #print (t2-t1)

    return HttpResponse(t.render(c))

@transaction.commit_on_success                                                              
def thu124(request):
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
    
    x='G'
    print (t2-t1)
    t = loader.get_template(os.path.join('school','ll.html'))
    
    c = RequestContext(request, {'x':x,
                                }
                       )
    
    #print (t2-t1)

    return HttpResponse(t.render(c))

@transaction.commit_on_success                                                              
def thu123(request):
    t1= time.time()
    list1 = TKMon.objects.filter(student_id__class_id=197)
    for m in list1:
        m.tb_nam=random.randrange( 7,11 )
       # m.save()
    for m in list1:
        m.save()
           
    list = Mark.objects.filter(student_id__class_id=197)
    for m in list:
        m.mieng_1 = random.randrange( 7,11 )
        m.mieng_2 = random.randrange( 7,11 )
        m.mieng_3 = random.randrange( 7,11 )
        m.mieng_4 = random.randrange( 7,11 )
        m.mieng_5 = random.randrange( 7,11 )

        m.mot_tiet_1 = random.randrange( 7,11 )
        m.mot_tiet_2 = random.randrange( 7,11 )
        m.mot_tiet_3 = random.randrange( 7,11 )
        m.mot_tiet_4 = random.randrange( 7,11 )
        m.mot_tiet_5 = random.randrange( 7,11 )
        m.ck=random.randrange( 7,11 )
        m.tb=random.randrange( 7,11 )
       # m.save()
    for m in list:
        m.save()
    print list       
    hanhKiemList =HanhKiem.objects.filter(student_id__class_id=197)
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
    
    t = loader.get_template(os.path.join('school','ll.html'))
    t2=time.time()
    print (t2-t1)
    c = RequestContext(request, {'list':list,
                                }
                       )

    #print (t2-t1)
    return HttpResponse(t.render(c))

def thu1(request):
    t1= time.time()
    
    markList = Mark.objects.filter(subject_id=1)
    for m in markList:
        m.mieng_1 = 7
        m.mieng_2 = 7
        m.mieng_3 = 7
        m.mieng_4 = 7
        m.mieng_5 = 7
        m.mlam_1 = 6
        m.mlam_2 = 6
        m.mlam_3 = 6
        m.mlam_4 = 6
        m.mlam_5 = 6
        m.mot_tiet_1= 8
        m.mot_tiet_2= 8
        m.mot_tiet_3= 8
        m.mot_tiet_4= 8
        m.mot_tiet_5= 8
        m.ck        = 9
        m.save() 
    t = loader.get_template(os.path.join('school','ll.html'))
    t2=time.time()
    print (t2-t1)
    c = RequestContext(request, {'list':list,
                                }
                       )

    #print (t2-t1)
    return HttpResponse(t.render(c))

