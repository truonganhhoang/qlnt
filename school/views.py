# -*- coding: utf-8 -*-

# Create your views here.
import os.path
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *
from school.models import *
from school.school_settings import *
import xlrd

NHAP_DANH_SACH_TRUNG_TUYEN = r'school/import/nhap_danh_sach_trung_tuyen.html'
DANH_SACH_TRUNG_TUYEN = r'school/import/danh_sach_trung_tuyen.html'
START_YEAR = r'school/start_year.html'
TEMP_FILE_LOCATION = os.path.dirname(__file__)

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
def school_index(request):
    school = School.objects.get( school_code = 'NT') # it's for testing, actually, it should be: school = School.objects.get(id = request['school_id'])
    if request.method == "POST":
        if request.POST['clickedButton'] == "start_year":
            request.session['school'] = school       
            return HttpResponseRedirect(reverse('start_year'))
        elif request.POST['clickedButton'] == "start_second_term":
            context = RequestContext(request, {'school':school})
            return render_to_response(r'school/start_second_term.html', context_instance = context)
        elif request.POST['clickedButton'] == "finish_year":
            context = RequestContext(request, {'school':school})
            return render_to_response(r'school/finish_year.html', context_instance = context)    
    context = RequestContext(request, {'school':school})
    return render_to_response(r'school/school.html', context_instance = context)
    
def b1(request):
    # tao moi cac khoi neu truong moi thanh lap
    school = request.session['school']
    if school.school_level == 1:
        lower_bound = 1
        upper_bound = 5
        ds_mon_hoc = CAP1_DS_MON
    elif school.school_level == 2:
        lower_bound = 6
        upper_bound = 9
        ds_mon_hoc = CAP2_DS_MON
    else:
        lower_bound = 10
        upper_bound = 12
        ds_mon_hoc = CAP3_DS_MON
        
    if school.status == 0:
        for khoi in range(lower_bound, upper_bound+1):
            block = Block()
            block.number = khoi
            block.school_id = school
            block.save()
        school.status = 1
        school.save()
    # tao nam hoc moi
    current_year = datetime.datetime.now().year
    year = school.year_set.filter( time__exact = current_year)
    if not year:
        # create new year
        year = Year()
        year.time = current_year
        year.school_id = school
        year.save()
        # create new StartYear
        start_year = StartYear()
        start_year.time = current_year
        start_year.school_id = school
        start_year.save()
        # create new term
        term = Term()
        term.number = 1
        term.year_id = year
        term.save()
        # create new class.
        # -- tao cac lop ---
        for khoi in range(lower_bound, upper_bound+1):
            block = school.block_set.filter( number__exact = khoi)
            if block:
                block = block[0]
            else:
                raise Exception(u'Khối' + str(khoi) + u'chưa đc tạo')
                
            print block
            loai_lop = school.danhsachloailop_set.all()
            for class_name in loai_lop:
                _class = Class()
                _class.name = str(block.number) + ' ' + class_name.loai
                _class.status = 1
                _class.block_id = block
                _class.year_id = year
                _class.save()
                for mon in ds_mon_hoc:
                    subject = Subject()
                    subject.name = mon
                    subject.hs = 1
                    subject.class_id = _class
                    subject.save()
        # -- day cac hoc sinh len lop        
        last_year = school.year_set.filter( time__exact = current_year -1)
        if last_year:
            blocks = school.block_set.all()
            for block in blocks:
                if block.number == upper_bound:
                    classes = block.class_set.all()
                    for _class in classes:
                        students = _class.pupil_set.all()
                        for student in students:
                            if (student.tbnam_set.get( year_id = last_year).len_lop):
                                student.disable = False
                                student.class_id = None
                                student.save()
                            else: # TRUONG HOP LUU BAN
                                pass
                else:
                    classes = block.class_set.all()
                    for _class in classes:
                        students = _class.pupil_set.all()
                        for student in students:
                            if (student.tbnam_set.get( year_id = last_year).len_lop):
                                new_block = year.block_set.get( number = block.number+1)
                                new_class_name = str(new_block.number) + ' ' + student.class_id.name.split()[1]
                                print new_class_name
                                new_class = new_block.class_set.get( name = new_class_name)
                                student.class_id = new_class
                                student.save()
                            else:
                                pass
        else: # truong ko co nam cu
            pass
        # render HTML
    else: 
        #raise Exception(u'Start_year: đã bắt đầu năm học rồi ?')    
        pass
    context = RequestContext(request, {'school':school})
    return render_to_response(START_YEAR, context_instance = context)                                            
def classes(request):
    message = None
    form = ClassForm()
    classList = Class.objects.all()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'You have added new class'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/classes.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'classList' : classList})
    return HttpResponse(t.render(c))

def viewClassDetail(request, class_id):
    class_view = Class.objects.get(id = class_id)
    t = loader.get_template('school/classDetail.html')
    c = RequestContext(request, {'class_view' : class_view})
    return HttpResponse(t.render(c))

def teachers(request):
    message = None
    form = TeacherForm()
    teacherList = Teacher.objects.all()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'You have added new teacher'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/teachers.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'teacherList' : teacherList})
    return HttpResponse(t.render(c))

def viewTeacherDetail(request, teacher_id):
    message = None
    teacher = Teacher.objects.get(id = teacher_id);
    form = TeacherForm (instance = teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance = teacher)
        if form.is_valid():
            form.save()
            message = 'You have updated successfully'
        else:
            message = 'Please check again'
    
    t = loader.get_template('school/teacher_detail.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'id' : teacher_id})
    return HttpResponse(t.render(c))

def subjectPerClass(request, class_id):
    message = None
    subjectList = Subject.objects.filter(class_id = class_id)
    form = SubjectForm()
    if request.method == 'POST':
        data = {'name':request.POST['name'], 'hs':request.POST['hs'], 'class_id':class_id, 'teacher_id':request.POST['teacher_id']}
        form = SubjectForm(data)
        if form.is_valid():
            form.save()
            message = 'You have added new subject'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/subject_per_class.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'subjectList' : subjectList, 'class_id' : class_id})
    return HttpResponse(t.render(c))

def studentPerClass(request, class_id):
    print ">>", class_id
    message = None
    form = PupilForm()
    studentList = Pupil.objects.filter(class_id = class_id)
    if request.method == 'POST':
        data = {'first_name':request.POST['first_name'], 'last_name':request.POST['last_name'],
        'birthday':request.POST['birthday'], 'class_id':class_id, 'sex':request.POST['sex'], 'ban_dk':request.POST['ban_dk'], 'school_join_date':request.POST['school_join_date'], 'start_year_id':request.POST['start_year_id']}
        print ">>", data
        form = PupilForm(data)
        if form.is_valid():
            form.save()
            message = 'You have added new student'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/student_per_class.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'studentList' : studentList, 'class_id' : class_id})
    return HttpResponse(t.render(c))

def students(request):
    message = None
    form = PupilForm()
    studentList = Pupil.objects.all()
    if request.method == 'POST':
        #data = {'first_name':request.POST['first_name'], 'last_name':request.POST['last_name'], 'birthday':request.POST['birthday'], 'sex':request.POST['sex'],'ban_dk':request.POST['ban_dk'], 'school_join_date':request.POST['school_join_date'], 'start_year_id':request.POST['start_year_id'], 'class_id' : request.POST['class_id']}
        form = PupilForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'You have added new student'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/students.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'studentList' : studentList})
    return HttpResponse(t.render(c))

def viewStudentDetail(request, student_id):
    message = None
    pupil = Pupil.objects.get(id = student_id);
    form = PupilForm (instance = pupil)
    if request.method == 'POST':
        form = PupilForm(request.POST, instance = pupil)
        if form.is_valid():
            form.save()
            message = 'You have updated successfully'
        else:
            message = 'Please check again'

    t = loader.get_template('school/student_detail.html')
    c = RequestContext(request, {'form' : form, 'message' : message, 'id' : student_id})
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
    t = loader.get_template('school/mark_table.html')
    
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
                                    
        
    t = loader.get_template('school/mark_for_a_student.html')
    
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
    t = loader.get_template('school/mark_for_a_subject.html')
    
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
    if pupilNoSum==0:
        message=None
    else:      
        message=u'lớp '+selectedClass.__unicode__()+u' có ' +str(pupilNoSum)+ u' học sinh chưa được tổng kết học kỳ '+str(termNumber)
    return message    
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
    


    t = loader.get_template('school/xep_loai_hl_theo_lop.html')
    
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
def finishTerm(request,term_id=8):
    
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
    t = loader.get_template('school/finish_term.html')
    c = RequestContext(request, {"message":message, 
                                 "finishList":finishList,
                                 "notFinishList":notFinishList,
                                 "selectedTerm":selectedTerm,
                                 "yearString":yearString,
                                }
                       )
    

    return HttpResponse(t.render(c))

# tinh diem tong ket va tinh hoc luc cua tat ca hoc sinh trong toan truong theo nam 

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
    t = loader.get_template('school/finish_year.html')
    c = RequestContext(request, {"message":message, 
                                 "finishList":finishList,
                                 "notFinishList":notFinishList,
                                 "yearString":yearString,
                                }
                       )
    

    return HttpResponse(t.render(c))

#----------- Exporting and Importing form Excel -------------------------------------

class UploadImportFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        print "Access __init___" 
        class_list = kwargs.pop('class_list')
        print "in form: ", class_list
        super(UploadImportFileForm, self).__init__(*args, **kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Chọn lớp:', choices = class_list, required = False)
        self.fields['import_file'] = forms.FileField(label=u'Chọn file excel:')
        
def to_date(value ):
    v=value.split('-')
    return date( int(v[2]), int(v[1]), int(v[0]))

def save_file( import_file, session):
    import_file_name = import_file.name
    session_key = session.session_key
    save_file_name = session_key + import_file_name
    saved_file = open(os.path.join(TEMP_FILE_LOCATION, save_file_name), 'wb+')
    for chunk in import_file.chunks():
        saved_file.write(chunk)
    saved_file.close()
    return save_file_name

def process_file( file_name, task):
    if task == "Nhap danh sach trung tuyen":
        student_list=[]
        filepath = os.path.join(TEMP_FILE_LOCATION, file_name)
        if not os.path.isfile(filepath):
            raise NameError, "%s is not a valid filename" % file_name
        book = xlrd.open_workbook(filepath)
        sheet = book.sheet_by_index(0)
        
        start_row = -1;
        for c in range(0, sheet.ncols):
            flag = False
            for r in range(0, sheet.nrows):
                if ( sheet.cell_value(r, c) == u'Tên'):
                    start_row = r
                    flag = True
                    break
            if flag: break
        #                                                             CHUA BIEN LUAN TRUONG HOP: start_row = -1, ko co cot ten: Mã học sinh
        # start_row != 0
        c_ten =-1
        c_ngay_sinh =-1
        c_tong_diem =-1
        c_nguyen_vong=-1
        for c in range(0, sheet.ncols):
            value = sheet.cell_value(start_row, c)
            if ( value == u'Tên'):
                c_ten = c
            elif ( value == u'Ngày sinh'):
                c_ngay_sinh = c
            elif ( value == u'Tổng điểm'):
                c_tong_diem = c
            elif ( value == u'Nguyện vọng'):
                c_nguyen_vong = c
        
        print "ten ", c_ten
        print "ngay sinh ", c_ngay_sinh
        print "tong diem ", c_tong_diem
        print "nv ", c_nguyen_vong
        for r in range(start_row + 1, sheet.nrows):
            name = sheet.cell_value( r, c_ten)
            print "->", sheet.cell(r, c_ngay_sinh).value
            birthday = sheet.cell(r, c_ngay_sinh).value
            nv = sheet.cell_value( r, c_nguyen_vong)
            tong_diem = sheet.cell_value( r, c_tong_diem)
            if ( name == "" or birthday =="" or nv == "" or tong_diem =="" ):
                print "co 1 cell empty or blank"
                continue
            date_value = xlrd.xldate_as_tuple(sheet.cell( r, c_ngay_sinh).value, book.datemode)
            birthday = date(*date_value[:3])
            student_list.append( { 'ten': name,\
                                   'ngay_sinh': birthday,\
                                   'nguyen_vong': nv, \
                                   'tong_diem': tong_diem, }) 
        return student_list
    else: task == ""
    
    return None

def nhap_danh_sach_trung_tuyen(request):
    school = request.session['school']
    _class_list = [(u'0',u'---')]
    try:
        this_year = school.year_set.latest('time')
        temp = this_year.class_set.all()
        for _class in temp:
            _class_list.append((_class.id, _class.name))
    except Exception as e:
        print e
        _class_list = None
    print _class_list
    if request.method == 'POST':
        form = UploadImportFileForm(request.POST, request.FILES, class_list = _class_list)
        if form.is_valid():
            save_file_name = save_file(form.cleaned_data['import_file'], request.session)
            chosen_class = form.cleaned_data['the_class']
            print save_file_name
            request.session['save_file_name'] = save_file_name
            request.session['chosen_class'] = chosen_class
            student_list = process_file(file_name = save_file_name, \
                                        task = "Nhap danh sach trung tuyen")
            #print student_list
            request.session['student_list'] = student_list
            return HttpResponseRedirect(reverse('imported_list'))
    else:
        form = UploadImportFileForm(class_list = _class_list)
    print request.session['school']
    context = RequestContext(request, {'form':form,})
    return render_to_response(NHAP_DANH_SACH_TRUNG_TUYEN, context_instance = context)
        
def danh_sach_trung_tuyen(request):
    student_list = request.session['student_list']
    school = request.session['school']
    chosen_class = request.session['chosen_class']
    print "chosen_class: ", chosen_class
    if chosen_class != u'0':
        chosen_class = school.year_set.latest('time').class_set.get(id = chosen_class)
    else:
        chosen_class = None
    message = None
   
    if request.method == 'POST':
        print ">>>", request.POST['clickedButton']
        if request.POST['clickedButton'] == 'save':
            print "button save has been clicked "
            year = school.startyear_set.get( time = datetime.date.today().year)
            today = datetime.date.today()   
            for student in student_list:
                name = student['ten'].split()
                last_name = ' '.join(name[:len(name)-1])
                first_name= name[len(name)-1]
                find = year.pupil_set.filter( first_name__exact = first_name)\
                                     .filter(last_name__exact = last_name)\
                                     .filter(birthday__exact = student['ngay_sinh'])
                if not find:
                    st = Pupil()
                    st.first_name = first_name
                    st.last_name = last_name
                    st.birthday = student['ngay_sinh']
                    st.school_join_date = today
                    st.ban_dk = student['nguyen_vong']
                    st.start_year_id = year
                    st.class_id = chosen_class
                    st.save()
                else:
                    find = find[0]
                    if  find.class_id != chosen_class:
                        find.class_id = chosen_class
                        find.save()
            message = u'Bạn vừa nhập thành công danh sách học sinh trúng tuyển.'
            student_list=[]
            request.session['student_list'] = student_list
        elif request.POST['clickedButton'] == 'add':
            print "button add has been clicked"
            
            diem = float(request.POST['diem_hs_trung_tuyen'])
            print "diem: ", diem
            ns = to_date(request.POST['ns_hs_trung_tuyen'])
            print "ngay sinh: ", ns
            element = { 'ten': request.POST['name_hs_trung_tuyen'],
                        'ngay_sinh': ns,
                        'nguyen_vong': request.POST['nv_hs_trung_tuyen'],
                        'tong_diem': diem,
                       }
            student_list.append(element)
            request.session['student_list'] = student_list
    context = RequestContext(request, {'student_list': student_list})
    return render_to_response(DANH_SACH_TRUNG_TUYEN, {'message':message}, context_instance = context)
#------------------------------------------------------------------------------------
def diem_danh(request, class_id, day, month, year):
    message = None
    listdh = None
    pupilList = Pupil.objects.filter(class_id = class_id)
    time = date(int(year),int(month),int(day))
    c = Class.objects.get(id__exact = class_id)
    term = Term.objects.filter(year_id = c.year_id).latest('id')
    form = []
    i = 0
    for p in pupilList:
        form.append(DiemDanhForm())
        try:
            dd = DiemDanh.objects.get(time__exact=time, student_id__exact = p.id, term_id__exact = term.id)
            form[i] = DiemDanhForm(instance = dd)
            i = i+1
        except ObjectDoesNotExist:
            i = i+1
    listdh = zip(pupilList,form)
    if request.method == 'POST':
        message = 'Cập nhật thành công danh sách điểm danh lớp ' + str(Class.objects.get(id = class_id)) +'. Ngày ' + str(time)
        list = request.POST.getlist('loai')
        i = 0
        for p in pupilList:
            try:
                dd = DiemDanh.objects.get(time__exact=time, student_id__exact = p.id, term_id__exact = term.id)
                if list[i] != 'k':
                    data = {'student_id':p.id,'time':time,'loai':list[i],'term_id':term.id}
                    form[i] = DiemDanhForm(data, instance = dd)
                    if form[i].is_valid():
                        form[i].save()
                else:
                    form[i] = DiemDanhForm()
                    dd.delete()
                i = i + 1
            except ObjectDoesNotExist:
                if list[i] != 'k':
                    data = {'student_id':p.id,'time':time,'loai':list[i],'term_id':term.id}
                    form[i] = DiemDanhForm(data)
                    if form[i].is_valid():
                        form[i].save()
                i = i + 1
    listdh = zip(pupilList,form)                
    t = loader.get_template('school/diem_danh.html')
    c = RequestContext(request, {'form':form, 'pupilList' : pupilList, 'time': time , 'message':message, 'class_id':class_id,'time':time,'list':listdh,
                                    'day':day, 'month':month, 'year':year})
    return HttpResponse(t.render(c))
    
def time_select(request, class_id):
    form = DateForm()
    message = 'Hãy chọn 1 ngày'
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            day = int(request.POST['day'])
            month = int(request.POST['month'])
            year = int(request.POST['year'])
            url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year) + '/'
            return HttpResponseRedirect(url)
    t = loader.get_template('school/time_select.html')
    c = RequestContext(request, {'form':form, 'class_id':class_id, 'message':message})
    return HttpResponse(t.render(c))
   
def diem_danh_hs(request, student_id):
    pupil = Pupil.objects.get(id = student_id)
    c = Class.objects.get(id__exact = pupil.class_id.id)
    term = Term.objects.filter(year_id = c.year_id).latest('id')
    ddl = DiemDanh.objects.filter(student_id = student_id, term_id = term.id)
    form = []
    iform = DiemDanhForm()
    for dd in ddl:
        form.append(DiemDanhForm(instance = dd))
    if request.method == 'POST':
        list = request.POST.getlist('loai')
        time = request.POST.getlist('time')
        i = 0
        for dd in ddl:
            if list[i] != 'k':
                data = {'student_id':student_id,'time':time[i],'loai':list[i],'term_id':term.id}
                form[i] = DiemDanhForm(data, instance = dd)
                if form[i].is_valid():
                    form[i].save()
                i = i + 1
            else:
                time.remove(time[i])
                form.remove(form[i])
                list.remove(list[i])
                dd.delete()
        if list[i] != 'k':
            data = {'student_id':student_id,'time':time[i],'loai':list[i],'term_id':term.id}
            iform = DiemDanhForm(data)
            if iform.is_valid():
                iform.save()
                form.append(iform)
                iform = DiemDanhForm
        
    t = loader.get_template('school/diem_danh_hs.html')
    c = RequestContext(request, {'form' : form,'iform' : iform,'pupil':pupil,'student_id':student_id})
    return HttpResponse(t.render(c))

def tk_diem_danh(student_id):
    pupil = Pupil.objects.get(id = student_id)
    c = Class.objects.get(id__exact = pupil.class_id.id)
    term = Term.objects.filter(year_id = c.year_id).latest('id')
    ts = DiemDanh.objects.filter(student_id = student_id).count()
    cp = DiemDanh.objects.filter(student_id = student_id, loai = u'C').count()
    kp = ts - cp
    tk = TKDiemDanh({'student_id':student_id,'tong_so':ts,'co_phep':cp,'khong_phep':kp,'term_id':term.id})
    tk.save()
    
def test(request, school_code = None):
    t = loader.get_template('school/test.html')
    
    c = RequestContext(request)

    return HttpResponse(t.render(c))

def deleteSubject(request, subject_id):
    message = "You have deleted succesfully"
    sub = Subject.objects.get(id = subject_id)
    class_id = sub.class_id
    sub.delete()
    subjectList = Subject.objects.filter(class_id = class_id)
    form = SubjectForm()
    t = loader.get_template('school/subject_per_class.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'subjectList' : subjectList, 'class_id' : class_id.id})
    return HttpResponse(t.render(c))

def deleteTeacher(request, teacher_id):
    message = "You have deleted succesfully"
    s = Teacher.objects.get(id = teacher_id)
    s.delete()
    teacherList = Teacher.objects.all()
    form = TeacherForm()
    t = loader.get_template('school/teachers.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'teacherList' : teacherList})
    return HttpResponse(t.render(c))

def deleteClass(request, class_id):
    message = "You have deleted succesfully"
    s = Class.objects.get(id = class_id)
    s.delete()
    classList = Class.objects.all()
    form = ClassForm()
    t = loader.get_template('school/classes.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'classList' : classList})
    return HttpResponse(t.render(c))

def deleteStudentInClass(request, student_id):
    message = "You have deleted succesfully"
    student = Pupil.objects.get(id = student_id)
    class_id = student.class_id
    student.delete()
    studentList = Pupil.objects.filter(class_id = class_id)
    form = PupilForm()
    t = loader.get_template('school/student_per_class.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'studentList' : studentList, 'class_id' : class_id.id})
    return HttpResponse(t.render(c))

def deleteStudentInSchool(request, student_id):
    message = "You have deleted succesfully"
    sub = Pupil.objects.filter(id = student_id)
    sub.delete()
    studentList = Pupil.objects.all()
    form = PupilForm()
    t = loader.get_template('school/students.html')
    c = RequestContext(request, {'form' : form, 'message' : message,  'studentList' : studentList})
    return HttpResponse(t.render(c))
