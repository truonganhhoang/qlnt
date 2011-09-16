# -*- coding: utf-8 -*-

# Create your views here.
import os.path
import datetime
from django.core.paginator import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *
from django.middleware.csrf import get_token
from django.db import transaction
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError
from school.utils import *
from school.models import *
from django.contrib.auth.forms import *
from school.forms import *
from school.school_settings import *
from sms.views import *
import xlrd
from xlrd import cellname
from xlwt import Workbook, XFStyle, Borders, Font

NHAP_DANH_SACH_TRUNG_TUYEN = os.path.join('school', 'import', 'nhap_danh_sach_trung_tuyen.html')
DANH_SACH_TRUNG_TUYEN = os.path.join('school', 'import', 'danh_sach_trung_tuyen.html')
START_YEAR = os.path.join('school', 'start_year.html')
NHAP_BANG_TAY = os.path.join('school', 'import', 'manual_adding.html')
SCHOOL = os.path.join('school', 'school.html')
YEARS = os.path.join('school', 'years.html')
CLASS_LABEL = os.path.join('school', 'class_labels.html')
CLASSIFY = os.path.join('school','classify.html')
INFO = os.path.join('school','info.html')
SETUP = os.path.join('school','setup.html')
ORGANIZE_STUDENTS = os.path.join('school','organize_students.html')
STUDENT = os.path.join('school','classDetail_one_student.html')
def school_index(request):

    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if not school.status:
        return HttpResponseRedirect(reverse('setup'))
    try:
        year = get_current_year(request)
    except Exception as e:
        print e
        return HttpResponseRedirect(reverse('setup'))

    user_type = get_permission(request)
    if user_type in ['HIEU_TRUONG', 'HIEU_PHO']:
        grades = school.block_set.all()
        classes = year.class_set.all()
        context = RequestContext(request)
        return render_to_response(SCHOOL,{'classes': classes,
                                          'grades': grades}, context_instance=context)
    elif user_type == 'GIAO_VIEN':
        teaching_subjects = Subject.objects.filter(teacher_id = user.teacher)
        teaching_class = user.teacher.teaching_class()
        term = get_current_term(request)
        context = RequestContext(request)

        return render_to_response(SCHOOL,{'teaching_subjects': teaching_subjects,
                                          'term': term, 'teaching_class': teaching_class},
                                  context_instance=context)
    elif user_type  == 'HOC_SINH':
        return HttpResponseRedirect(reverse('student_detail', args=[user.pupil.id]))
def is_safe(school):
    if school.danhsachloailop_set.all(): return True
    else: return False

def setup(request):
    user = request.user
    message = None
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect( reverse('index'))
    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))


    if request.is_ajax():
        if request.method == 'POST':
            if 'update_school_detail' in request.POST:
                school_form = SchoolForm(request.POST, request = request)
                if school_form.is_valid():
                    school_form.save_to_model()
                    message = u'Bạn vừa cập nhật thông tin trường học thành công.\
                    Hãy cung cấp danh sách tên lớp học theo dạng [khối] [tên lớp]. Ví dụ: 10 A'

                data = simplejson.dumps( {'message': message, 'status':'done'})
            elif 'update_class_name' in request.POST:
                message, labels, success = parse_class_label(request, school)

                classes_ = None
                grades = None
                if success:
                    classes_ = school.get_setting('classes')
                    classes_ = '-'.join(classes_)
                    lower_bound = get_lower_bound(school)
                    upper_bound = get_upper_bound(school)
                    grades = '-'.join([str(grade) for grade in range(lower_bound, upper_bound)])

                data = simplejson.dumps( {'message': message, 'status': success,
                                          'classes': classes_, 'grades': grades})

            elif 'start_year' in request.POST:
                if is_safe(school):

                    data = simplejson.dumps({'status':'done'})
                else:
                    data = simplejson.dumps( {'message': message,'status': 'failed'} )
            return HttpResponse(data, mimetype = 'json')
        else:
            raise Exception('StrangeRequestMethod')

    form_data = {'name': school.name, 'school_level':school.school_level,
                 'address': school.address, 'phone': school.phone,
                 'email': school.email}
    school_form = SchoolForm(form_data, request= request)
    message, labels, success = parse_class_label(request, school)

    if request.method == 'POST':
        school_form = SchoolForm(request.POST, request = request)
        if school_form.is_valid():
            school_form.save_to_model()
            message = u'Bạn vừa cập nhật thông tin trường học thành công. '

        if 'start_year' in request.POST and is_safe(school):
            HttpResponseRedirect( reverse('start_year'))

    context = RequestContext(request)
    return render_to_response( SETUP, { 'form': school_form, 'message':message, 'labels':labels},
                               context_instance = context )

def info(request):
    user = request.user
    message = None
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect( reverse('index'))
    if request.method == 'POST':
        data = request.POST.copy()
        data['phone'] = data['phone'].strip()
        data['email'] = data['email'].strip()
        data['name'] = data['name'].strip()
        name=''
        address=''
        email=''
        phone=''
        if request.is_ajax():
            form = SchoolForm(data, request = request)
            if form.is_valid():
                form.save_to_model()
                message = u'Bạn vừa cập nhật thông tin trường học thành công'
                status = 'done'
            else:
                message = u'Có lỗi ở thông tin nhập vào'
                for a in form:
                    if a.name == 'phone':
                        if a.errors:
                            phone = str(a.errors)
                    elif a.name == 'email':
                        if a.errors:
                            email = str(a.errors)
                    elif a.name == 'address':
                        if a.errors:
                            address = str(a.errors)
                    elif a.name == 'name':
                        if a.errors:
                            name = str(a.errors)
                status = 'error'
            response = simplejson.dumps({'message': message, 'status': status, 'phone':phone, 'email':email, 'name':name, 'address':address})
            return HttpResponse(response, mimetype = 'json')

        form = SchoolForm(data, request = request)
        if form.is_valid():
            form.save_to_model()
            message = u'Bạn vừa cập nhật thông tin trường học thành công.'
            return HttpResponseRedirect( reverse('info'))
    else:
        data = {'name': school.name, 'school_level':school.school_level,
                'address': school.address, 'phone': school.phone,
                'email': school.email}
        form = SchoolForm(data, request= request)

    context = RequestContext(request)
    return render_to_response(INFO, { 'form':form, 'school':school, 'message':message}, context_instance = context)

def empty(label_list):
    for l in label_list:
        if l.strip(): return False
    return True


# this following view handles all ajax request of indexing targets.
@transaction.commit_manually
def change_index(request, target, class_id):
    object = None
    if target == u'subject': object = 'Subject'
    elif target == u'student': object = 'Pupil'
    elif target == u'teacher': object = 'Teacher'
    elif target == u'class': object = 'Class'
    else:
        raise Exception('BadTarget')
    if request.is_ajax():
        if request.method == 'POST':
            data = request.POST['data']
            try:
                list = data.split('/')
                for element in list:
                    if element:
                        id = int(element.split('_')[0])
                        index = int(element.split('_')[1])
                        exec('item = ' + object + '.objects.get(id = id)')
                        #subject = Subject.objects.get(id = id)
                        if item.index != index:
                            item.index = index
                            item.save()
                transaction.commit()
                response = simplejson.dumps({'success': True})
                return HttpResponse( response, mimetype='json')
            except Exception as e:
                print e
    else:
        raise Exception('NotAjaxRequest')

def organize_students(request, class_id, type = '0'):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    student_list = None
    _class = None
    try:
        _class = Class.objects.get( id = int(class_id))
        if type=='1':
            student_list = _class.pupil_set.order_by('first_name', 'last_name')
        else:
            student_list = _class.pupil_set.order_by('index')
    except Exception as e:
        print e

    context = RequestContext(request)
    return render_to_response(ORGANIZE_STUDENTS, {'student_list': student_list, 'class': _class},
                              context_instance = context)




def parse_class_label(request, school):
    message = None
    if 'message' in request.session:
        message = request.session['message']

    labels = ','.join(school.get_setting('classes'))
    success = None
    if request.method == 'POST':
        labels = request.POST['labels']
        if u'Nhanh:' in labels or u'nhanh:' in labels:
            try:
                labels = labels.split(':')[1]
                labels = labels.strip()
            except Exception as e:
                message = u'Bạn cần nhập ít nhất một tên lớp.'
                success = False

            if ',' in labels:
                list_labels = labels.split(',')
            else:
                list_labels = labels.split(' ')

            if empty(list_labels):
                message = u'Bạn cần nhập ít nhất một tên lớp.'
                success = False
            else:
                ds = school.danhsachloailop_set.all()
                for d in ds:
                    d.delete()
                labels_to_save = []
                for label in list_labels:
                    if label:
                        label = label.strip()
                        lb = school.danhsachloailop_set.filter( loai__exact = label )
                        if not lb:
                            lb = DanhSachLoaiLop()
                            lb.loai = label
                            lb.school_id = school
                            lb.save()
                        for i in range(get_lower_bound(school), get_upper_bound(school)):
                            labels_to_save.append("%s %s" % (i, lb.loai))

                school.save_settings('classes', str(labels_to_save))
                message = u'Bạn vừa thiết lập thành công danh sách tên lớp cho trường.'
                success = True
            labels = 'Nhanh: '+ labels
        else:
            if ',' in labels:
                list_labels = labels.split(',')
                # draft version
                if not list_labels:
                    message = u'Bạn cần nhập ít nhất một tên lớp'
                    success = False
                else:
                    ds = school.danhsachloailop_set.all()
                    labels_to_save= []
                    for d in ds:
                        d.delete()
                    for label in list_labels:
                        label = label.strip()
                        if label:
                            try:
                                class_type = label.split(' ')[1]
                                lb = school.danhsachloailop_set.filter( loai__exact = class_type )
                                if not lb:
                                    lb = DanhSachLoaiLop()
                                    lb.loai = class_type
                                    lb.school_id = school
                                    lb.save()
                                labels_to_save.append(label)
                            except Exception as e:
                                message = u'Các tên lớp phải được cung cấp theo dạng [khối][dấu cách][tên lớp]. Ví dụ: 10 A'
                                success = False
                                return message, labels, success
                    school.save_settings('classes', str(labels_to_save))
                    message = u'Bạn vừa thiết lập thành công danh sách tên lớp cho trường.'
                    success = True

                    #--------------

    return message, labels, success

@transaction.commit_on_success
def class_label(request):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))


    #------ user filtering
    message, labels, success = parse_class_label(request, school)

    context = RequestContext(request)
    t = loader.get_template(CLASS_LABEL)
    c = RequestContext(request, {'labels': labels, 'message': message}, )
    return HttpResponse(t.render(c))

@transaction.commit_on_success
def b1(request):
    # tao moi cac khoi neu truong moi thanh lap
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    message = None
    if not school.danhsachloailop_set.all():
        message = u'Bạn chưa thiết lập danh sách tên lớp học cho nhà trường. Hãy điền vào ô dưới \
                    danh sách tên lớp học cho nhà trường rồi ấn nút Lưu lại'
        request.session['message'] = message
        transaction.commit()
        return HttpResponseRedirect( reverse('class_label'))
    if school.school_level == u'1':
        lower_bound = 1
        upper_bound = 5
        ds_mon_hoc = CAP1_DS_MON
    elif school.school_level == u'2':
        lower_bound = 6
        upper_bound = 9
        ds_mon_hoc = CAP2_DS_MON
    elif school.school_level == u'3':
        lower_bound = 10
        upper_bound = 12
        ds_mon_hoc = CAP3_DS_MON
    else:
        raise Exception('SchoolLevelInvalid')

    if not school.status:
        for khoi in range(lower_bound, upper_bound+1):
            if not school.block_set.filter(number = khoi):
                block = Block()
                block.number = khoi
                block.school_id = school
                block.save()
        school.status = 1
        school.save()
        # tao nam hoc moi
    current_year = datetime.datetime.now().year
    year = school.year_set.filter(time__exact=current_year)
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
        term = Term()
        term.active = False
        term.number = 2
        term.year_id = year
        term.save()
        term = Term()
        term.active = False
        term.number = 3
        term.year_id = year
        term.save()
        # create new class.
        # -- tao cac lop ---

        loai_lop = school.get_setting('classes')
        for class_name in loai_lop:
            _class = Class()
            _class.name = class_name
            _class.status = 1
            _class.block_id = school.block_set.get( number = int(class_name.split(' ')[0]))
            _class.year_id = year
            _class.save()
            i =0
            for mon in ds_mon_hoc:
                i+=1
                add_subject(subject_name= mon, subject_type= mon, _class=_class, index=i)
            # -- day cac hoc sinh len lop
        last_year = school.year_set.filter(time__exact=current_year -1)
        if last_year:
            blocks = school.block_set.all()
            for block in blocks:
                if block.number == upper_bound:
                    classes = block.class_set.all()
                    for _class in classes:
                        students = _class.pupil_set.all()
                        for student in students:
                            if student.tbnam_set.get(year_id=last_year).len_lop:
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
                            if student.tbnam_set.get(year_id=last_year).len_lop:
                                new_block = school.block_set.get(number=block.number + 1)
                                new_class_name = str(new_block.number) + ' ' + student.class_id.name.split()[1]
                                new_class = new_block.class_set.get(name=new_class_name)
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
    return HttpResponseRedirect(reverse("classes"))

def years(request):
    school = get_school(request)
    years = school.year_set.all()
    return render_to_response(YEARS, {'years':years}, context_instance=RequestContext(request))

@transaction.commit_on_success
def classify(request):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect( reverse("index"))
    try:
        startyear = get_latest_startyear(request)
        year = get_current_year(request)
    except Exception as e:
        print e
        return HttpResponseRedirect( reverse("school_index"))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))


    message = None
    nothing = False
    student_list = startyear.pupil_set.filter( class_id__exact = None).order_by('first_name')
    lower_bound = get_lower_bound(school)
    grade = school.block_set.filter( number__exact = lower_bound)
    _class_list = [(u'-1', u'Chọn lớp')]
    class_list = year.class_set.filter( block_id__exact = grade)
    for _class in class_list:
        _class_list.append((_class.id, _class.name))
    if request.method == "GET":
        if not student_list:
            message = u'Không còn học sinh nào cần được phân lớp.'
            nothing = True
    else:
        form = ClassifyForm( request.POST, student_list = student_list, class_list = _class_list)
        if form.is_valid():
            count =0
            for student in student_list:
                _class = form.cleaned_data[str(student.id)]
                if _class == u'-1':
                    _class = None
                    student.class_id = _class
                    student.save()

                else:
                    _class = year.class_set.get( id = int(_class))
                    move_student(school, student, _class)
                    count +=1
            message = u'Bạn vừa phân lớp thành công cho ' + str(count) + u' học sinh.'
        else:
            message = u'Xảy ra trục trặc trong quá trình nhập dữ liệu.'
        student_list = startyear.pupil_set.filter( class_id__exact = None).order_by('first_name')
    form = ClassifyForm( student_list = student_list, class_list= _class_list)
    return render_to_response( CLASSIFY, { 'message':message, 'student_list':student_list, 'form':form, 'nothing':nothing},
                               context_instance = RequestContext(request))

#----------------------------------------------------------------------------------------------------------------- 
#----------- Exporting from Excel -------------------------------------

def class_generate(request, class_id, object):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect( reverse("index"))
    try:
        startyear = get_latest_startyear(request)
        year = get_current_year(request)
    except Exception as e:
        print e
        return HttpResponseRedirect( reverse("school_index"))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    try:
        _class = Class.objects.get(id = class_id)
    except Exception as e:
        print e
        return HttpResponse()
    if object == 'student_list':
        file_name = request.session.session_key + unicode(_class) + '_student_list.xls'
        file_name = os.path.join(settings.TEMP_FILE_LOCATION, file_name)
        student_list = _class.pupil_set.all().order_by('index')
        book = Workbook(encoding = 'utf-8')
        #renderring xls file

        fnt = Font()
        fnt.name = 'Arial'
        fnt.height = 240

        fnt_bold = Font()
        fnt_bold.name = 'Arial'
        fnt_bold.height = 240
        fnt_bold.bold = True

        borders = Borders()
        borders.left = Borders.THIN
        borders.right = Borders.THIN
        borders.top = Borders.THIN
        borders.bottom = Borders.THIN
        borders.left_colour = 0x17
        borders.right_colour = 0x17
        borders.top_colour = 0x17
        borders.bottom_colour = 0x17


        style = XFStyle()
        style.font = fnt
        style.borders = borders

        style_bold = XFStyle()
        style_bold.font = fnt_bold
        style_bold.borders = borders

        sheet = book.add_sheet('Danh sách học sinh')
        sheet.write(0,0,u'Danh sách học sinh lớp %s' % unicode(_class), style_bold)
        sheet.row(0).height = 350


        sheet.col(0).width = 1500
        sheet.col(1).width = 7000
        sheet.col(2).width = 4500
        sheet.col(3).width = 7000
        sheet.col(4).width = 3000
        sheet.col(5).width = 4000
        sheet.col(6).width = 7000
        sheet.col(7).width = 4500
        sheet.col(8).width = 7000
        sheet.row(4).height = 350

        sheet.write(4,0,'STT', style_bold)
        sheet.write(4,1,'Họ và Tên', style_bold)
        sheet.write(4,2,'Ngày sinh', style_bold)
        sheet.write(4,3,'Nơi sinh', style_bold)
        sheet.write(4,4,'Giới tính', style_bold)
        sheet.write(4,5,'Dân tộc', style_bold)
        sheet.write(4,6,'Chỗ ở hiện tại', style_bold)
        sheet.write(4,7,'Số điện thoại', style_bold)
        sheet.write(4,8,'Ghi chú', style_bold)
        row = 5
        for student in student_list:
            sheet.row(row).height = 350
            sheet.write(row, 0, row -4, style)
            sheet.write(row, 1, student.last_name + ' '+student.first_name, style)
            sheet.write(row, 2, student.birthday.strftime('%d/%m/%Y'), style)
            sheet.write(row, 3, student.birth_place, style)
            sheet.write(row, 4, student.sex, style)
            sheet.write(row, 5, student.dan_toc, style)
            sheet.write(row, 6, student.current_address, style)
            sheet.write(row, 7, student.phone, style)
            sheet.write(row, 8, '', style)
            row +=1
            #return HttpResponse
        response = HttpResponse(mimetype='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=ds_hoc_sinh_%s.xls' % unicode(_class)
        book.save(response)
        return response
    else:
        raise Http404( "Page does not exist!" )

def teacher_generate(request, type):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect( reverse("index"))
    try:
        startyear = get_latest_startyear(request)
        year = get_current_year(request)
    except Exception as e:
        print e
        return HttpResponseRedirect( reverse("school_index"))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    if type == 'all':
        file_name = request.session.session_key + unicode(school) + '_teacher_list.xls'
        file_name = os.path.join(settings.TEMP_FILE_LOCATION, file_name)
        teacher_list = school.teacher_set.all().order_by('first_name', 'last_name','birthday')
        book = Workbook(encoding = 'utf-8')
        #renderring xls file

        fnt = Font()
        fnt.name = 'Arial'
        fnt.height = 240

        fnt_bold = Font()
        fnt_bold.name = 'Arial'
        fnt_bold.height = 240
        fnt_bold.bold = True

        borders = Borders()
        borders.left = Borders.THIN
        borders.right = Borders.THIN
        borders.top = Borders.THIN
        borders.bottom = Borders.THIN
        borders.left_colour = 0x17
        borders.right_colour = 0x17
        borders.top_colour = 0x17
        borders.bottom_colour = 0x17


        style = XFStyle()
        style.font = fnt
        style.borders = borders

        style_bold = XFStyle()
        style_bold.font = fnt_bold
        style_bold.borders = borders

        sheet = book.add_sheet('Danh sách giáo viên')
        sheet.write(0,0,u'Danh sách giáo viên  %s' % unicode(school), style_bold)
        sheet.row(0).height = 350


        sheet.col(0).width = 1500
        sheet.col(1).width = 7000
        sheet.col(2).width = 4500
        sheet.col(3).width = 7000
        sheet.col(4).width = 3000
        sheet.col(5).width = 4000
        sheet.col(6).width = 7000
        sheet.row(4).height = 350

        sheet.write(4,0,'STT', style_bold)
        sheet.write(4,1,'Họ và Tên', style_bold)
        sheet.write(4,2,'Ngày sinh', style_bold)
        sheet.write(4,3,'Quê quán', style_bold)
        sheet.write(4,4,'Giới tính', style_bold)
        sheet.write(4,5,'Dạy môn', style_bold)
        sheet.write(4,6,'Tổ', style_bold)

        row = 5
        for teacher in teacher_list:
            sheet.row(row).height = 350
            sheet.write(row, 0, row -4, style)
            sheet.write(row, 1, teacher.last_name + ' '+teacher.first_name, style)
            sheet.write(row, 2, teacher.birthday.strftime('%d/%m/%Y'), style)
            sheet.write(row, 3, teacher.home_town, style)
            sheet.write(row, 4, teacher.sex, style)
            if teacher.major and teacher.major!= '-1':
                sheet.write(row, 5, teacher.get_major_display(), style)
            else:
                sheet.write(row, 5, '', style)
            if teacher.team_id:
                sheet.write(row, 6, teacher.team_id.name, style)
            else:
                sheet.write(row, 6, '', style)
            row +=1
            #return HttpResponse
        response = HttpResponse(mimetype='application/ms-excel')
        response['Content-Disposition'] = u'attachment; filename=ds_giao_vien.xls'
        book.save(response)
        return response
    else:
        raise Http404( "Page does not exist!" )
#----------- Importing form Excel -------------------------------------

def save_file(import_file, session):
    import_file_name = import_file.name
    session_key = session.session_key
    save_file_name = session_key + import_file_name
    saved_file = open(os.path.join(TEMP_FILE_LOCATION, save_file_name), 'wb+')
    for chunk in import_file.chunks():
        saved_file.write(chunk)
    saved_file.close()
    return save_file_name

def process_file(file_name, task):
    message = u'<ul>'
    if task == "import_student":
        student_list = []
        filepath = os.path.join(TEMP_FILE_LOCATION, file_name)
        if not os.path.isfile(filepath):
            raise NameError, "%s is not a valid filename" % file_name
        try:
            book = xlrd.open_workbook(filepath)
            sheet = book.sheet_by_index(0)
        except Exception as e:
            print e
            return {'error': u'File tải lên không phải file Excel'}

        start_row = -1
        for c in range(0, sheet.ncols):
            flag = False
            for r in range(0, sheet.nrows):
                if sheet.cell_value(r, c) == u'Họ và Tên':
                    start_row = r
                    flag = True
                    break
            if flag: break
            #                                                             CHUA BIEN LUAN TRUONG HOP: start_row = -1, ko co cot ten: Mã học sinh
        if start_row == -1:
            return {'error': u'File tải lên phải có cột "Họ và Tên".'}, u'File tải lên phải có cột "Họ và Tên".', 0, 0
            # start_row != 0
        c_ten = -1
        c_ngay_sinh = -1
        c_gioi_tinh = -1
        c_noi_sinh = -1
        c_dan_toc = -1
        c_cho_o_ht = -1
        c_ten_bo = -1
        c_ten_me = -1
        c_so_dt_bo = -1
        c_so_dt_me = -1
        c_nguyen_vong = -1
        c_so_dt_nt = -1
        number = 0
        number_ok = 0
        for c in range(0, sheet.ncols):
            value = sheet.cell_value(start_row, c)

            if value == u'Họ và Tên':
                c_ten = c
            elif value == u'Ngày sinh':
                c_ngay_sinh = c
            elif value == u'Giới tính':
                c_gioi_tinh = c
            elif value == u'Nơi sinh':
                c_noi_sinh = c
            elif value == u'Dân tộc':
                c_dan_toc = c
            elif value == u'Chỗ ở hiện tại':
                c_cho_o_ht = c
            elif value == u'Họ tên bố':
                c_ten_bo = c
            elif value == u'Số điện thoại của bố':
                c_so_dt_bo = c
            elif value == u'Họ tên mẹ':
                c_ten_me = c
            elif value == u'Số điện thoại của mẹ':
                c_so_dt_me = c
            elif value == u'Ban đăng ký':
                c_nguyen_vong = c
            elif value == u'Số nhắn tin' or value == u'Số điện thoại nhắn tin':
                c_so_dt_nt = c


        for r in range(start_row + 1, sheet.nrows):
            name = ''
            birthday =''
            gt='Nam'
            dan_toc=u'Kinh'
            noi_sinh=''
            cho_o_ht=''
            ten_bo=''
            dt_bo=''
            ten_me=''
            dt_me=''
            ban_dk = u'CB'
            sms_phone = ''
            name = sheet.cell(r, c_ten).value.strip()
            name = ' '.join([i.capitalize() for i in name.split(' ')])
            if not name.strip():
                message += u'<li>Ô ' + unicode(cellname(r, c_ten)) + u':Trống. </li>'
                continue
            number += 1
            birthday = sheet.cell(r, c_ngay_sinh).value
            if not birthday:
                message += u'<li>Ô ' + unicode(cellname(r, c_ngay_sinh)) + u':Trống. Học sinh: ' + name + u' không đủ thông tin.</li>'
                continue
            if c_gioi_tinh>-1:
                gt = sheet.cell(r, c_gioi_tinh).value.strip().capitalize()
                if not gt: gt = 'Nam'
            if c_noi_sinh>-1:
                noi_sinh = sheet.cell(r, c_noi_sinh).value.strip()
            if c_dan_toc>-1:
                dan_toc = sheet.cell(r, c_dan_toc).value.strip()
                if not dan_toc.strip(): dan_toc = 'Kinh'
            if c_cho_o_ht>-1:
                cho_o_ht = sheet.cell(r, c_cho_o_ht).value.strip()
            if c_ten_bo>-1:
                ten_bo = sheet.cell(r, c_ten_bo).value.strip().capitalize()
            if c_so_dt_bo>-1:
                dt_bo = sheet.cell(r, c_so_dt_bo).value.strip()
            if c_ten_me>-1:
                ten_me = sheet.cell(r, c_ten_me).value.strip().capitalize()
            if c_so_dt_me>-1:
                dt_me = sheet.cell(r, c_so_dt_me).value.strip()
            if c_nguyen_vong>-1:
                ban_dk = sheet.cell( r, c_nguyen_vong).value.strip()
                if not ban_dk.strip(): ban_dk = 'CB'

            if c_so_dt_nt>-1:
                sms_phone = sheet.cell(r, c_so_dt_nt).value.strip()
                if sms_phone:
                    try:
                        validate_phone(sms_phone)
                    except Exception as e:
                        message += u'<li>Ô ' + unicode(cellname(r, c_ngay_sinh)) + u':   Số điện thoại không hợp lệ ' + u'</li>'
                        sms_phone = ''
                        print e
            try:
                if type(birthday) == unicode or type(birthday)== str:
                    birthday = to_date(birthday)
                else:

                    date_value = xlrd.xldate_as_tuple(sheet.cell(r, c_ngay_sinh).value, book.datemode)
                    birthday = date(*date_value[:3])
            except Exception as e:
                print e
                message += u'<li>Ô ' + unicode(cellname(r, c_ngay_sinh)) + u':Không đúng định dạng "ngày/tháng/năm" ' + u'</li>'
                continue
            data = {'fullname': name,
                    'birthday': birthday,
                    'sex': gt,
                    'dan_toc': dan_toc,
                    'birth_place': noi_sinh,
                    'current_address': cho_o_ht,
                    'father_name': ten_bo,
                    'father_phone': dt_bo,
                    'mother_name': ten_me,
                    'mother_phone': dt_me,
                    'ban_dk': ban_dk,
                    'sms_phone': sms_phone}
            student_list.append(data)
            number_ok += 1
        message += u'</ul>'
        return student_list, message, number, number_ok
    elif task == u"import_teacher":
        teacher_list = []
        filepath = os.path.join(TEMP_FILE_LOCATION, file_name)
        if not os.path.isfile(filepath):
            raise NameError, "%s is not a valid filename" % file_name
        try:
            book = xlrd.open_workbook(filepath)
            sheet = book.sheet_by_index(0)
        except Exception as e:
            print e
            return {'error': u'File tải lên không phải file Excel'}

        start_row = -1
        for c in range(0, sheet.ncols):
            flag = False
            for r in range(0, sheet.nrows):
                if sheet.cell_value(r, c) == u'Họ và Tên':
                    start_row = r
                    flag = True
                    break
            if flag: break
            #                                                             CHUA BIEN LUAN TRUONG HOP: start_row = -1, ko co cot ten: Mã học sinh
        if start_row == -1:
            return {'error': u'File tải lên phải có cột "Họ và Tên".'}, u'File tải lên phải có cột "Họ và Tên".', 0, 0
            # start_row != 0
        c_ten = -1
        c_ngay_sinh = -1
        c_gioi_tinh = -1
        c_que_quan = -1
        c_dan_toc = -1
        c_cho_o_ht = -1
        c_to = -1
        c_nhom = -1
        c_chuyen_mon = -1
        number = 0
        number_ok = 0
        for c in range(0, sheet.ncols):
            value = sheet.cell_value(start_row, c)

            if value == u'Họ và Tên':
                c_ten = c
            elif value == u'Ngày sinh':
                c_ngay_sinh = c
            elif value == u'Giới tính':
                c_gioi_tinh = c
            elif value == u'Quê quán':
                c_que_quan = c
            elif value == u'Dân tộc':
                c_dan_toc = c
            elif value == u'Chỗ ở hiện tại':
                c_cho_o_ht = c
            elif value == u'Tổ':
                c_to = c
            elif value == u'Nhóm':
                c_nhom = c
            elif value == u'Dạy môn':
                c_chuyen_mon = c


        for r in range(start_row + 1, sheet.nrows):
            name = ''
            birthday =''
            gt=''
            dan_toc=''
            que_quan=''
            cho_o_ht=''
            to = ''
            nhom = ''
            chuyen_mon = ''
            name = sheet.cell(r, c_ten).value.strip()
            name = ' '.join([i.capitalize() for i in name.split(' ')])
            if not name.strip():
                message += u'<li>Ô ' + unicode(cellname(r, c_ten)) + u':Trống. </li>'
                continue
            number += 1
            birthday = sheet.cell(r, c_ngay_sinh).value
            if not birthday:
                message += u'<li>Ô ' + unicode(cellname(r, c_ngay_sinh)) + u':Trống. </li>'
                birthday = None
            if c_gioi_tinh>-1:
                gt = sheet.cell(r, c_gioi_tinh).value.strip().capitalize()
                if not gt: gt = 'Nam'
            if c_que_quan >-1:
                que_quan = sheet.cell(r, c_que_quan).value.strip()
            if c_dan_toc>-1:
                dan_toc = sheet.cell(r, c_dan_toc).value.strip()
                if not dan_toc.strip(): dan_toc = 'Kinh'
            if c_cho_o_ht>-1:
                cho_o_ht = sheet.cell(r, c_cho_o_ht).value.strip()

            if c_to>-1:
                to = sheet.cell(r, c_to).value.strip()
            if c_nhom>-1:
                nhom = sheet.cell(r, c_nhom).value.strip()
            if c_chuyen_mon>-1:
                chuyen_mon = sheet.cell(r, c_chuyen_mon).value.strip()

            if birthday:
                try:
                    if type(birthday) == unicode or type(birthday)== str:
                        birthday = to_date(birthday)
                    else:

                        date_value = xlrd.xldate_as_tuple(sheet.cell(r, c_ngay_sinh).value, book.datemode)
                        birthday = date(*date_value[:3])
                except Exception as e:
                    print e
                    message += u'<li>Ô ' + unicode(cellname(r, c_ngay_sinh)) + u':Không đúng định dạng "ngày/tháng/năm" ' + u'</li>'
                    continue

            data = {'fullname': name,
                    'birthday': birthday,
                    'sex': gt,
                    'dan_toc': dan_toc,
                    'home_town': que_quan,
                    'current_address': cho_o_ht,
                    'team': to,
                    'group': nhom,
                    'major': chuyen_mon
            }
            teacher_list.append(data)
            number_ok += 1
        message += u'</ul>'
        return teacher_list, message, number, number_ok
    return None

def student_import( request, class_id, request_type='' ):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    file = None
    if request.method == "POST":
        if request.is_ajax( ):
            # the file is stored raw in the request
            try:
                if request_type==u'update':
                    chosen_class = Class.objects.get( id = int(class_id) )
                    year = school.startyear_set.get(time=datetime.date.today().year)
                    current_year = school.year_set.latest('time')
                    term = get_current_term( request)
                    saving_import_student = request.session.pop('saving_import_student')
                    print saving_import_student
                    try:
                        number_of_change = add_many_students( student_list = saving_import_student,
                                                              _class = chosen_class,
                                                              start_year = year, year = current_year,
                                                              term = term, school=school,
                                                              force_update= True)
                    except Exception as e:
                        print e
                    if number_of_change:
                        data =simplejson.dumps({'success': True, 'message': u'Đã cập nhật %s học sinh.' %number_of_change})
                    else:
                        data =simplejson.dumps({'success': True, 'message': u'Thông tin không thay đổi'})
                    return HttpResponse(data, mimetype='json')
                    # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
                try:
                    file = request.FILES.get('file')
                except KeyError:
                    return HttpResponseBadRequest( "AJAX request not valid" )
                    # not an ajax upload, so it was the "basic" iframe version with submission via form
            except Exception as e:
                print e
                raise e
        else:
            is_raw = False
            if len( request.FILES ) == 1:
            # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
            # ID based on a random number, so it cannot be guessed here in the code.
            # Rather than editing Ajax Upload to pass the ID in the querystring,
            # observer that each upload is a separate request,
            # so FILES should only have one entry.
            # Thus, we can just grab the first (and only) value in the dict.
                upload = request.FILES.values( )[ 0 ]
            else:
                raise Http404( "Bad Upload" )
            filename = '_'.join([request.session.session_key,upload.name])
    else:
        return HttpResponseRedirect( reverse('school_index'))
        # save the file

    filename = save_file(request.FILES.get('file'), request.session)
    message = None
    process_file_message = None

    result, process_file_message, number, number_ok = process_file( filename, "import_student")
    existing_student = []
    if 'error' in result:
        success = False
        message = result['error']
        data = [{'name': file.name,
                 'url': filename,
                 'sizef':file.size,
                 'process_message': process_file_message,
                 'error': u'File excel không đúng định dạng'}]
    else:
        chosen_class = Class.objects.get( id = int(class_id) )
        year = school.startyear_set.get(time=datetime.date.today().year)
        current_year = school.year_set.latest('time')
        term = get_current_term( request)
        try:
            existing_student= add_many_students(student_list = result, _class = chosen_class,
                                                start_year = year, year = current_year,
                                                term = term, school=school)


        except Exception as e:
            message = u'Lỗi trong quá trình lưu cơ sở dữ liệu'

        student_confliction = ''
        if existing_student:
            student_confliction = u'Có %s học sinh không được nhập do đã tồn tại trong hệ thống' % len(existing_student)
            request.session['saving_import_student'] = existing_student
        data = [{'name': file.name, 'url': filename,
                 'sizef':file.size,
                 'process_message': process_file_message,
                 'student_confliction': student_confliction,
                 'number': number,
                 'number_ok': number_ok - len(existing_student),
                 'message': 'Nhập dữ liệu thành công'}]
    return HttpResponse( simplejson.dumps( data ) )

def teacher_import( request, request_type = ''):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    file = None
    if request.method == "POST":
        if request.is_ajax( ):
            if request_type==u'update':
                saving_import_teacher = request.session.pop('saving_import_teacher')
                print saving_import_teacher
                for teacher in saving_import_teacher:
                    try:
                        add_teacher(  full_name= teacher['fullname'],
                                      birthday= teacher['birthday'],
                                      sex= teacher['sex'],
                                      dan_toc= teacher['dan_toc'],
                                      home_town= teacher['home_town'],
                                      current_address= teacher['current_address'],
                                      team_id= teacher['team'],
                                      group_id= teacher['group'],
                                      major= teacher['major'],
                                      school= school,
                                      force_update=True)
                    except Exception as e:
                        print e
                data =simplejson.dumps({'success': True, 'message': 'Đã cập nhật.'})
                return HttpResponse(data, mimetype='json')
            try:
                file = request.FILES.get('file')
            except KeyError:
                return HttpResponseBadRequest( "AJAX request not valid" )
                # not an ajax upload, so it was the "basic" iframe version with submission via form
        else:
            is_raw = False
            if len( request.FILES ) == 1:
            # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
            # ID based on a random number, so it cannot be guessed here in the code.
            # Rather than editing Ajax Upload to pass the ID in the querystring,
            # observer that each upload is a separate request,
            # so FILES should only have one entry.
            # Thus, we can just grab the first (and only) value in the dict.
                upload = request.FILES.values( )[ 0 ]
            else:
                raise Http404( "Bad Upload" )
            filename = '_'.join([request.session.session_key,upload.name])
    else:
        return HttpResponseRedirect( reverse('school_index'))
        # save the file
    filename = save_file(request.FILES.get('file'), request.session)
    message = None
    process_file_message = None

    result, process_file_message, number, number_ok = process_file( filename, "import_teacher")
    existing_teacher = []
    saving_import_teacher = []
    if 'error' in result:
        success = False
        message = result['error']
        data = [{'name': file.name,
                 'url': filename,
                 'sizef':file.size,
                 'process_message': process_file_message,
                 'error': u'File excel không đúng định dạng'}]
    else:
        try:
            teacher_list = result
            for teacher in teacher_list:
            #                data = {'fullname': name,
            #                    'birthday': birthday,
            #                    'sex': gt,
            #                    'dan_toc': dan_toc,
            #                    'home_town': que_quan,
            #                    'current_address': cho_o_ht,
            #                    'team': to,
            #                    'group': nhom,
            #                    'major': chuyen_mon
            #                    }
                try:
                    existing = add_teacher(  full_name= teacher['fullname'],
                                             birthday= teacher['birthday'],
                                             sex= teacher['sex'],
                                             dan_toc= teacher['dan_toc'],
                                             home_town= teacher['home_town'],
                                             current_address= teacher['current_address'],
                                             team_id= teacher['team'],
                                             group_id= teacher['group'],
                                             major= teacher['major'],
                                             school= school)
                    if existing:
                        existing_teacher.append(existing)
                        saving_import_teacher.append(teacher)
                except Exception as e:
                    print e

        except Exception as e:
            print e
            message = u'Lỗi trong quá trình lưu cơ sở dữ liệu'

        teacher_confliction = ''
        if existing_teacher:
            teacher_confliction = u'Có %s giáo viên không được nhập do đã tồn tại trong hệ thống' % len(existing_teacher)
            request.session['saving_import_teacher'] = saving_import_teacher
        data = [{'name': file.name, 'url': filename,
                 'sizef':file.size,
                 'process_message': process_file_message,
                 'teacher_confliction': teacher_confliction,
                 'number': number,
                 'number_existing': len(existing_teacher),
                 'number_ok': number_ok - len(existing_teacher),
                 'message': 'Hoàn tất'}]
    return HttpResponse( simplejson.dumps( data ) )

def nhap_danh_sach_trung_tuyen(request):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    message = ''
    _class_list = []
    try:
        this_year = school.year_set.latest('time')
        temp = this_year.class_set.all()
        for _class in temp:
            _class_list.append((_class.id, _class.name))
    except Exception as e:
        print e
        _class_list = None
    if request.method == 'POST':
        form = UploadImportFileForm(request.POST, request.FILES, class_list=_class_list)
        if form.is_valid():
            save_file_name = save_file(form.cleaned_data['import_file'], request.session)
            chosen_class = form.cleaned_data['the_class']
            if chosen_class:
                request.session['save_file_name'] = save_file_name
                request.session['chosen_class'] = chosen_class
                student_list, process_file_message, number, number_ok = process_file(file_name=save_file_name, task="import_student")
                if 'error' in student_list:
                    message = student_list['error']
                else:
                    request.session['student_list'] = student_list
                    return HttpResponseRedirect(reverse('imported_list'))
                    # end if error in save_file_name
        else:
            message = u'Gặp lỗi trong quá trình tải file lên server'
    form = UploadImportFileForm(class_list=_class_list)
    context = RequestContext(request, {'form':form, 'message': message})
    return render_to_response(NHAP_DANH_SACH_TRUNG_TUYEN, context_instance=context)

@transaction.commit_on_success
def manual_adding(request):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    _class_list = []
    message = None
    try:
        this_year = school.year_set.latest('time')
        term = this_year.term_set.get(number__exact=school.status)
        temp = this_year.class_set.all()
        for _class in temp:
            _class_list.append((_class.id, _class.name))
    except Exception as e:
        print e
        _class_list = None

    ns_error = False
    name_error = False
    ns_entered = ""

    if request.method == 'POST':
        form = ManualAddingForm(request.POST, class_list=_class_list)
        student_list = request.session['student_list']
        if form.is_valid():
            chosen_class = form.cleaned_data['the_class']
            if chosen_class != u'0':
                chosen_class = school.year_set.latest('time').class_set.get(id=chosen_class)
                number_of_student = chosen_class.pupil_set.count()
            else:
                chosen_class = None
            if request.POST['clickedButton'] == 'save':
                year = school.startyear_set.get(time=datetime.date.today().year)
                today = datetime.date.today()
                i = number_of_student
                for student in student_list:
                    i += 1
                    data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                            'ban':student['nguyen_vong'], }
                    try:
                        add_student(student=data, _class=chosen_class,
                                    start_year=year, year=this_year,
                                    index = i,
                                    term=term, school=school)
                    except Exception as e:
                        print e
                transaction.commit()
                message = u'Bạn vừa nhập thành công danh sách học sinh trúng tuyển.'
                student_list = []
                request.session['student_list'] = student_list
            elif request.POST['clickedButton'] == 'add':
                try:
                    diem = float(request.POST['diem_hs_trung_tuyen'])
                except Exception as e:
                    diem = 0
                if not request.POST['name_hs_trung_tuyen'].strip():
                    name_error = True
                try:
                    ns = to_date(request.POST['ns_hs_trung_tuyen'])
                    if request.POST['name_hs_trung_tuyen'].strip():
                        element = { 'ten': request.POST['name_hs_trung_tuyen'],
                                    'ngay_sinh': ns,
                                    'nguyen_vong': request.POST['nv_hs_trung_tuyen'],
                                    'tong_diem': diem,
                                    }
                        student_list.append(element)

                except Exception as e:
                    print e
                    ns_error = True
                    ns_entered = request.POST['ns_hs_trung_tuyen']
                request.session['student_list'] = student_list
    else:
        student_list = []
        request.session['student_list'] = student_list
        form = ManualAddingForm(class_list=_class_list)
    context = RequestContext(request, {'student_list': student_list})
    return render_to_response(NHAP_BANG_TAY, {'form':form,
                                              'name_error':name_error,
                                              'ns_error':ns_error,
                                              'ns_entered':ns_entered}, context_instance=context)

@transaction.commit_on_success
def danh_sach_trung_tuyen(request):

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))

    student_list = request.session['student_list']
    term = school.year_set.latest('time').term_set.latest('number')
    chosen_class = request.session['chosen_class']
    current_year = school.year_set.latest('time')
    number_of_student = 0
    if chosen_class != u'0':
        chosen_class = school.year_set.latest('time').class_set.get(id=chosen_class)
        number_of_student = chosen_class.pupil_set.count();
    else:
        chosen_class = None
    message = None

    if request.method == 'POST':
        if request.POST['clickedButton'] == 'save':
            year = school.startyear_set.get(time=datetime.date.today().year)
            today = datetime.date.today()
            i = number_of_student
            for student in student_list:
                i += 1
                data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                        'ban':student['nguyen_vong'], }

                add_student(student=data, _class=chosen_class,
                            start_year=year, year=current_year,
                            index = i,
                            term=term, school=school)
            message = u'Bạn vừa nhập thành công danh sách học sinh trúng tuyển.'
            student_list = []
            request.session['student_list'] = student_list
            return HttpResponseRedirect('/school/viewClassDetail/'+ str(chosen_class.id))
        elif request.POST['clickedButton'] == 'add':

            diem = float(request.POST['diem_hs_trung_tuyen'])
            ns = to_date(request.POST['ns_hs_trung_tuyen'])
            element = {'ten': request.POST['name_hs_trung_tuyen'],
                       'ngay_sinh': ns,
                       'nguyen_vong': request.POST['nv_hs_trung_tuyen'],
                       'tong_diem': diem,
                       }
            student_list.append(element)
            request.session['student_list'] = student_list

    context = RequestContext(request, {'student_list': student_list})
    return render_to_response(DANH_SACH_TRUNG_TUYEN, {'message':message}, context_instance=context)
#------------------------------------------------------------------------------------

def password_change(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    form = PasswordChangeForm(user)
    message = ''
    if request.method == 'POST':
        form = PasswordChangeForm(user,request.POST)
        if form.is_valid():
            form.save()
            message = u'Bạn đã thay đổi mật khẩu thành công'
    t = loader.get_template(os.path.join('school','password_change.html'))
    c = RequestContext(request, {'form':form, 'message':message})
    return HttpResponse(t.render(c))

def username_change(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    form = UsernameChangeForm(user)
    message = ''
    if request.method == 'POST':
        form = UsernameChangeForm(user,request.POST)
        if form.is_valid() and user.userprofile.username_change == 0:
            form.save()
            message = u'Bạn đã thay tên tài khoản thành công'
    t = loader.get_template(os.path.join('school','username_change.html'))
    c = RequestContext(request, {'form':form, 'message':message})
    return HttpResponse(t.render(c))

def student_account(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pos = get_position(request)
    if pos < 4:
        return HttpResponseRedirect('/')
    message = ''
    student = user.userprofile.organization.pupil_set.get(id = student_id)
    url = '/school/student/account/' + student_id
    if request.method == 'POST':
        student.user_id.set_password(student.user_id.username)
        student.save()
        message = 'Mật khẩu của học sinh đã được tạo lại giống tên tài khoản'
    t = loader.get_template(os.path.join('school','account.html'))
    c = RequestContext(request, {'account':student.user_id.username,'url':url,'message':message})
    return HttpResponse(t.render(c))

def teacher_account(request, teacher_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pos = get_position(request)
    if pos < 4:
        return HttpResponseRedirect('/')
    message = ''
    teacher = user.userprofile.organization.teacher_set.get(id = teacher_id)
    url = '/school/teacher/account/' + teacher_id
    if request.method == 'POST':
        teacher.user_id.set_password(teacher.user_id.username)
        teacher.save()
        message = 'Mật khẩu của giáo viên đã được tạo lại giống tên tài khoản'
    t = loader.get_template(os.path.join('school','account.html'))
    c = RequestContext(request, {'account':teacher.user_id.username,'url':url,'message':message})
    return HttpResponse(t.render(c))

def classes(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    pos = get_position(request)
    if pos == 1:
        url = '/school/viewClassDetail/' + str(get_student(request).class_id.id)
        return HttpResponseRedirect(url)
    message = None
    school = get_school(request)
    blockList = school.block_set.all()
    if request.method == 'POST':
        if request.is_ajax():
            cyear = get_current_year(request)
            class_id = request.POST['id']
            c = cyear.class_set.get(id = int(class_id))
            tc = None
            teacher_id = None
            if request.POST['teacher_id'] != u'':
                teacher_id = request.POST['teacher_id']
                teacher = school.teacher_set.get(id = int(teacher_id))
                try:
                    tc = cyear.class_set.get(teacher_id__exact = teacher.id)
                except ObjectDoesNotExist:
                    pass
            else:
                teacher_id = None
            if teacher_id == None or tc == None:
                data = {'name':c.name, 'year_id':c.year_id.id, 'block_id':c.block_id.id, 'teacher_id':teacher_id,'status':c.status,'index':c.index}
                form = ClassForm(school.id, data, instance=c)
                if form.is_valid():
                    form.save()
            else:
                message = 'Giáo viên đã có lớp chủ nhiệm'
                data = simplejson.dumps({'message':message})
                return HttpResponse(data, mimetype = 'json')
    t = loader.get_template(os.path.join('school', 'classes.html'))
    c = RequestContext(request, {   'message': message,
                                    'blockList': blockList,
                                    'pos':pos,})
    return HttpResponse(t.render(c))

def classtab(request, block_id=0):
    try:
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        try:
            school = get_school(request)
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

        pos = get_position(request)
        if pos == 1:
            url = '/school/viewClassDetail/' + str(get_student(request).class_id.id)
            return HttpResponseRedirect(url)
        message = None
        school = get_school(request)
        school_id = school.id
        form = ClassForm(school_id)
        cyear = get_current_year(request)
        if not int(block_id):
            classList = cyear.class_set.order_by('name')
        else:
            block = school.block_set.get(id=int(block_id))
            classList = block.class_set.order_by('name')
        cfl = []
        num = []
        for c in classList:
            cfl.append(ClassForm(school_id, instance=c))
            num.append(c.pupil_set.count())
        list = zip(classList, cfl, num)
        if request.method == 'POST':
            if request.is_ajax() and request.POST['request_type']==u'update':
                class_id = request.POST['id']
                c = classList.get(id = int(class_id))
                tc = None
                teacher_id = None
                if request.POST['teacher_id'] != u'':
                    teacher_id = request.POST['teacher_id']
                    teacher = school.teacher_set.get(id = int(teacher_id))
                    try:
                        tc = cyear.class_set.get(teacher_id__exact = teacher.id)
                    except ObjectDoesNotExist:
                        pass
                else:
                    teacher_id = None
                if not teacher_id or not tc:
                    data = {'name':c.name, 'year_id':c.year_id.id, 'block_id':c.block_id.id, 'teacher_id':teacher_id,'status':c.status,'index':c.index}
                    form = ClassForm(school_id, data, instance=c)
                    if form.is_valid():
                        form.save()
                else:
                    message = 'Giáo viên đã có lớp chủ nhiệm'
                    data = simplejson.dumps({'message':message})
                    return HttpResponse(data, mimetype = 'json')
            elif request.POST['request_type']=='update_all':
                teacher_list = request.POST.getlist('teacher_id')
                i = 0
                for c in classList:
                    data = {'name':c.name, 'year_id':c.year_id.id, 'block_id':c.block_id.id, 'teacher_id':teacher_list[i],'status':c.status,'index':c.index}
                    of = cfl[i]
                    cfl[i] = ClassForm(school_id, data, instance=c)
                    if str(of) != str(cfl[i]):
                        if cfl[i].is_valid():
                            cfl[i].save()
                        message = 'Thông tin lớp đã được cập nhật.'
                    i += 1
                cfl.append(ClassForm(school_id, instance=c))
                url = 'school/classes'
                return HttpResponseRedirect(url)
            list = zip(classList, cfl, num)
        t = loader.get_template(os.path.join('school', 'classtab.html'))
        c = RequestContext(request, {   'list': list,
                                        'form': form,
                                        'message': message,
                                        'classList': classList,
                                        'block_id': block_id,
                                        'pos':pos,})
        return HttpResponse(t.render(c))
    except Exception as e:
        print e
        raise e

#User: loi.luuthe@gmail.com
#This function receives a form from template, and immediately creates new class with from the form information
def addClass(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    school = user.userprofile.organization
    if school.status != 0:
        form = ClassForm(school.id)
        if request.method == 'POST':
            index = get_current_year(request).class_set.count()
            data = {'name':request.POST['name'].strip(), 'year_id':request.POST['year_id'], 'block_id':request.POST['block_id'], 'teacher_id':request.POST['teacher_id'], 'status':school.status,'index':index}
            form = ClassForm(school.id,data)
            if form.is_valid():
                _class = form.save()
                if school.school_level == '1': ds_mon_hoc = CAP1_DS_MON
                elif school.school_level == '2': ds_mon_hoc = CAP2_DS_MON
                elif school.school_level == '3': ds_mon_hoc = CAP3_DS_MON
                else: raise Exception('SchoolLevelInvalid')
                index = 0
                for mon in ds_mon_hoc:
                    index +=1
                    add_subject(subject_name= mon, subject_type= mon, _class=_class, index=index)
                return HttpResponseRedirect('/school/classes')

        t = loader.get_template(os.path.join('school', 'add_class.html'))
        c = RequestContext(request, {'form': form})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template(os.path.join('school', 'add_class.html'))
        c = RequestContext(request)
        return HttpResponse(t.render(c))

def student(request, student_id):
    try:
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        try:
            school = get_school(request)
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))
        if not request.is_ajax():
            raise Exception("PageDoesNotExist")
        try:
            student = Pupil.objects.get(id=student_id)
            if school != student.get_school():
                raise Exception("IllegalAccess")
            return render_to_response(STUDENT, {'student': student}, context_instance = RequestContext(request))
        except ObjectDoesNotExist as e:
            raise Exception("StudentDoesNotExist")
    except Exception as e:
        print e

#User: loi.luuthe@gmail.com
#This function has class_id is an int argument. It gets the information of the class corresponding to the class_id and response to the template
def viewClassDetail(request, class_id, sort_type=0, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    pos = get_position(request)
    if not pos:
        return HttpResponseRedirect('/')
    try:
        cl = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return HttpResponseRedirect('/school/classes')
    cn=gvcn(request, class_id)
    inCl=inClass(request, class_id)
    if not in_school(request, cl.block_id.school_id):
        return HttpResponseRedirect('/')
    message = None
    school = cl.block_id.school_id
    cyear = get_current_year(request)
    classList = cyear.class_set.all()
    form = PupilForm(school.id)

    if request.method == 'POST':
        if request.is_ajax() and request.POST[u'request_type'] == u'del':
            data = request.POST[u'data']
            data = data.split('-')
            for e in data:
                if e.strip():
                    std = Pupil.objects.get(id__exact = int(e))
                    completely_del_student(std)

            data = simplejson.dumps({'success': True})
            return HttpResponse(data, mimetype='json')

        elif request.POST[u'request_type'] == u'add':
            start_year = StartYear.objects.get(time = int(date.today().year), school_id = school.id)
            data = request.POST.copy()
            data.appendlist('school_join_date',date.today().strftime("%d/%m/%Y"))
            data.appendlist('ban_dk',u'CB')
            data.appendlist('quoc_tich',u'Việt Nam')
            data.appendlist('index',cl.pupil_set.count()+1)
            data.appendlist('class_id',class_id)
            data.appendlist('start_year_id',start_year.id)
            form = PupilForm(school.id, data)
            if form.is_valid():
                school_join_date = date.today()
                birthday = to_date(request.POST['birthday'])
                data['birthday'] = birthday
                _class = Class.objects.get(id=class_id)
                index = _class.pupil_set.count() + 1
                student = add_student( student=data, start_year=start_year,
                                       year=get_current_year(request),
                                       _class=_class,
                                       index= index,
                                       term=get_current_term(request),
                                       school=get_school(request),
                                       school_join_date=school_join_date)
                message = u'Bạn vừa thêm 1 học sinh'
                data = simplejson.dumps({'message':message, 'success': True, 'student_id': student.id})
                return HttpResponse(data, mimetype = 'json')
                #form = PupilForm(school.id)
            else:
                message = ''
                try:
                    birthday = to_date(request.POST['birthday'])
                    if birthday >= date.today():
                        message += u'<li> ' + u'Ngày không hợp lệ' + u'</li>'

                    find = start_year.pupil_set.filter( first_name__exact = request.POST['first_name'])\
                    .filter(last_name__exact = request.POST['last_name'])\
                    .filter(birthday__exact = birthday)
                    if find:
                        message += u'<li> ' + u'Học sinh đã tồn tại' + u'</li>'
                except Exception as e:
                    message = u'<li> ' + u'Chưa nhập hoặc nhập không đúng định dạng "ngày/tháng/năm" ' + u'</li>'
                    print e

                if not request.POST['first_name']:
                    message += u'<li> ' + u'Ô tên là bắt buộc' + u'</li>'

                data = simplejson.dumps({'message': message})
                return HttpResponse(data, mimetype='json')
    if int(sort_type) == 0:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('index','first_name', 'last_name','birthday')
        else:
            studentList = cl.pupil_set.order_by('index','-first_name', '-last_name','-birthday')
    if int(sort_type) == 1:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('first_name', 'last_name','birthday')
        else:
            studentList = cl.pupil_set.order_by('-first_name', '-last_name','-birthday')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('birthday')
        else:
            studentList = cl.pupil_set.order_by('-birthday')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('sex')
        else:
            studentList = cl.pupil_set.order_by('-sex')
    if int(sort_type) == 4:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('ban_dk')
        else:
            studentList = cl.pupil_set.order_by('-ban_dk')
    if int(sort_type) == 5:
        if int(sort_status) == 0:
            studentList = cl.pupil_set.order_by('school_join_date')
        else:
            studentList = cl.pupil_set.order_by('-school_join_date')

    tmp = get_student(request)
    inCl = inClass(request, class_id)
    id = 0
    if tmp:
        id = tmp.id


    currentTerm= get_current_term(request)
    if currentTerm.number ==3:
        currentTerm=Term.objects.get(year_id=currentTerm.year_id,number=2)

    t = loader.get_template(os.path.join('school', 'classDetail.html'))
    c = RequestContext(request, {   'form': form,
                                    'csrf_token': get_token(request),
                                    'message': message,
                                    'studentList': studentList,
                                    'class': cl,
                                    'cl':classList,
                                    'inClass' : inCl,
                                    'sort_type':int(sort_type),
                                    'sort_status':int(sort_status),
                                    'next_status':1-int(sort_status),
                                    'pos': pos,
                                    'gvcn':cn,
                                    'student_id':id,
                                    'currentTerm':currentTerm,
                                    })
    return HttpResponse(t.render(c))

#sort_type = '1': fullname, '2': birthday, '3':'sex'
#sort_status = '0':ac '1':'dec
def teachers(request,  sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    school = get_school(request)
    pos = get_position(request)
    message = None
    form = TeacherForm(school.id)
    school = get_school(request)
    if request.is_ajax():
        if request.POST['request_type'] == u'addTeam':
            data = {'name': request.POST['name'].strip(), 'school_id': school.id}
            try:
                t = school.team_set.get(name=request.POST['name'].strip())
                message = 'Tổ này đã tồn tại'
            except ObjectDoesNotExist:
                message = 'OK'
                t = TeamForm(data)
                if t.is_valid():
                    t.save()
            data = simplejson.dumps({'message': message})
            return HttpResponse(data, mimetype='json')
        if request.POST['request_type'] == u'delete_team':
            t = school.team_set.get(id = request.POST['id'])
            teacherList = t.teacher_set.all()
            for teacher in teacherList:
                teacher.group_id = None
                teacher.team_id = None
            t.delete()
            return HttpResponse()
        if request.POST['request_type'] == u'delete_group':
            g = Group.objects.get(id = request.POST['id'])
            teacherList = g.teacher_set.all()
            for teacher in teacherList:
                teacher.group_id = None
            g.delete()
            return HttpResponse()
        if request.POST['request_type'] == u'rename_team':
            t = school.team_set.get(id = request.POST['id'])
            try:
                tmp = school.team_set.get(name=request.POST['name'].strip())
                message = u'Tên Tổ này đã tồn tại'
            except ObjectDoesNotExist:
                message = u'Đổi tên thành công'
                t.name = request.POST['name'].strip()
                t.save()
            data = simplejson.dumps({'message': message})
            return HttpResponse(data, mimetype='json')
    num = []
    teamList = school.team_set.all()
    t = loader.get_template(os.path.join('school', 'teachers.html'))

    c = RequestContext(request, {   'list' : teamList,
                                    'pos':pos,
                                    'sort_type':sort_type,
                                    'sort_status':sort_status,
                                    'next_status':1-int(sort_status),
                                    })
    return HttpResponse(t.render(c))

def team(request, team_id ,sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    school = get_school(request)
    pos = get_position(request)
    message = None
    form = TeacherForm(school.id)
    school = get_school(request)
    if request.method == 'POST' and request.is_ajax():
        try:
            if request.POST['request_type'] == u'addGroup':
                try:
                    g = Group.objects.get(name = request.POST['name'].strip(), team_id=request.POST['team_id'])
                    message = u'Nhóm này đã tồn tại'
                    data = simplejson.dumps({'message': message})
                    return HttpResponse(data, mimetype='json')
                except ObjectDoesNotExist:
                    data = {'name': request.POST['name'].strip(), 'team_id': request.POST['team_id']}
                    t = GroupForm(data)
                    if t.is_valid():
                        t.save()
                    return HttpResponseRedirect('/school/team/' + request.POST['team_id'])
            if request.POST['request_type'] == u'renameGroup':
                g = Group.objects.get( id = request.POST['id'])
                try:
                    _t = g.team_id.group_set.get( name = request.POST['name'])
                    message = u'Nhóm này đã tồn tại'
                    data = simplejson.dumps({'message': message})
                    return HttpResponse(data, mimetype='json')
                except ObjectDoesNotExist:
                    g.name = request.POST['name'].strip()
                    g.save()
                    return HttpResponseRedirect('/school/team/' + team_id)
        except Exception as e:
            print e
            pass
    team = school.team_set.get(id=team_id)
    groupList = team.group_set.all()
    t = loader.get_template(os.path.join('school', 'team.html'))

    c = RequestContext(request, {   'groupList' : groupList,
                                    'team' : team,
                                    'pos':pos,
                                    'sort_type':sort_type,
                                    'sort_status':sort_status,
                                    'next_status':1-int(sort_status),
                                    })
    return HttpResponse(t.render(c))

def teachers_tab(request, sort_type=1, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    school = get_school(request)
    pos = get_position(request)
    message = None
    form = TeacherForm(school.id)
    if request.is_ajax():
        if request.method == 'POST' and request.POST['request_type'] == u'team':
            try:
                t = school.teacher_set.get(id=request.POST['id'])
                if request.POST['team']:
                    team = school.team_set.get(id=request.POST['team'])
                else:
                    team = None
                t.team_id = team
                t.group_id = None
                t.save()
                response = simplejson.dumps({'success': True})
                return HttpResponse(response, mimetype='json')
            except Exception as e:
                print e
        elif request.method == 'POST' and request.POST['request_type'] == u'major':
            try:
                t = school.teacher_set.get(id=request.POST['id'])
                major = request.POST['major']
                t.major = major
                t.save()
                response = simplejson.dumps({'success': True})
                return HttpResponse(response, mimetype='json')
            except Exception as e:
                print e
        elif request.method == 'POST' and request.POST['request_type']==u'add':
            print request.POST
            if request.POST['first_name'].strip():
                name = request.POST['first_name'].split()
                last_name = ' '.join(name[:len(name)-1])
                first_name = name[len(name)-1]
            else:
                last_name = ''
                first_name = ''
            index = school.teacher_set.count() + 1
            teamlist = request.POST.getlist('team_id')
            tid = teamlist.pop()
            if tid != u'':
                team = school.team_set.get(id = tid)
                team_id = team.id
            else:
                team = None
                team_id = ''
            data = {'first_name':first_name, 'last_name':last_name, 'birthday':request.POST['birthday'],
                    'sex':request.POST['sex'], 'school_id':school.id, 'home_town':request.POST['home_town'].strip(),
                    'team_id': team_id, 'major' : request.POST['major'], 'index':index}
            form = TeacherForm(school.id,data)
            if form.is_valid():
                birthday = to_date(request.POST['birthday'])
                try:
                    test = school.teacher_set.get(first_name__exact=data['first_name'], last_name__exact=data['last_name'],birthday__exact=birthday)
                    message = 'Giáo viên này đã tồn tại trong hệ thống'
                except ObjectDoesNotExist:
                    add_teacher(first_name=data['first_name'], last_name=data['last_name'], school=get_school(request), birthday=birthday,
                                sex=data['sex'], home_town=data['home_town'], team_id =team, major=data['major'])
                    message = 'Bạn vừa thêm một giáo viên mới'
                form = TeacherForm(school.id)
            else:
                if data['first_name'] != '':
                    data['first_name'] = data['last_name'] + ' ' + data['first_name']
                    form = TeacherForm(school.id,data)

    if int(sort_type) == 1:
        if int(sort_status) == 0:
            teacherList = school.teacher_set.order_by('first_name', 'last_name')
        else:
            teacherList = school.teacher_set.order_by('-first_name', '-last_name')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            teacherList = school.teacher_set.order_by('birthday')
        else:
            teacherList = school.teacher_set.order_by('-birthday')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
            teacherList = school.teacher_set.order_by('sex')
        else:
            teacherList = school.teacher_set.order_by('-sex')
    if int(sort_type) == 4:
        if int(sort_status) == 0:
            teacherList = school.teacher_set.order_by('team_id')
        else:
            teacherList = school.teacher_set.order_by('-team_id')

    flist = []
    i = 0
    for t in teacherList:
        flist.append(TeacherForm(school.id))
        flist[i] = TeacherForm(school.id,instance = t)
        i += 1
    list = zip(teacherList, flist)
    t = loader.get_template(os.path.join('school', 'teachers_tab.html'))
    tmp = get_teacher(request)
    id = 0
    if tmp:
        id = tmp.id
    c = RequestContext(request, {   'form': form,
                                    'message': message,
                                    'list': list,
                                    'sort_type':sort_type,
                                    'sort_status':sort_status,
                                    'next_status':1-int(sort_status),
                                    'pos':pos,
                                    'teacher_id':id})
    return HttpResponse(t.render(c))
def teachers_in_team(request, team_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    pos = get_position(request)
    school = get_school(request)
    if request.is_ajax():
        if (request.method == 'POST' and request.POST['request_type'] == u'team'):
            t = school.teacher_set.get(id = request.POST['id'])
            if request.POST['team']:
                team = school.team_set.get (id = request.POST['team'])
                t.team_id = team
                t.group_id = None
                t.save()
            else:
                t.team_id = None
                t.group_id = None
                t.save()
            response = simplejson.dumps({'success': True})
            return HttpResponse( response, mimetype='json')
        elif (request.method == 'POST' and request.POST['request_type'] == u'major'):
            try:
                t = school.teacher_set.get(id=request.POST['id'])
                major = request.POST['major']
                t.major = major
                t.save()
                response = simplejson.dumps({'success': True})
                return HttpResponse(response, mimetype='json')
            except Exception as e:
                print e
        if (request.method == 'POST' and request.POST['request_type'] == u'group'):
            t = school.teacher_set.get(id = request.POST['id'])
            team = school.team_set.get(id = team_id)
            if request.POST['group']:
                group = team.group_set.get (id = request.POST['group'])
                t.group_id = group
                t.save()
            else:
                t.group_id = None
                t.save()
            response = simplejson.dumps({'success': True})
            return HttpResponse( response, mimetype='json')
    teacherList =  school.teacher_set.filter(team_id = team_id).order_by('first_name', 'last_name')
    flist = []
    team = school.team_set.get(id = team_id)
    i = 0
    for t in teacherList:
        flist.append(TeacherITForm(team_id))
        flist[i] = TeacherITForm(team_id,instance = t)
        i += 1
    list = zip(teacherList, flist)
    t = loader.get_template(os.path.join('school', 'teachers_in_team.html'))
    tmp = get_teacher(request)
    id = 0
    if (tmp):
        id = tmp.id
    c = RequestContext(request, {   'list': list,
                                    'pos':pos,
                                    'teacher_id':id,
                                    'team' : team})
    return HttpResponse(t.render(c))

def teachers_in_group(request, group_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    pos = get_position(request)
    school = get_school(request)
    if request.is_ajax():
        if (request.method == 'POST' and request.POST['request_type'] == u'team'):
            t = school.teacher_set.get(id = request.POST['id'])
            if request.POST['team']:
                team = school.team_set.get (id = request.POST['team'])
                t.team_id = team
                t.group_id = None
                t.save()
            else:
                t.team_id = None
                t.group_id = None
                t.save()
            response = simplejson.dumps({'success': True})
            return HttpResponse( response, mimetype='json')
        elif (request.method == 'POST' and request.POST['request_type'] == u'major'):
            try:
                t = school.teacher_set.get(id=request.POST['id'])
                major = request.POST['major']
                t.major = major
                t.save()
                response = simplejson.dumps({'success': True})
                return HttpResponse(response, mimetype='json')
            except Exception as e:
                print e
        if (request.method == 'POST' and request.POST['request_type'] == u'group'):
            t = school.teacher_set.get(id = request.POST['id'])
            if request.POST['group']:
                group = Group.objects.get(id = request.POST['group'])
                t.group_id = group
                t.save()
            else:
                t.group_id = None
                t.save()
            response = simplejson.dumps({'success': True})
            return HttpResponse( response, mimetype='json')
    teacherList =  school.teacher_set.filter(group_id = group_id).order_by('first_name', 'last_name')
    flist = []
    group = Group.objects.get(id = group_id)
    team = group.team_id
    i = 0
    for t in teacherList:
        flist.append(TeacherITForm(team.id))
        flist[i] = TeacherITForm(team.id,instance = t)
        i += 1
    list = zip(teacherList, flist)
    t = loader.get_template(os.path.join('school', 'teachers_in_group.html'))
    tmp = get_teacher(request)
    id = 0
    if (tmp):
        id = tmp.id
    c = RequestContext(request, {   'list': list,
                                    'pos':pos,
                                    'teacher_id':id,
                                    'group' : group})
    return HttpResponse(t.render(c))

def viewTeacherDetail(request, teacher_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    message = None
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return HttpResponseRedirect('/school/teachers')
    if in_school(request, teacher.school_id) == False:
        return HttpResponseRedirect('/')
    pos = get_position(request)
    school = get_school(request)
    if (pos==3) and not(get_teacher(request).id == int(teacher_id)):
        pos = 1
    if (pos < 1):
        return HttpResponseRedirect('/')
    form = TeacherForm (school.id,instance=teacher)
    ttcnform = TeacherTTCNForm(instance=teacher)
    ttllform = TeacherTTLLForm(instance=teacher)
    if request.method == 'POST':
        data = request.POST.copy()
        if data['request_type'] == 'ttcn':
            data['first_name'] = data['first_name'].strip()
            data['last_name'] = data['last_name'].strip()
            ttcnform = TeacherTTCNForm(data, instance=teacher)
            if ttcnform.is_valid():
                ttcnform.save()
                message = 'Bạn vừa cập nhật thành công thông tin cá nhân'
        if data['request_type'] == 'ttll':
            ttllform = TeacherTTLLForm(data, instance=teacher)
            if ttllform.is_valid():
                ttllform.save()
                message = 'Bạn vừa cập nhật thành công thông tin liên lạc'
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['request_type'] == 'ttcn':
                first_name = ''
                last_name = ''
                birthday = ''
                if not ttcnform.is_valid():
                    message = 'Có lỗi ở dữ liệu nhập vào'
                    for a in ttcnform:
                        if a.name == 'first_name':
                            if a.errors:
                                first_name = str(a.errors)
                                print first_name
                        if a.name == 'last_name':
                            if a.errors:
                                last_name = str(a.errors)
                                print last_name
                        if a.name == 'birthday':
                            if a.errors:
                                birthday = str(a.errors)
                                print birthday
                response = simplejson.dumps({'message': message, 'response_type': 'ttcn',
                                             'first_name':first_name, 'last_name':last_name,'birthday':birthday})
                return HttpResponse(response, mimetype = 'json')
            if request.POST['request_type'] == 'ttll':
                phone = ''
                email = ''
                sms_phone = ''
                if not ttllform.is_valid():
                    message = 'Có lỗi ở dữ liệu nhập vào'
                    for a in ttllform:
                        if a.name == 'phone':
                            if a.errors:
                                phone = str(a.errors)
                        if a.name == 'email':
                            if a.errors:
                                email = str(a.errors)
                        if a.name == 'sms_phone':
                            if a.errors:
                                sms_phone = str(a.errors)
                response = simplejson.dumps({'message': message, 'response_type': 'ttll',
                                             'phone':phone, 'email':email,'sms_phone':sms_phone})
                return HttpResponse(response, mimetype = 'json')
    t = loader.get_template(os.path.join('school', 'teacher_detail.html'))
    c = RequestContext(request, {   'form': form, 'message': message,
                                    'id': teacher_id, 'ttcnform':ttcnform,
                                    'pos': pos, 'ttllform':ttllform})
    return HttpResponse(t.render(c))

def subjectPerClass(request, class_id, sort_type=4, sort_status=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    pos = get_position(request)
    if (pos == 0):
        return HttpResponseRedirect('/')
    message = None
    cl = Class.objects.get(id=class_id)
    term=get_current_term(request)
    school = get_school(request)
    try:
        if int(sort_type) == 1:
            if int(sort_status) == 0:
                subjectList = cl.subject_set.order_by('name')
            else:
                subjectList = cl.subject_set.order_by('-name')
        if int(sort_type) == 2:
            if int(sort_status) == 0:
                subjectList = cl.subject_set.order_by('hs')
            else:
                subjectList = cl.subject_set.order_by('-hs')
        if int(sort_type) == 3:
            if int(sort_status) == 0:
                subjectList = cl.subject_set.order_by('teacher_id__first_name')
            else:
                subjectList = cl.subject_set.order_by('-teacher_id__first_name')
        if int(sort_type) == 4:
            if int(sort_status) == 0:
                subjectList = cl.subject_set.order_by('index')
            else:
                subjectList = cl.subject_set.order_by('-index')
    except Exception as e:
        print e

    form = SubjectForm(school.id)
    sfl = []
    for s in subjectList:
        sfl.append(SubjectForm(school.id, instance=s))
    list = zip(subjectList, sfl)
    if request.is_ajax():
        sid = request.POST['id']
        sub = cl.subject_set.get(id = sid)
        if request.POST['request_type'] == u'teacher':
            if request.POST['teacher'] != u'':
                shs = int(request.POST['teacher'])
            else:
                shs = None
            if shs:
                teacher = school.teacher_set.get(id = shs)
            else:
                teacher = None
            sub.teacher_id = teacher
            sub.save()
        if request.POST['request_type'] == u'type':
            if request.POST['type'] != u'':
                type = request.POST['type']
            else:
                type = None
            try:
                sub.type = type
                sub.save()
            except Exception as e:
                print e

        elif request.POST['request_type'] == u'primary':
            shs = request.POST['primary']
            sub.primary = shs
            sub.save()

        elif request.POST['request_type'] == u'hs':
            shs = float(request.POST['hs'])
            sub.hs = shs
            sub.save()
    elif request.method == 'POST':
        hs_list = request.POST.getlist('hs')
        teacher_list = request.POST.getlist('teacher_id')
        p_list = request.POST.getlist('primary')
        t_list = request.POST.getlist('type')
        i = 0
        for s in subjectList:
            data = {'name':s.name, 'hs':hs_list[i], 'class_id':class_id, 'teacher_id':teacher_list[i], 'index':i, 'primary':p_list[i], 'type':t_list[i]}
            of = sfl[i]
            sfl[i] = SubjectForm(school.id, data, instance=s)
            if str(of) != str(sfl[i]):
                if sfl[i].is_valid():
                    sfl[i].save()
                    message = 'Danh sách môn học đã được cập nhật.'
            i += 1
        if teacher_list[i] != u'' or request.POST['name'].strip() != u'' or hs_list[i] != u'':
            index = i+1
            data = {'name':request.POST['name'].strip(), 'hs':hs_list[i], 'class_id':class_id, 'teacher_id':teacher_list[i], 'index':index, 'primary':p_list[i], 'type':t_list[i]}
            form = SubjectForm(school.id, data)
            if form.is_valid():
                _class = Class.objects.get(id=class_id)
                if teacher_list[i] != u'':
                    teacher = Teacher.objects.get(id=int(data['teacher_id']))
                    add_subject(subject_name=data['name'], hs=float(data['hs']), teacher=teacher, _class=_class, index = index, subject_type=data['type'])
                    form = SubjectForm(school.id)
                else:
                    add_subject(subject_name=data['name'], hs=float(data['hs']), _class=_class, index = index, subject_type = data['type'])
                    form = SubjectForm(school.id)
                message = 'Môn học mới đã được thêm.'
            else:
                message = None
    if int(sort_type) == 1:
        if int(sort_status) == 0:
            subjectList = cl.subject_set.order_by('name')
        else:
            subjectList = cl.subject_set.order_by('-name')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            subjectList = cl.subject_set.order_by('hs')
        else:
            subjectList = cl.subject_set.order_by('-hs')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
            subjectList = cl.subject_set.order_by('teacher_id__first_name')
        else:
            subjectList = cl.subject_set.order_by('-teacher_id__first_name')
    if int(sort_type) == 4:
        subjectList = cl.subject_set.order_by('index')

    sfl = []
    year = get_current_year(request)
    classList = year.class_set.all()
    for s in subjectList:
        sfl.append(SubjectForm(school.id, instance=s))
    list = zip(subjectList, sfl)
    t = loader.get_template(os.path.join('school', 'subject_per_class.html'))
    c = RequestContext(request, {   'list':list,
                                    'form': form,
                                    'message': message,
                                    'subjectList': subjectList,
                                    'class': cl,
                                    'sort_type': sort_type,
                                    'sort_status':sort_status,
                                    'next_status':1-int(sort_status),
                                    'term':term,
                                    'classList':classList,
                                    'pos':pos})
    return HttpResponse(t.render(c))

def viewStudentDetail(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    pos = get_position(request)
    if (pos==1) and not(get_student(request).id==int(student_id)):
        pos = 2
    if get_position(request) < 1:
        return HttpResponseRedirect('/')
    message = None
    pupil = Pupil.objects.get(id=student_id)
    school_id = pupil.school_id.id
    if not in_school(request, pupil.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    form = PupilForm (school_id, instance=pupil)
    ttcnform = ThongTinCaNhanForm(school_id, instance=pupil)
    ttllform = ThongTinLienLacForm(instance=pupil)
    ttgdform = ThongTinGiaDinhForm(instance=pupil)
    ttddform = ThongTinDoanDoiForm(student_id,instance=pupil)
    if request.method == 'POST':
        print request.POST
        data = request.POST.copy()
        if request.POST['request_type'] == 'ttcn':
            data['first_name'] = data['first_name'].strip()
            data['last_name'] = data['last_name'].strip()
            ttcnform = ThongTinCaNhanForm(school_id, data, instance=pupil)
            if ttcnform.is_valid():
                ttcnform.save()
                message = 'Bạn đã cập nhật thành công thông tin cá nhân'
        elif request.POST['request_type'] == 'ttll':
            ttllform = ThongTinLienLacForm(data, instance=pupil)
            if ttllform.is_valid():
                ttllform.save()
                message = 'Bạn đã cập nhật thành công thông tin liên lạc'
        elif request.POST['request_type'] == 'ttgd':
            ttgdform = ThongTinGiaDinhForm(data, instance=pupil)
            if ttgdform.is_valid():
                ttgdform.save()
                message = 'Bạn đã cập nhật thành công thông gia đình'
        elif request.POST['request_type'] == 'ttdd':
            ttddform = ThongTinDoanDoiForm(student_id, data, instance=pupil)
            if ttddform.is_valid():
                ttddfrom.save()
                message = 'Bạn đã cập nhật thành công thông tin đoàn đội'
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['request_type'] == 'ttcn':
                first_name = ''
                last_name = ''
                birthday = ''
                school_join_date = ''
                school_join_mark = ''
                if not ttcnform.is_valid():
                    message = 'Có lỗi ở dữ liệu nhập vào'
                    for a in ttcnform:
                        if a.name == 'first_name':
                            if a.errors:
                                first_name = str(a.errors)
                        if a.name == 'last_name':
                            if a.errors:
                                last_name = str(a.errors)
                        if a.name == 'birthday':
                            if a.errors:
                                birthday = str(a.errors)
                        if a.name == 'school_join_date':
                            if a.errors:
                                school_join_date = str(a.errors)
                        if a.name == 'school_join_mark':
                            if a.errors:
                                school_join_mark = str(a.errors)
                response = simplejson.dumps({'message': message, 'response_type': 'ttcn',
                                             'first_name':first_name, 'last_name':last_name,
                                             'birthday':birthday, 'school_join_date':school_join_date,
                                             'school_join_mark':school_join_mark})
                return HttpResponse(response, mimetype = 'json')
            if request.POST['request_type'] == 'ttll':
                phone = ''
                father_phone = ''
                mother_phone = ''
                email = ''
                sms_phone = ''
                if not ttllform.is_valid():
                    message = 'Có lỗi ở dữ liệu nhập vào'
                    for a in ttllform:
                        if a.name == 'phone':
                            if a.errors:
                                phone = str(a.errors)
                        if a.name == 'father_phone':
                            if a.errors:
                                father_phone = str(a.errors)
                        if a.name == 'mother_phone':
                            if a.errors:
                                mother_phone = str(a.errors)
                        if a.name == 'email':
                            if a.errors:
                                email = str(a.errors)
                        if a.name == 'sms_phone':
                            if a.errors:
                                sms_phone = str(a.errors)
                response = simplejson.dumps({'message': message, 'response_type': 'ttll',
                                             'father_phone':father_phone, 'mother_phone':mother_phone,
                                             'phone':phone, 'email':email,'sms_phone':sms_phone})
                return HttpResponse(response, mimetype = 'json')
            if request.POST['request_type'] == 'ttgd':
                father_birthday = ''
                mother_birthday = ''
                if not ttgdform.is_valid():
                    message = 'Có lỗi ở dữ liệu nhập vào'
                    for a in ttgdform:
                        if a.name == 'father_birthday':
                            father_birthday = str(a.errors)
                        if a.name == 'mother_birthday':
                            mother_birthday = str(a.errors)
                response = simplejson.dumps({'message': message, 'response_type': 'ttgd',
                                             'father_birthday':father_birthday, 'mother_birthday':mother_birthday})
                return HttpResponse(response, mimetype = 'json')
            if request.POST['request_type'] == 'ttdd':
                ngay_vao_doi = ''
                ngay_vao_doan = ''
                ngay_vao_dang = ''
                if not ttddform.is_valid():
                    message = u'Có lỗi ở dữ liệu nhập vào'
                    for a in ttddform:
                        if a.name == 'ngay_vao_doan':
                            if a.errors:
                                ngay_vao_doan = str(a.errors)
                        if a.name == 'ngay_vao_doi':
                            if a.errors:
                                ngay_vao_doi = str(a.errors)
                        if a.name == 'ngay_vao_dang':
                            if a.errors:
                                ngay_vao_dang = str(a.errors)
                response = simplejson.dumps({'message': message, 'response_type': 'ttdd',
                                             'ngay_vao_doi':ngay_vao_doi, 'ngay_vao_doan':ngay_vao_doan,
                                             'ngay_vao_dang':ngay_vao_dang})
                return HttpResponse(response, mimetype = 'json')
    t = loader.get_template(os.path.join('school', 'student_detail.html'))
    c = RequestContext(request, {   'form': form,
                                    'ttcnform': ttcnform,
                                    'ttllform': ttllform,
                                    'ttgdform': ttgdform,
                                    'ttddform': ttddform,
                                    'message': message,
                                    'id': student_id,
                                    'class':pupil.class_id,
                                    'pos':pos,
                                    'student': pupil,
                                    }
    )
    return HttpResponse(t.render(c))

def diem_danh(request, class_id, day, month, year):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    cl = Class.objects.get(id__exact=class_id)
    if not in_school(request, cl.block_id.school_id):
        return HttpResponseRedirect('/')
    url = '/school/dsnghi/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
    pos = get_position(request)
    if (pos < 3 or (pos == 3 and not gvcn(request,class_id))):
        return HttpResponseRedirect(url)
    message = ''
    listdh = None
    term = None
    dncdata = {'date':date(int(year),int(month),int(day)),'class_id':class_id}
    year_id = get_current_year(request).id
    dncform = DateAndClassForm(year_id,dncdata)
    if request.is_ajax():
        if request.method == 'POST':
            request_type = request.POST[u'request_type']
            if request_type == u'update':
                id = request.POST[u'id']
                loai = request.POST[u'loai']
                student = Pupil.objects.get( id = int(id))
                time = date(int(year), int(month), int(day))
                diemdanh = student.diemdanh_set.filter( student_id__exact = student)\
                .filter( time__exact = time)
                if not diemdanh:

                    diemdanh = DiemDanh()
                    diemdanh.term_id = get_current_term(request)
                    diemdanh.student_id = student
                    diemdanh.time = time
                    diemdanh.loai = loai
                    diemdanh.save()
                else:
                    diemdanh = diemdanh[0]
                    if loai == 'k':
                        diemdanh.delete()
                        message = u'No need to update'
                        data = simplejson.dumps({'message':message})
                        return HttpResponse(data, mimetype = 'json')

                    if diemdanh.loai != loai:
                        diemdanh.loai = loai
                        diemdanh.save()

                message = student.full_name() + ': updated.'
                data = simplejson.dumps({'message': message})
                return HttpResponse( data, mimetype = 'json')
            if request_type == 'sms':
                data = request.POST[u'data']
                sms_message = ''
                data = data.split(':')
                for element in data:
                    if element:
                        element = element.split('-')
                        id = element[0]
                        loai = element[1]
                        # send sms
                        student = Pupil.objects.get( id = id)
                        phone_number = student.sms_phone

                        if loai == 'k':
                            loai = u'đi học'
                        elif loai == u'Có phép':
                            loai = u'nghỉ học có phép'
                        else:
                            loai = u'nghỉ học không phép'
                        name = ' '.join([student.last_name,student.first_name])
                        time = '/'.join([str(day),str(month),str(year)])
                        sms_message = u'Em '+name+u' đã ' + loai + u'.\n Ngày: ' + time + '.'
                        if phone_number:
                            try:
                                sent = sendSMS(phone_number, to_en1(sms_message), user)
                            except Exception as e:
                                if e.message == 'InvalidPhoneNumber':
                                    message = message + u'<li><b>Số ' + str(phone_number)\
                                              + u' không tồn tại</b>'\
                                              + u': ' + sms_message + u'</li>'
                                    continue
                                else:
                                    raise e
                            if sent == '1':
                                message = message + u'<li><b>-> ' + str(phone_number) + u': ' + sms_message + u'</b></li>'
                            else:
                                print sent
                                message = message + u'<li> ' + str(phone_number) + u': ' + sms_message + u'</li>'
                        else:
                            message = message + u'<li> ' + u'<b>Không số</b>' + u': ' + sms_message + u'</li>'
                data = simplejson.dumps({'message':message})
                return HttpResponse(data, mimetype = 'json')
        else:
            raise Exception('StrangeRequestMethod')
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('index','first_name', 'last_name')
    time = date(int(year), int(month), int(day))
    term = get_current_term(request)
    form = []
    for p in pupilList:
        try:
            dd = DiemDanh\
            .objects.get(time__exact=time, student_id__exact=p.id, term_id__exact=term.id)
            form.append(DiemDanhForm(instance=dd))
        except ObjectDoesNotExist:
            form.append(DiemDanhForm())
    listdh = zip(pupilList, form)
    try:
        if request.method == 'POST':
        #            message = 'Điểm danh lớp ' + str(Class.objects.get(id=class_id)) + ', ngày ' + str(time) + ' đã xong.'
            message = 'Đã lưu điểm danh.'
            list = request.POST.getlist('loai')
            i = 0
            for p in pupilList:
                try:
                    dd = DiemDanh.objects.get(time__exact=time, student_id__exact=p.id, term_id__exact=term.id)
                    if list[i] != 'k':
                        data = {'student_id':p.id, 'time':time, 'loai':list[i], 'term_id':term.id}
                        of = form[i]
                        form[i] = DiemDanhForm(data, instance=dd)
                        if str(of) != str(form[i]):
                            if form[i].is_valid():
                                form[i].save()
                    else:
                        form[i] = DiemDanhForm()
                        dd.delete()
                    i += 1
                except ObjectDoesNotExist:
                    if list[i] != 'k':
                        data = {'student_id':p.id, 'time':time, 'loai':list[i], 'term_id':term.id}
                        form[i] = DiemDanhForm(data)
                        if form[i].is_valid():
                            form[i].save()
                    i += 1
    except IndexError:
        message = None
    listdh = zip(pupilList, form)
    t = loader.get_template(os.path.join('school', 'diem_danh.html'))
    c = RequestContext(request, {'dncform':dncform, 'form':form, 'pupilList': pupilList, 'time': time, 'message':message, 'class_id':class_id, 'time':time, 'list':listdh,
                                 'day':day, 'month':month, 'year':year, 'cl':cl,'pos':pos})
    return HttpResponse(t.render(c))

def time_select(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    message = 'Chọn ngày điểm danh'
    try:
        cl = Class.objects.get(id__exact=class_id)
        term = get_current_term(request)
    except ObjectDoesNotExist:
        message = None
    form = DateForm()
    day = int(date.today().day)
    month = int(date.today().month)
    year = int(date.today().year)
    url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
    return HttpResponseRedirect(url)

def tnc_select(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    y = get_current_year(request)
    year_id = y.id
    pos = get_position(request)
    if (pos < 2 and pos !=3):
        return HttpResponseRedirect('/')
    elif (pos == 3):
        try:
            tc = y.class_set.get(teacher_id__exact = request.user.teacher.id)
            url = '/school/diemdanh/' + str(tc.id) + '/' + str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)
            return HttpResponseRedirect(url)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')
    message = 'Hãy chọn ngày và lớp học bạn muốn điểm danh'
    form = DateAndClassForm(year_id)
    if request.method == 'POST':
        form = DateAndClassForm(year_id,request.POST)
        if form.is_valid():
            d = to_date(request.POST['date'])
            class_id = str(request.POST['class_id'])
            day = d.day
            month = d.month
            year = d.year
            url = '/school/diemdanh/' + class_id + '/' + str(day) + '/' + str(month) + '/' + str(year)
            return HttpResponseRedirect(url)
        else:
            message = 'Chọn lớp và ngày chưa đúng.'
    t = loader.get_template(os.path.join('school', 'time_class_select.html'))
    c = RequestContext(request, {'form':form, 'message':message})
    return HttpResponse(t.render(c))

def ds_nghi(request, class_id, day, month, year):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pos = get_position(request)
    if (pos == 3 and not gvcn(request,class_id)):
        pos = 2
    cl  = Class.objects.get(id=class_id)
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name')
    time = date(int(year), int(month), int(day))
    term = get_current_term(request)
    dncdata = {'date':date(int(year),int(month),int(day)),'class_id':class_id}
    year_id = get_current_year(request).id
    dncform = DateAndClassForm(year_id,dncdata)
    hs_nghi = []
    stt = []
    message = ''
    if request.is_ajax():
        if request.method == 'POST':
            data = request.POST[u'data']
            sms_message = ''
            data = data.split(':')
            for element in data:
                if element:
                    element = element.split('-')
                    id = element[0]
                    loai = element[1]
                    # send sms
                    student = Pupil.objects.get( id = id)
                    phone_number = student.sms_phone

                    loai = loai.strip()
                    if loai == 'k':
                        loai = u'đi học'
                    elif loai == u'Có phép':
                        loai = u'nghỉ học có phép'
                    else:
                        loai = u'nghỉ học không phép'
                    name = ' '.join([student.last_name,student.first_name])
                    time = '/'.join([str(day),str(month),str(year)])
                    sms_message = u'Em '+name+u' đã ' + loai + u'.\n Ngày: ' + time + '.'
                    message = message + u'---> ' + str(phone_number) + u': ' + sms_message + u'<br>'
                    if phone_number:
                        sendSMS(phone_number, sms_message, user)
            data = simplejson.dumps({'message':message})
            return HttpResponse(data, mimetype = 'json')
        else:
            raise Exception("StrangeRequestMethod")
        #end if request.is_ajax()
    for p in pupilList:
        try:
            dd = DiemDanh.objects.get(time__exact=time, student_id__exact=p.id, term_id__exact=term.id)
            hs_nghi.append(p)
            stt.append(dd.loai)
        except ObjectDoesNotExist:
            pass
    ds_nghi = zip(hs_nghi,stt)
    t = loader.get_template(os.path.join('school', 'ds_nghi_hoc.html'))
    c = RequestContext(request, {'list':ds_nghi, 'class_id':class_id, 'time':time, 'day':day, 'month':month, 'year':year, 'cl':cl, 'pos':pos,'dncform':dncform})
    return HttpResponse(t.render(c))

def diem_danh_hs(request, student_id, view_type = 0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pos = get_position(request)
    pupil = Pupil.objects.get(id=student_id)
    if pos == 3 and not gvcn(request,pupil.class_id):
        pos = 1
    if pos < 1:
        return HttpResponseRedirect('/')
    term = None
    c = pupil.class_id
    if not in_school(request, c.block_id.school_id):
        return HttpResponseRedirect('/')
    term = get_current_term(request)
    if not term:
        message = None
        t = loader.get_template(os.path.join('school', 'time_select.html'))
        ct = RequestContext(request, {'class_id':c.id, 'message':message})
        return HttpResponse(t.render(ct))
    ddl = DiemDanh.objects.filter(student_id=student_id, term_id=term.id).order_by('time')
    count = ddl.count()
    if pos > 1 and view_type:
        iform = DiemDanhForm()
        form = []
        for dd in ddl:
            form.append(DiemDanhForm(instance=dd))
        if request.method == 'POST':
            list = request.POST.getlist('loai')
            i = 0
            for dd in ddl:
                if list[i] != 'k':
                    data = {'loai':list[i]}
                    form[i] = DiemDanhForm(data, instance=dd)
                    if form[i].is_valid():
                        form[i].save()
                    i += 1
                else:
                    dd.delete()
                    i += 1
            if list[i] != 'k':
                time = to_date(request.POST['time'])
                data = {'student_id':student_id, 'time':time, 'loai':list[i], 'term_id':term.id}
                iform = DiemDanhForm(data)
                if iform.is_valid():
                    iform.save()
                    form.append(iform)
                    iform = DiemDanhForm()
                    url = '/school/diemdanhhs/' + str(student_id)
        ddl = DiemDanh.objects.filter(student_id=student_id, term_id=term.id).order_by('time')
        for dd in ddl:
            form.append(DiemDanhForm(instance=dd))
        ddhs = zip(ddl,form)
        t = loader.get_template(os.path.join('school', 'diem_danh_hs_edit.html'))
        c = RequestContext(request, {   'ddhs':ddhs,
                                        'iform':iform,
                                        'pupil':pupil,
                                        'student_id':student_id,
                                        'term':term,
                                        'pos':pos,
                                        'count':count})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template(os.path.join('school', 'diem_danh_hs.html'))
        c = RequestContext(request, {   'form': ddl,
                                        'pupil':pupil,
                                        'student_id':student_id,
                                        'term':term,
                                        'pos':pos,
                                        'count':count})
        return HttpResponse(t.render(c))

def tk_dd_lop(class_id, term_id):
    ppl = Pupil.objects.filter(class_id=class_id)
    for p in ppl:
        tk_diem_danh(p.id, term_id)

def tk_diem_danh(student_id, term_id):
    pupil = Pupil.objects.get(id=student_id)
    c = pupil.class_id
    ts = DiemDanh.objects.filter(student_id=student_id, term_id=term_id).count()
    cp = DiemDanh.objects.filter(student_id=student_id, term_id=term_id, loai=u'C').count()
    kp = ts - cp
    data = {'student_id':student_id, 'tong_so':ts, 'co_phep':cp, 'khong_phep':kp, 'term_id':term_id}
    tk = TKDiemDanhForm()
    try:

        tkdd = TKDiemDanh.objects.get(student_id__exact=student_id, term_id__exact=term_id)
        tk = TKDiemDanhForm(data, instance=tkdd)
    except ObjectDoesNotExist:
        tk = TKDiemDanhForm(data)
    tk.save()

def test(request):
    form = PupilForm()
    message = 'Hello'
    t = loader.get_template('school/time_select.html')
    c = RequestContext(request, {'form':form, 'message':message})

    return HttpResponse(t.render(c))

def deleteSubject(request, subject_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    try:
        sub = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return HttpResponseRedirect('/')

    class_id = sub.class_id
    if not in_school(request, class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    completely_del_subject(sub)
    url = '/school/subjectPerClass/' + str(class_id.id)
    return HttpResponseRedirect(url)

def deleteTeacher(request, teacher_id, team_id = 0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    message = "Đã xóa xong."
    school = get_school(request)
    try:
        s = Teacher.objects.get(id = teacher_id)
    except Teacher.DoesNotExist:
        return HttpResponseRedirect('/')

    if not in_school(request, s.school_id):
        return HttpResponseRedirect('/school/teachers')
    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    cl = Subject.objects.filter(teacher_id = s.id)
    for sj in cl:
        sj.teacher_id = None
        sj.save()
    cl = Class.objects.filter(teacher_id = s.id)
    for sj in cl:
        sj.teacher_id = None
        sj.save()
        #s.delete()
    del_teacher(s)
    if int(team_id) != 0:
        return HttpResponseRedirect("/school/teachers_in_team/" + team_id)
    return HttpResponseRedirect("/school/teachers_tab")

def deleteClass(request, class_id, block_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    message = "Đã xóa xong."
    try:
        s = get_current_year(request).class_set.get(id=class_id)
    except Class.DoesNotExist:
        return HttpResponseRedirect('/school/classes')
    if not in_school(request, s.block_id.school_id):
        return HttpResponseRedirect('/')
    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    s.delete()
    return HttpResponseRedirect('/school/classtab/'+block_id)

def deleteStudentInClass(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    message = "Đã xóa xong."
    try:
        student = Pupil.objects.get(id=student_id)
    except Pupil.DoesNotExist:
        return HttpResponseRedirect('/')

    class_id = student.class_id
    if not in_school(request, class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    completely_del_student(student)
    return HttpResponseRedirect('/school/viewClassDetail/'+str(class_id.id))

@transaction.commit_manually
def deleteAllStudentsInClass(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    try:
        cl = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return HttpResponseRedirect('/')

    students = cl.pupil_set.all()

    if not in_school(request, cl.block_id.school_id):
        return HttpResponseRedirect('/')
    if get_position(request) < 4:
        return HttpResponseRedirect('/')

    for student in students:
        completely_del_student(student)
    transaction.commit()
    return HttpResponseRedirect('/school/viewClassDetail/'+str(cl.id))

def deleteStudentInSchool(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    #    message = "Đã xóa xong."
    sub = Pupil.objects.get(id=student_id)
    if not in_school(request, sub.class_id.block_id.school_id):

        return HttpResponseRedirect('/')
    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    sub.delete()
    return HttpResponseRedirect ('/school/students')

def khen_thuong(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    sub = Pupil.objects.get(id=student_id)
    if not in_school(request, sub.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,sub.class_id):
        pos = 4
    if get_position(request) < 1:
        return HttpResponseRedirect('/')
    message = ''
    ktl = sub.khenthuong_set.order_by('time')
    count = ktl.count()
    t = loader.get_template(os.path.join('school', 'khen_thuong.html'))
    c = RequestContext(request, {'ktl': ktl, 'message':message, 'student_id':student_id,'pupil':sub, 'pos':pos, 'count':count})
    return HttpResponse(t.render(c))

def add_khen_thuong(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    form = KhenThuongForm(student_id)
    pupil = Pupil.objects.get(id=student_id)
    if not in_school(request, pupil.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    url = "/school/khenthuong/"+str(student_id) + "/add"
    cl = Class.objects.get(id__exact=pupil.class_id.id)
    term = get_current_term(request)
    if request.method == 'POST':
        form = KhenThuongForm(student_id, request.POST)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/khenthuong/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'khen_thuong_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':student_id, 'term':term, 'url':url})
    return HttpResponse(t.render(c))

def delete_khen_thuong(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    kt = KhenThuong.objects.get(id=kt_id)
    student = kt.student_id
    if not in_school(request, student.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    kt.delete()
    url = '/school/khenthuong/' + str(student.id)
    return HttpResponseRedirect(url)

def edit_khen_thuong(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    kt = KhenThuong.objects.get(id=kt_id)
    pupil = kt.student_id
    if not in_school(request, pupil.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    url = "/school/khenthuong/"+str(pupil.id) + "/edit"
    term = kt.term_id
    form = KhenThuongForm(pupil.id,instance=kt)
    if request.method == 'POST':
        form = KhenThuongForm(pupil.id, request.POST, instance=kt)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/viewStudentDetail/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'khen_thuong_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':pupil.id, 'term':term, 'url':url})
    return HttpResponse(t.render(c))

def ki_luat(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    student = Pupil.objects.get(id=student_id)
    if not in_school(request, student.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,student.class_id):
        pos = 4
    if get_position(request) < 1:
        return HttpResponseRedirect('/')
    message = ''
    ktl = student.kiluat_set.order_by('time')
    count = ktl.count()
    t = loader.get_template(os.path.join('school', 'ki_luat.html'))
    c = RequestContext(request, {'ktl': ktl, 'message':message, 'student_id':student_id, 'pupil':student, 'pos':pos, 'count':count})
    return HttpResponse(t.render(c))

def add_ki_luat(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))

    form = KiLuatForm(student_id)
    pupil = Pupil.objects.get(id=student_id)
    if not in_school(request, pupil.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    url = "/school/kiluat/"+str(student_id) + "/add"
    cl = Class.objects.get(id__exact=pupil.class_id.id)
    term = get_current_term(request)
    if request.method == 'POST':
        form = KiLuatForm(student_id,request.POST)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/kiluat/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'ki_luat_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':student_id, 'term':term, 'url':url})
    return HttpResponse(t.render(c))

def delete_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception:
        return HttpResponseRedirect(reverse('index'))

    kt = KiLuat.objects.get(id=kt_id)
    student = kt.student_id
    if not in_school(request, student.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    kt.delete()
    url = '/school/kiluat/' + str(student.id)
    return HttpResponseRedirect(url)

def edit_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    try:
        school = get_school(request)
    except Exception :
        return HttpResponseRedirect(reverse('index'))

    kt = KiLuat.objects.get(id=kt_id)

    pupil = kt.student_id
    if not in_school(request, pupil.class_id.block_id.school_id):
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if pos == 3 and gvcn(request,pupil.class_id):
        pos = 4
    if pos < 4:
        return HttpResponseRedirect('/')
    url = "/school/kiluat/"+str(pupil.id) + "/edit"
    term = kt.term_id
    form = KiLuatForm(pupil.id, instance=kt)
    if request.method == 'POST':
        form = KiLuatForm(pupil.id, request.POST, instance=kt)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/kiluat/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'ki_luat_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':pupil.id, 'term':term, 'url':url})
    return HttpResponse(t.render(c))
#term_number = 1: ki 1. = 2: ki 2, = 3: ca nam.
def hanh_kiem(request, class_id = 0, sort_type = 1, sort_status = 0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    year = get_current_year(request)
    classList = year.class_set.all()
    if class_id == 0:
        for cl in classList:
            return HttpResponseRedirect('/school/hanhkiem/'+str(cl.id))
    c = classList.get(id__exact=class_id)
    if not in_school(request, c.block_id.school_id):
        return HttpResponseRedirect('/')

    pos=get_position(request)
    if pos < 1:
        return HttpResponseRedirect('/')
    if pos == 1:
        if not inClass(request,class_id):
            return HttpResponseRedirect('/')
    if gvcn(request, class_id) == 1:
        pos = 4
    message = None
    pupilList = c.pupil_set.all()
    term = get_current_term(request)
    if int(sort_type) == 1:
        if not int(sort_status):
            pupilList = c.pupil_set.order_by('first_name', 'last_name')
        else:
            pupilList = c.pupil_set.order_by('-first_name', '-last_name')
    if int(sort_type) == 2:
        if not int(sort_status):
            pupilList = c.pupil_set.order_by('birthday')
        else:
            pupilList = c.pupil_set.order_by('-birthday')
    if int(sort_type) == 3:
        if not int(sort_status):
            pupilList = c.pupil_set.order_by('sex')
        else:
            pupilList = c.pupil_set.order_by('-sex')

    #tk_dd_lop(class_id, term.id)
    form = []
    all = []
    i = 0
    for p in pupilList:
        form.append(HanhKiemForm())
        all.append(HanhKiem())
        hk = p.hanhkiem_set.get(year_id__exact=year.id)
        all[i] = hk
        form[i] = HanhKiemForm(instance=hk)
        i += 1

    if request.is_ajax() and request.POST['request_type'] != u'all':
        p_id = request.POST['id']
        p = c.pupil_set.get(id = int(p_id))
        hk = p.hanhkiem_set.get(year_id__exact=year.id)
        data = {}
        if request.POST['request_type'] == u'term1':
            if request.POST['term1'] != u'':
                term1 = request.POST['term1']
            else:
                term1 = None
            data = {'student_id':p_id, 'term1':term1, 'year_id':year.id}


        elif request.POST['request_type'] == u'term2':
            if request.POST['term2'] != u'':
                term2 = request.POST['term2']
            else:
                term2 = None
            data = {'student_id':p_id, 'term1':hk.term1, 'term2':term2, 'year_id':year.id}

        elif request.POST['request_type'] == u'year':
            if request.POST['year'] != u'':
                y = request.POST['year']
            else:
                y = None
            data = {'student_id':p_id, 'term1':hk.term1, 'term2': hk.term2, 'year':y, 'year_id':year.id}

        form = HanhKiemForm(data, instance=hk)
        if form.is_valid():
            form.save()

    elif request.is_ajax() and request.POST['request_type']=='all':
        message = 'Cập nhật thành công hạnh kiểm lớp ' + str(Class.objects.get(id=class_id))
        term1 = request.POST.getlist('term1')
        term2 = request.POST.getlist('term2')
        y = request.POST.getlist('year')
        i = 0
        for p in pupilList:
            hk = p.hanhkiem_set.get(year_id__exact=year.id)
            if term.number == 1:
                data = {'student_id':p.id, 'term1':term1[i], 'year_id':year.id}
            else:
                data = {'student_id':p.id, 'term1':hk.term1, 'term2':term2[i], 'year':y[i], 'year_id':year.id}
            form[i] = HanhKiemForm(data, instance=hk)
            form[i].save()
            i += 1
    listdh = zip(pupilList, form, all)
    t = loader.get_template(os.path.join('school', 'hanh_kiem.html'))
    c = RequestContext(request, {   'form':form,
                                    'message':message,
                                    'class':c,
                                    'list':listdh,
                                    'sort_type':sort_type,
                                    'sort_status':sort_status,
                                    'next_status':1-int(sort_status),
                                    'year' : year,
                                    'term' : term,
                                    'classList':classList,
                                    'pos':pos})
    return HttpResponse(t.render(c))

def viewSubjectDetail (request, subject_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception :
        return HttpResponseRedirect(reverse('index'))

    if get_position(request) < 4:
        return HttpResponseRedirect('/')
    sub = Subject.objects.get(id=subject_id)
    class_id = sub.class_id
    if not in_school(request, class_id.block_id.school_id):
        return HttpResponseRedirect('/')

    form = SubjectForm (class_id.block_id.school_id.id, instance = sub)
    message = None
    if request.method == 'POST':
        data = request.POST.copy()
        data['name'] = data['name'].strip()
        form = SubjectForm(class_id.block_id.school_id.id, data, instance = sub)
        if form.is_valid():
            form.save()
            message = 'Bạn đã cập nhật thành công'

    t = loader.get_template(os.path.join('school', 'subject_detail.html'))
    c = RequestContext(request, {   'form':form,
                                    'message':message,
                                    'sub': sub,
                                    })
    return HttpResponse(t.render(c))
