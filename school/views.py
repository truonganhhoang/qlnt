# -*- coding: utf-8 -*-

# Create your views here.
import os.path
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *
from django.db import transaction

from school.utils import *
from school.models import *
from school.school_settings import *
import xlrd

NHAP_DANH_SACH_TRUNG_TUYEN = os.path.join('school','import','nhap_danh_sach_trung_tuyen.html')
DANH_SACH_TRUNG_TUYEN = os.path.join('school','import','danh_sach_trung_tuyen.html')
START_YEAR = os.path.join('school','start_year.html')
NHAP_BANG_TAY = os.path.join('school','import','manual_adding.html')
TEMP_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'uploaded')
SCHOOL = os.path.join('school','school.html')
YEARS = os.path.join('school','years.html')

def school_index(request):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    if request.method == "POST":
        print request.POST['clickedButton']
        if request.POST['clickedButton'] == "start_year":
            return HttpResponseRedirect(reverse('start_year'))
        elif request.POST['clickedButton'] == "start_second_term":
            context = RequestContext(request, {'school':school})
            return render_to_response(r'school/start_second_term.html', context_instance = context)
        elif request.POST['clickedButton'] == "finish_year":
            context = RequestContext(request, {'school':school})
            return render_to_response(r'school/finish_year.html', context_instance = context)    
    context = RequestContext(request)
    return render_to_response(SCHOOL, context_instance = context)
@transaction.commit_manually    
def b1(request):
    # tao moi cac khoi neu truong moi thanh lap
    school = get_school(request)
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
        term.active = True
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
        transaction.commit()
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
            transaction.commit()
        else: # truong ko co nam cu
            pass
        # render HTML
    else: 
        #raise Exception(u'Start_year: đã bắt đầu năm học rồi ?')    
        pass
    transaction.commit()
    context = RequestContext(request, {'school':school})
    return render_to_response(START_YEAR, context_instance = context)     

def years(request):
    school = get_school(request)
    
    years = school.year_set.all()
    return render_to_response(YEARS, {'years':years}, context_instance = RequestContext(request))        
    
#-----------------------------------------------------------------------------------------------------------------                                       
def classes(request, sort_type = 1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    form = ClassForm()
    if int(sort_type)==1:
		if int(sort_status) == 0:
			classList = Class.objects.all().order_by('name')
		else:
			classList = Class.objects.all().order_by('-name')
    if int(sort_type) == 2:
		if int(sort_status) == 0:
			classList = Class.objects.all().order_by('block_id__number')
		else:
			classList = Class.objects.all().order_by('-block_id__number')
    if int(sort_type) == 3:
		if int(sort_status) == 0:
			classList = Class.objects.all().order_by('teacher_id__first_name')
		else:
			classList = Class.objects.all().order_by('-teacher_id__first_name')
    if int(sort_type)==4:
		if int(sort_status) == 0:
			classList = Class.objects.all().order_by('year_id__time')
		else:
			classList = Class.objects.all().order_by('-year_id__time')
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'You have added new class'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template(os.path.join('school','classes.html'))
    c = RequestContext(request, {'form' : form, 'message' : message, 'classList' : classList, 'sort_type':sort_type, 'sort_status':sort_status, 'next_status':1-int(sort_status)})
    return HttpResponse(t.render(c))

def viewClassDetail(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    class_view = Class.objects.get(id = class_id)
    t = loader.get_template(os.path.join('school','classDetail.html'))
    c = RequestContext(request, {'class_view' : class_view})
    return HttpResponse(t.render(c))

#sort_type = '1': fullname, '2': birthday, '3':'sex'
#sort_status = '0':ac '1':'dec

def teachers(request, sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    form = TeacherForm()
    school_id = get_school(request).id
    #print sort_type +' ' + sort_status
    if int(sort_type)==1:
		if int(sort_status) == 0:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('first_name', 'last_name')
		else:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('-first_name','-last_name')
    if int(sort_type) == 2:
		if int(sort_status) == 0:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('birthday')
		else:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('-birthday')
    if int(sort_type) == 3:
		if int(sort_status) == 0:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('sex')
		else:
			teacherList = Teacher.objects.filter(school_id = school_id).order_by('-sex')
    if request.method == 'POST':
        name = request.POST['first_name'].split()
        last_name = ' '.join(name[:len(name)-1])
        first_name = name[len(name)-1]
        birthday = date(int(request.POST['birthday_year']),int(request.POST['birthday_month']),int(request.POST['birthday_day']))
        data = {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'sex':request.POST['sex'], 'school_id':school_id, 'birth_place':request.POST['birth_place']}
        form = TeacherForm(data)
        if form.is_valid():
            form.save()
            message = 'You have added new teacher'
            form = TeacherForm()
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template(os.path.join('school','teachers.html'))
    c = RequestContext(request, {'form': form, 'message': message, 'teacherList': teacherList, 'sort_type':sort_type, 'sort_status':sort_status, 'next_status':1-int(sort_status)})
    return HttpResponse(t.render(c))

def viewTeacherDetail(request, teacher_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
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
    
    t = loader.get_template(os.path.join('school','teacher_detail.html'))
    c = RequestContext(request, {'form' : form, 'message' : message, 'id' : teacher_id})
    return HttpResponse(t.render(c))

def subjectPerClass(request, class_id, sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    if int(sort_type)==1:
		if int(sort_status) == 0:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('name')
		else:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('-name')
    if int(sort_type) == 2:
		if int(sort_status) == 0:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('hs')
		else:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('-hs')
    if int(sort_type) == 3:
		if int(sort_status) == 0:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('teacher_id__first_name')
		else:
			subjectList = Subject.objects.filter(class_id=class_id).order_by('-teacher_id__first_name')
    form = SubjectForm()
    if request.method == 'POST':
        data = {'name':request.POST['name'], 'hs':request.POST['hs'], 'class_id':class_id, 'teacher_id':request.POST['teacher_id']}
        form = SubjectForm(data)
        if form.is_valid():
            form.save()
            message = 'You have added new subject'
            form = SubjectFrom()
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template(os.path.join('school','subject_per_class.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'subjectList' : subjectList, 'class_id' : class_id, 'sort_type' : sort_type, 'sort_status':sort_status, 'next_status':1-int(sort_status)})
    return HttpResponse(t.render(c))

def studentPerClass(request, class_id, sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    form = PupilForm()
    if int(sort_type)==1:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name')
		else:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('-first_name','-last_name')
    if int(sort_type) == 2:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('birthday')
		else:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('-birthday')
    if int(sort_type) == 3:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('sex')
		else:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('-sex')
    if int(sort_type) == 4:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('ban_dk')
		else:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('-ban_dk')
    if int(sort_type) == 5:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('school_join_date')
		else:
			studentList = Pupil.objects.filter(class_id=class_id).order_by('-school_join_date')
			
    if request.method == 'POST':
        name = request.POST['first_name'].split()
        last_name = ' '.join(name[:len(name)-1])
        first_name = name[len(name)-1]
        birthday = date(int(request.POST['birthday_year']),int(request.POST['birthday_month']),int(request.POST['birthday_day']))
        school_join_date = date(int(request.POST['school_join_date_year']),int(request.POST['school_join_date_month']),int(request.POST['school_join_date_day']))
        data = {'first_name':first_name, 'last_name':last_name,'birthday':birthday, 'class_id':class_id, 'sex':request.POST['sex'], 'ban_dk':request.POST['ban_dk'], 'school_join_date':school_join_date, 'start_year_id':request.POST['start_year_id']}
        form = PupilForm(data)
        if form.is_valid():
            form.save()
            message = 'You have added new student'
            form = PupilForm()
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template(os.path.join('school','student_per_class.html'))
    c = RequestContext(request, {'form': form, 'message': message, 'studentList': studentList, 'class_id': class_id, 'sort_type':int(sort_type), 'sort_status':int(sort_status), 'next_status':1-int(sort_status)})
    return HttpResponse(t.render(c))

def students(request, sort_type=1, sort_status=1):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    school_id = get_school(request).id
    form = PupilForm()
    if int(sort_type)==1:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('first_name', 'last_name')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-first_name','-last_name')
    if int(sort_type) == 2:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('birthday')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-birthday')
    if int(sort_type) == 3:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('sex')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-sex')
    if int(sort_type) == 4:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('ban_dk')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-ban_dk')
    if int(sort_type) == 5:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('school_join_date')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-school_join_date')
	
    if int(sort_type) == 6:
		if int(sort_status) == 0:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('class_id__name')
		else:
			studentList = Pupil.objects.filter(school_id = school_id).order_by('-class_id__name')
			
    if request.method == 'POST':
		name = request.POST['first_name'].split()
		last_name = ' '.join(name[:len(name)-1])
		first_name = name[len(name)-1]
		birthday = date(int(request.POST['birthday_year']),int(request.POST['birthday_month']),int(request.POST['birthday_day']))
		school_join_date=date(int(request.POST['school_join_date_year']),int(request.POST['school_join_date_month']),int(request.POST['school_join_date_day']))
		data = {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'sex':request.POST['sex'],'ban_dk':request.POST['ban_dk'], 'school_join_date':school_join_date, 'start_year_id':request.POST['start_year_id'], 'class_id' : request.POST['class_id']}
		form = PupilForm(data)
		if form.is_valid():
			form.save()
			message = 'You have added new student'
			form = PupilForm()
		else:
			message = 'Please check your information, something is wrong'

    t = loader.get_template(os.path.join('school','students.html'))
    c = RequestContext(request, {'form': form, 'message': message, 'studentList': studentList, 'sort_type':sort_type, 'sort_status':sort_status, 'next_status':1-int(sort_status)})
    return HttpResponse(t.render(c))

def viewStudentDetail(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
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

    t = loader.get_template(os.path.join('school','student_detail.html'))
    c = RequestContext(request, {'form' : form, 'message' : message, 
                                 'id' : student_id,
                                 'class_id':pupil.class_id.id
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
        
class ManualAddingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        class_list = kwargs.pop('class_list')
        super(ManualAddingForm, self).__init__(*args, **kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Chọn lớp:', choices = class_list, required = False)
        
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
    school = get_school(request)
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

@transaction.commit_manually   
def manual_adding(request):
    school = get_school(request)
    _class_list = [(u'0',u'---')]
    message = None
    try:
        this_year = school.year_set.latest('time')
        term = this_year.term_set.get(number__exact = school.status)
        temp = this_year.class_set.all()
        for _class in temp:
            _class_list.append((_class.id, _class.name))
    except Exception as e:
        print e
        _class_list = None
    if request.method == 'POST':
        form = ManualAddingForm(request.POST, class_list = _class_list)
        student_list = request.session['student_list']
        if form.is_valid():
            chosen_class = form.cleaned_data['the_class']
            if chosen_class != u'0':
                chosen_class = school.year_set.latest('time').class_set.get(id = chosen_class)
            else:
                chosen_class = None
            if request.POST['clickedButton'] == 'save':
                year = school.startyear_set.get( time = datetime.date.today().year)
                today = datetime.date.today()   
                for student in student_list:
                    data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                        'ban':student['nguyen_vong'],}
                    
                    print "data", data
                    print "_class", _class
                    print "start_year", year
                    print "year", this_year
                    print "term", term
                    print "school", school
                    add_student( student = data, _class = chosen_class,
                             start_year = year, year = this_year,
                             term = term, school = school)
                    '''
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
                    '''
                transaction.commit()
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
    else:
        student_list = []
        request.session['student_list'] = student_list
        form = ManualAddingForm( class_list = _class_list)
    transaction.commit()
    context = RequestContext( request, {'student_list': student_list})    
    return render_to_response(NHAP_BANG_TAY, {'form':form}, context_instance = context)   

@transaction.commit_on_success    
def danh_sach_trung_tuyen(request):
    student_list = request.session['student_list']
    school = get_school(request)
    term = school.year_set.latest('time').term_set.latest('number')
    chosen_class = request.session['chosen_class']
    current_year = school.year_set.latest('time')
    if chosen_class != u'0':
        chosen_class = school.year_set.latest('time').class_set.get(id = chosen_class)
    else:
        chosen_class = None
    print "chosen_class: ", chosen_class
    message = None
   
    if request.method == 'POST':
        print ">>>", request.POST['clickedButton']
        if request.POST['clickedButton'] == 'save':
            print "button save has been clicked "
            year = school.startyear_set.get( time = datetime.date.today().year)
            today = datetime.date.today()   
            for student in student_list:
                data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                        'ban':student['nguyen_vong'],}
                
                add_student( student = data, _class = chosen_class,
                             start_year = year, year = current_year,
                             term = term, school = school)
                '''
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
                    
                    tbnam = TBNam()
                    tbnam.year_id = current_year
                    tbnam.student_id = st
                    tbnam.save()
                    
                    tbhk = TBHocKy()
                    tbhk.student_id = st
                    tbhk.term_id = term
                    tbhk.save()
                    
                    if chosen_class:
                        subject_list = chosen_class.subject_set.all()
                        for subject in subject_list:
                            mark = Mark()
                            mark.subject_id = subject
                            mark.student_id = st
                            mark.term_id = term
                            mark.save()
                            
                            tkmon = TKMon()
                            tkmon.subject_id = subject
                            tkmon.student_id = st
                            tkmon.thi_lai = False
                            tkmon.save()
                else:
                    find = find[0]
                    if  find.class_id != chosen_class:
                        if find.class_id.block_id.number == chosen_class.block_id.number:
                            marks = find.mark_set.all()
                            # disassociated 
                            for mark in marks:
                                mark.student_id = None
                                mark.save()    
                            #
                            # transfer mark
                                
                            #----------------
                            find.class_id = chosen_class
                            find.save()
                            
                            if chosen_class:
                                subject_list = chosen_class.subject_set.all()
                                for subject in subject_list:
                                    mark = Mark()
                                    mark.subject_id = subject
                                    mark.student_id = find
                                    mark.term_id = term
                                    mark.save()
                                    
                                    tkmon = TKMon()
                                    tkmon.subject_id = subject
                                    tkmon.student_id = find
                                    tkmon.thi_lai = False
                                    tkmon.save()
            '''        
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
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    listdh = None
    term = None
    pupilList = Pupil.objects.filter(class_id = class_id).order_by('first_name','last_name')
    time = date(int(year),int(month),int(day))
    c = Class.objects.get(id__exact = class_id)
    term = get_current_term(request)
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
    t = loader.get_template(os.path.join('school','diem_danh.html'))
    c = RequestContext(request, {'form':form, 'pupilList' : pupilList, 'time': time , 'message':message, 'class_id':class_id,'time':time,'list':listdh,
                                    'day':day, 'month':month, 'year':year})
    return HttpResponse(t.render(c))
    
def time_select(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = 'Hãy chọn 1 ngày'
    try:
        cl = Class.objects.get(id__exact = class_id)
        term = get_current_term(request)
    except ObjectDoesNotExist:
        message = None
    form = DateForm()
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            day = int(request.POST['date_day'])
            month = int(request.POST['date_month'])
            year = int(request.POST['date_year'])
            url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year) + '/'
            #url = os.path.join('','school','diemdanh', str(class_id), str(day), str(month), str(year),'')
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school','time_select.html'))
    c = RequestContext(request, {'form':form, 'class_id':class_id, 'message':message})
    return HttpResponse(t.render(c))
   
def diem_danh_hs(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    term = None
    pupil = Pupil.objects.get(id = student_id)
    c = pupil.class_id
    term = get_current_term(request)
    if term == None:
        message = None
        t = loader.get_template(os.path.join('school','time_select.html'))
        ct = RequestContext(request, {'class_id':c.id, 'message':message})
        return HttpResponse(t.render(ct))
    ddl = DiemDanh.objects.filter(student_id = student_id, term_id = term.id).order_by('time')
    form = []
    iform = DiemDanhForm()
    for dd in ddl:
        form.append(DiemDanhForm(instance = dd))
    if request.method == 'POST':
        list = request.POST.getlist('loai')
        time_day = request.POST.getlist('time_day')
        time_month = request.POST.getlist('time_month')
        time_year = request.POST.getlist('time_year')
        i = 0
        for dd in ddl:
            if list[i] != 'k':
                time = date(int(time_year[i]),int(time_month[i]),int(time_day[i]))
                data = {'student_id':student_id,'time':time,'loai':list[i],'term_id':term.id}
                form[i] = DiemDanhForm(data, instance = dd)
                if form[i].is_valid():
                    form[i].save()  
                    i = i + 1
            else:
                time_day.remove(time_day[i])
                time_month.remove(time_month[i])
                time_year.remove(time_year[i])
                form.remove(form[i])
                list.remove(list[i])
                dd.delete()
        if list[i] != 'k':
            time = date(int(time_year[i]),int(time_month[i]),int(time_day[i]))
            data = {'student_id':student_id,'time':time,'loai':list[i],'term_id':term.id}
            iform = DiemDanhForm(data)
            if iform.is_valid():
                iform.save()
                form.append(iform)
                iform = DiemDanhForm  
    t = loader.get_template(os.path.join('school','diem_danh_hs.html'))
    c = RequestContext(request, {'form' : form,'iform' : iform,'pupil':pupil,'student_id':student_id})
    return HttpResponse(t.render(c))
    
def tk_dd_lop(class_id,term_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    ppl = pupil.objects.filter(class_id = class_id)
    for p in ppl:
        tk_diem_danh(p.id,term_id)
    
def tk_diem_danh(student_id,term_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    pupil = Pupil.objects.get(id = student_id)
    c = pupil.class_id
    ts = DiemDanh.objects.filter(student_id = student_id, term_id = term.id).count()
    cp = DiemDanh.objects.filter(student_id = student_id, term_id = term.id, loai = u'C').count()
    kp = ts - cp
    data = {'student_id':student_id, 'tong_so':ts, 'co_phep':cp, 'khong_phep':kp, 'term_id':term.id}
    tk = TKDiemDanhForm()
    try:
        tkdd = TKDiemDanh.objects.get(student_id__exact = student_id, term_id__exact = term.id)
        tk = TKDiemDanhForm(data, instace = tkdd)
    except ObjectDoesNotExist:
        tk = TKDiemDanhForm(data)
    tk.save()
    
def test(request):
    form = PupilForm()
    message = 'Hello'
    t = loader.get_template('school/time_select.html')
    c = RequestContext(request, {'form':form,'message':message})

    return HttpResponse(t.render(c))

def deleteSubject(request, subject_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = "You have deleted succesfully"
    sub = Subject.objects.get(id = subject_id)
    class_id = sub.class_id
    sub.delete()
    subjectList = Subject.objects.filter(class_id = class_id)
    form = SubjectForm()
    t = loader.get_template(os.path.join('school','subject_per_class.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'subjectList' : subjectList, 'class_id' : class_id.id})
    return HttpResponse(t.render(c))

def deleteTeacher(request, teacher_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = "You have deleted succesfully"
    s = Teacher.objects.get(id = teacher_id)
    s.delete()
    teacherList = Teacher.objects.all()
    form = TeacherForm()
    t = loader.get_template(os.path.join('school','teachers.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'teacherList' : teacherList})
    return HttpResponse(t.render(c))

def deleteClass(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = "You have deleted succesfully"
    s = Class.objects.get(id = class_id)
    s.delete()
    classList = Class.objects.all()
    form = ClassForm()
    t = loader.get_template(os.path.join('school','classes.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'classList' : classList})
    return HttpResponse(t.render(c))

def deleteStudentInClass(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = "You have deleted succesfully"
    student = Pupil.objects.get(id = student_id)
    class_id = student.class_id
    student.delete()
    studentList = Pupil.objects.filter(class_id = class_id)
    form = PupilForm()
    t = loader.get_template(os.path.join('school','student_per_class.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'studentList' : studentList, 'class_id' : class_id.id})
    return HttpResponse(t.render(c))

def deleteStudentInSchool(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = "You have deleted succesfully"
    sub = Pupil.objects.filter(id = student_id)
    sub.delete()
    studentList = Pupil.objects.all()
    form = PupilForm()
    t = loader.get_template(os.path.join('school','students.html'))
    c = RequestContext(request, {'form' : form, 'message' : message,  'studentList' : studentList})
    return HttpResponse(t.render(c))

def khen_thuong(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = ''
    ktl = KhenThuong.objects.filter(student_id = student_id).order_by('time')
    t = loader.get_template(os.path.join('school','khen_thuong.html'))
    c = RequestContext(request, {'ktl': ktl,'message':message, 'student_id':student_id})
    return HttpResponse(t.render(c))
    
def add_khen_thuong(request,student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    form = KhenThuongForm()
    pupil = Pupil.objects.get(id = student_id)
    cl = Class.objects.get(id__exact = pupil.class_id.id)
    term = Term.objects.filter(year_id = cl.year_id, active = True).latest('number')
    if request.method == 'POST':
        form = KhenThuongForm(request.POST)
        if form.is_valid():
            form.save()
            url = '/school/khenthuong/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school','khen_thuong_detail.html'))
    c = RequestContext(request, {'form' : form, 'p' : pupil, 'student_id':student_id,'term':term})
    return HttpResponse(t.render(c))

def delete_khen_thuong(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    kt = KhenThuong.objects.get(id = kt_id)
    student = Pupil.objects.get(id = kt.student_id.id)
    kt.delete()
    url = '/school/khenthuong/' + str(student.id)
    return HttpResponseRedirect(url)
    
def edit_khen_thuong(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    kt = KhenThuong.objects.get(id = kt_id)
    pupil = kt.student_id
    term = kt.term_id
    form = KhenThuongForm(instance = kt)
    if request.method == 'POST':
        form = KhenThuongForm(request.POST, instance = kt)
        if form.is_valid():
            form.save()
            url = '/school/khenthuong/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school','khen_thuong_detail.html'))
    c = RequestContext(request, {'form' : form, 'p' : pupil, 'student_id':pupil.id,'term':term})
    return HttpResponse(t.render(c))
    
def ki_luat(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = ''
    ktl = KiLuat.objects.filter(student_id = student_id).order_by('time')
    t = loader.get_template(os.path.join('school','ki_luat.html'))
    c = RequestContext(request, {'ktl': ktl,'message':message, 'student_id':student_id})
    return HttpResponse(t.render(c))
    
def add_ki_luat(request,student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    form = KiLuatForm()
    pupil = Pupil.objects.get(id = student_id)
    cl = Class.objects.get(id__exact = pupil.class_id.id)
    term = Term.objects.filter(year_id = cl.year_id, active = True).latest('number')
    if request.method == 'POST':
        form = KiLuatForm(request.POST)
        if form.is_valid():
            form.save()
            url = '/school/khenthuong/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school','ki_luat_detail.html'))
    c = RequestContext(request, {'form' : form, 'p' : pupil, 'student_id':student_id,'term':term})
    return HttpResponse(t.render(c))

def delete_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    kt = KiLuat.objects.get(id = kt_id)
    student = Pupil.objects.get(id = kt.student_id.id)
    kt.delete()
    url = '/school/khenthuong/' + str(student.id)
    return HttpResponseRedirect(url)

def edit_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    kt = KiLuat.objects.get(id = kt_id)
    pupil = kt.student_id
    term = kt.term_id
    form = KiLuatForm(instance = kt)
    if request.method == 'POST':
        form = KiLuatForm(request.POST, instance = kt)
        if form.is_valid():
            form.save()
            url = '/school/khenthuong/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school','ki_luat_detail.html'))
    c = RequestContext(request, {'form' : form, 'p' : pupil, 'student_id':pupil.id,'term':term})
    return HttpResponse(t.render(c))    

def hanh_kiem(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect( reverse('login'))
    message = None
    listdh = None
    term = None
    pupilList = Pupil.objects.filter(class_id = class_id)
    c = Class.objects.get(id__exact = class_id)
    term = Term.objects.filter(year_id = c.year_id,active = True).latest('number')
    form = []
    i = 0
    for p in pupilList:
        form.append(HanhKiemForm())
        try:
			hk= HanhKiem.objects.get(student_id__exact = p.id, term_id__exact = term.id)
			form[i] = HanhKiemForm(instance = hk)
        except ObjectDoesNotExist:
			data={'student_id':p.id,'term_id':term.id}
			form[i] = HanhKiemForm(data)
        i=i+1
    listdh = zip(pupilList,form)
    if request.method == 'POST':
        message = 'Cập nhật thành công hạnh kiểm lớp ' + str(Class.objects.get(id = class_id))
        list = request.POST.getlist('loai')
        i = 0
        for p in pupilList:
			try:
				hk= HanhKiem.objects.get(student_id__exact = p.id, term_id__exact = term.id)
				data = {'student_id':p.id,'loai':list[i],'term_id':term.id}
				form[i] = HanhKiemForm(data, instance = hk)
				form[i].save()
			except ObjectDoesNotExist:
				data = {'student_id':p.id,'loai':list[i],'term_id':term.id}
				form[i] = HanhKiemForm(data)
				form[i].save()
			i=i+1
			
    listdh = zip(pupilList,form)                
    t = loader.get_template(os.path.join('school','hanh_kiem.html'))
    c = RequestContext(request, {'form':form, 'pupilList' : pupilList, 'message':message, 'class_id':class_id,'list':listdh})
    return HttpResponse(t.render(c))
