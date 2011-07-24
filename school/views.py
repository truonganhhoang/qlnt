# -*- coding: utf-8 -*-

# Create your views here.
import os.path
import datetime
from django.core.paginator import *
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
from school.forms import *
from school.school_settings import *
from sms.views import *
import xlrd

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
    
    if school.status == 0:
        return HttpResponseRedirect(reverse('setup'))
    
    year = get_current_year(request)
    request.session['year'] = year
    context = RequestContext(request)
    return render_to_response(SCHOOL, context_instance=context)

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
                message, labels, success = phase_class_label(request, school)
                data = simplejson.dumps( {'message': message, 'status': success})
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
    message, labels, success = phase_class_label(request, school)
        
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
        form = SchoolForm(request.POST, request = request)
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

def phase_class_label(request, school):
    class_labels = []
    message = None
    if 'message' in request.session:
        message = request.session['message']
    for loai in school.danhsachloailop_set.order_by('loai'):
        class_labels.append(loai.loai)
    
    labels = ','.join(class_labels)
    labels = 'Nhanh: ' + labels
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
                for label in list_labels:
                    if label:
                        label = label.strip()
                        find = school.danhsachloailop_set.filter( loai__exact = label )
                        if not find:
                            lb = DanhSachLoaiLop()
                            lb.loai = label
                            lb.school_id = school
                            lb.save()
                message = u'Bạn vừa thiết lập thành công danh sách tên lớp cho trường.'
                success = True
            labels = 'Nhanh: '+ labels
        else:
            if ',' in labels:
                list_labels = labels.split(',')
                # draft version
                if len(list_labels) == 0:
                    message = u'Bạn cần nhập ít nhất một tên lớp'
                    success = False
                else:
                    ds = school.danhsachloailop_set.all()
                    for d in ds:
                        d.delete()
                    for label in list_labels:
                        label = label.strip()
                        if label:
                            try:
                                label = label.split(' ')[1]
                                find = school.danhsachloailop_set.filter( loai__exact = label )
                                if not find:
                                    lb = DanhSachLoaiLop()
                                    lb.loai = label
                                    lb.school_id = school
                                    lb.save()
                            except Exception as e:
                                message = u'Các tên lớp phải được cung cấp theo dạng [khối][dấu cách][tên lớp]. Ví dụ: 10 A'
                                success = False
                                return message, labels, success     
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
    message, labels, success = phase_class_label(request, school)
    
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
        for khoi in range(lower_bound, upper_bound + 1):
            block = school.block_set.filter(number__exact=khoi)
            if block:
                block = block[0]
            else:
                raise Exception(u'Khối' + str(khoi) + u'chưa đc tạo')
                
            loai_lop = school.danhsachloailop_set.all()
            for class_name in loai_lop:
                _class = Class()
                _class.name = str(block.number) + ' ' + class_name.loai
                _class.status = 1
                _class.block_id = block
                _class.year_id = year
                _class.save()
                for mon in ds_mon_hoc:
                    add_subject( mon, 1, None, _class)
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
                            if (student.tbnam_set.get(year_id=last_year).len_lop):
                                new_block = year.block_set.get(number=block.number + 1)
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

#----------- Exporting and Importing form Excel -------------------------------------

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
    if task == "Nhap danh sach trung tuyen":
        student_list = []
        filepath = os.path.join(TEMP_FILE_LOCATION, file_name)
        if not os.path.isfile(filepath):
            raise NameError, "%s is not a valid filename" % file_name
        try:
            book = xlrd.open_workbook(filepath)
            sheet = book.sheet_by_index(0)
        except Exception as e:
            return {'error': u'File tải lên không phải file Excel'}
        
        start_row = -1
        for c in range(0, sheet.ncols):
            flag = False
            for r in range(0, sheet.nrows):
                if (sheet.cell_value(r, c) == u'Tên'):
                    start_row = r
                    flag = True
                    break
            if flag: break
        #                                                             CHUA BIEN LUAN TRUONG HOP: start_row = -1, ko co cot ten: Mã học sinh
        # start_row != 0
        c_ten = -1
        c_ngay_sinh = -1
        c_tong_diem = -1
        c_nguyen_vong = -1
        for c in range(0, sheet.ncols):
            value = sheet.cell_value(start_row, c)
            if (value == u'Tên'):
                c_ten = c
            elif (value == u'Ngày sinh'):
                c_ngay_sinh = c
            elif (value == u'Tổng điểm'):
                c_tong_diem = c
            elif (value == u'Nguyện vọng'):
                c_nguyen_vong = c
        
        for r in range(start_row + 1, sheet.nrows):
            name = sheet.cell_value(r, c_ten)
            birthday = sheet.cell(r, c_ngay_sinh).value
            nv = sheet.cell_value( r, c_nguyen_vong)
            tong_diem = sheet.cell_value( r, c_tong_diem)
            if ( name == "" or birthday =="" ):
                continue
            if nv.strip() == "": nv = "CB"
            if str(tong_diem).strip()=="": tong_diem = "0"
            date_value = xlrd.xldate_as_tuple(sheet.cell(r, c_ngay_sinh).value, book.datemode)
            birthday = date(*date_value[:3])
            student_list.append({'ten': name, \
                                'ngay_sinh': birthday, \
                                'nguyen_vong': nv, \
                                'tong_diem': tong_diem,})
        return student_list
    else: task == ""
    
    return None
    
def save_upload( uploaded, filename, raw_data ):
    ''' 
    raw_data: if True, uploaded is an HttpRequest object with the file being
              the raw post data 
              if False, uploaded has been submitted via the basic form
              submission and is a regular Django UploadedFile in request.FILES
    '''
    try:
        from io import FileIO, BufferedWriter
        with BufferedWriter( FileIO( filename, "wb" ) ) as dest:
        # if the "advanced" upload, read directly from the HTTP request 
        # with the Django 1.3 functionality
            if raw_data:
                foo = uploaded.read( 1024 )
                while foo:
                    dest.write( foo )
                    foo = uploaded.read( 1024 ) 
         # if not raw, it was a form upload so read in the normal Django chunks fashion
            else:
                for c in uploaded.chunks( ):
                    dest.write( c )
            # got through saving the upload, report success
            return True
    except IOError:
        # could not open the file most likely
        pass
    return False

def student_import( request, class_id ):
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    permission = get_permission(request)
    if not permission in [u'HIEU_TRUONG',u'HIEU_PHO']:
        return HttpResponseRedirect(reverse('school_index'))
        
    if request.method == "POST":    
        if request.is_ajax( ):
            # the file is stored raw in the request
            upload = request
            is_raw = True
            # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
            try:
                filename = '_'.join([request.session.session_key, request.GET[ 'qqfile' ]])
                filename = os.path.join( TEMP_FILE_LOCATION, filename)
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
    success = save_upload( upload, filename, is_raw )
    message = None
    result = process_file( filename, "Nhap danh sach trung tuyen")
    if 'error' in result:
        success = False
        message = result['error']
    else:
        chosen_class = Class.objects.get( id = int(class_id) )
        year = school.startyear_set.get(time=datetime.date.today().year)
        current_year = school.year_set.latest('time')
        term = get_current_term( request)
        try:
            c = datetime.datetime.now()
            add_many_students(student_list = result, _class = chosen_class, 
                              start_year = year, year = current_year,
                              term = term, school=school)
            '''
            for student in result:
                data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                        'ban':student['nguyen_vong'], }
                add_student(student=data, _class=chosen_class,
                            start_year=year, year=current_year,
                            term=term, school=school)
            '''
            a = datetime.datetime.now()
            
        except Exception as e:
            message = u'Lỗi trong quá trình lưu cơ sở dữ liệu'
    # let Ajax Upload know whether we saved it or not
    data = { 'success': success, 'message': message }
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
    _class_list = [(u'0', u'---')]
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
                student_list = process_file(file_name=save_file_name, \
                                            task="Nhap danh sach trung tuyen")
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
    
    _class_list = [(u'0', u'---')]
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
            else:
                chosen_class = None
            if request.POST['clickedButton'] == 'save':
                year = school.startyear_set.get(time=datetime.date.today().year)
                today = datetime.date.today()   
                for student in student_list:
                    data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                        'ban':student['nguyen_vong'], }
                    
                    add_student(student=data, _class=chosen_class,
                                start_year=year, year=this_year,
                                term=term, school=school)
                    
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
    if chosen_class != u'0':
        chosen_class = school.year_set.latest('time').class_set.get(id=chosen_class)
    else:
        chosen_class = None
    message = None
   
    if request.method == 'POST':
        if request.POST['clickedButton'] == 'save':
            year = school.startyear_set.get(time=datetime.date.today().year)
            today = datetime.date.today()   
            for student in student_list:
                data = {'full_name': student['ten'], 'birthday':student['ngay_sinh'],
                    'ban':student['nguyen_vong'], }
                
                add_student(student=data, _class=chosen_class,
                            start_year=year, year=current_year,

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
                                      
def classes(request, sort_type=1, sort_status=0, page=1):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    pos = get_position(request)
    if (pos == 1):
        url = '/school/viewClassDetail/' + str(get_student(request).class_id.id)
        return HttpResponseRedirect(url)
    message = None
    school_id = get_school(request).id
    form = ClassForm(school_id)
    cyear = get_current_year(request)
    if int(sort_type) == 1:
        if int(sort_status) == 0:
            class_List = cyear.class_set.order_by('name')
        else:
            class_List = cyear.class_set.order_by('-name')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            class_List = cyear.class_set.order_by('block_id__number')
        else:
            class_List = cyear.class_set.order_by('-block_id__number')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
            class_List = cyear.class_set.order_by('teacher_id__first_name')
        else:
            class_List = cyear.class_set.order_by('-teacher_id__first_name')
    if int(sort_type) == 4:
        if int(sort_status) == 0:
            class_List = cyear.class_set.order_by('year_id__time')
        else:
            class_List = cyear.class_set.order_by('-year_id__time')
    paginator = Paginator(class_List, 20)
    try:
        classList = paginator.page(page)
    except (EmptyPage, InvalidPage):
        classList = paginator.page(paginator.num_pages)
    cfl = []
    for c in classList.object_list:
        cfl.append(ClassForm(school_id, instance=c))
	list = zip(classList.object_list, cfl)
    if request.method == 'POST':
        teacher_list = request.POST.getlist('teacher_id')
        i = 0
        for c in classList.object_list:
            data = {'name':c.name, 'year_id':c.year_id.id, 'block_id':c.block_id.id, 'teacher_id':teacher_list[i]}
            of = cfl[i]
            cfl[i] = ClassForm(school_id, data, instance=c)
            if str(of) != str(cfl[i]): 
                if cfl[i].is_valid():
                    cfl[i].save()
                message = 'Thông tin lớp đã được cập nhật.'
            i = i + 1
        cfl.append(ClassForm(school_id, instance=c))		
    list = zip(classList.object_list, cfl)
    t = loader.get_template(os.path.join('school', 'classes.html'))
    c = RequestContext(request, {   'list': list, 
                                    'form': form, 
                                    'message': message, 
                                    'classList': classList, 
                                    'sort_type':sort_type, 
                                    'sort_status':sort_status, 
                                    'next_status':1-int(sort_status), 
                                    'base_order': (int(page)-1) * 20,
                                    'pos':pos,})
    return HttpResponse(t.render(c))


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
    
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    school = user.userprofile.organization
    if school.status != 0:
        form = ClassForm(school.id)
        if request.method == 'POST':
            data = {'name':request.POST['name'], 'year_id':request.POST['year_id'], 'block_id':request.POST['block_id'], 'teacher_id':request.POST['teacher_id'], 'status':school.status,}
            form = ClassForm(school.id,data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/school/classes')
        
        t = loader.get_template(os.path.join('school', 'add_class.html'))
        c = RequestContext(request, {'form': form})
        return HttpResponse(t.render(c))
    else:    
        t = loader.get_template(os.path.join('school', 'add_class.html'))
        c = RequestContext(request)
        return HttpResponse(t.render(c))
		
#User: loi.luuthe@gmail.com
#This function has class_id is an int argument. It gets the information of the class corresponding to the class_id and response to the template
def viewClassDetail(request, class_id, sort_type=1, sort_status=0, page=1):
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
    try:
        cl = Class.objects.get(id=class_id)    
    except Class.DoesNotExist:
        return HttpResponseRedirect('/school/classes')
    cn=gvcn(request, class_id)
    inCl=inClass(request, class_id)
    if in_school(request, cl.block_id.school_id) == False:
        return HttpResponseRedirect('/')   
    message = None
    school = cl.block_id.school_id
    cyear = get_current_year(request)
    classList = cyear.class_set.all()
    form = PupilForm(school.id)
    		
    if request.method == 'POST':
        if (request.is_ajax()):
            data = request.POST[u'data']
            data = data.split('-')
            for e in data:
                std = Pupil.objects.get(id = int(e))
                completely_del_student(std)
                url = '/school/viewClassDetail/' + str(class_id)
                return HttpResponseRedirect(url)
        else:        
            if (request.POST['first_name']):
                name = request.POST['first_name'].split()
                last_name = ' '.join(name[:len(name)-1])
                first_name = name[len(name)-1]
            else:
                last_name = ''
                first_name = ''
            if (int(request.POST['birthday_year']) and int(request.POST['birthday_month']) and int(request.POST['birthday_day'])):
                try :
                    birthday = date(int(request.POST['birthday_year']), int(request.POST['birthday_month']), int(request.POST['birthday_day']))
                except ValueError:
                    birthday = None
            else:
                birthday = None
                
            if (request.POST['school_join_date_year'] and request.POST['school_join_date_month'] and request.POST['school_join_date_day']):
                try:
                    school_join_date = date(int(request.POST['school_join_date_year']), int(request.POST['school_join_date_month']), int(request.POST['school_join_date_day']))
                except ValueError:
                    school_join_date=None
            else:
                school_join_date = None
            data = {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'class_id':class_id, 'sex':request.POST['sex'], 'ban_dk':request.POST['ban_dk'], 'school_join_date':school_join_date, 'start_year_id':request.POST['start_year_id']}
            form = PupilForm(school.id, data)
            if form.is_valid():
                data['ban'] = data['ban_dk']
                _class = Class.objects.get(id=class_id)
                start_year = StartYear.objects.get(id=int(data['start_year_id']))
                add_student(student=data, start_year=start_year, year=get_current_year(request), _class=_class, term=get_current_term(request), school=get_school(request), school_join_date=school_join_date)
                message = 'Bạn vừa thêm một học sinh mới'
                form = PupilForm(school.id)
            else:
                if data['first_name'] != '':
                    data['first_name']=data['last_name'] + ' ' + data['first_name']
                    form=PupilForm(school.id, data)
                    
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
    paginator = Paginator (studentList, 20)
    try:
        student_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        student_list = paginator.page(paginator.num_pages)
    tmp = get_student(request)
    id = 0
    if (tmp):
        id = tmp.id
    
    currentTerm= get_current_term(request)    
    t = loader.get_template(os.path.join('school', 'classDetail.html'))
    c = RequestContext(request, {   'form': form,
                                    'csrf_token': get_token(request), 
                                    'message': message, 
                                    'studentList': student_list, 
                                    'class': cl, 
                                    'cl':classList,
                                    'sort_type':int(sort_type), 
                                    'sort_status':int(sort_status), 
                                    'next_status':1-int(sort_status), 
                                    'base_order': (int(page)-1) * 20,
                                    'pos': pos,
                                    'gvcn':cn,
                                    'student_id':id,
                                    'currentTerm':currentTerm,                                    
                                    })
    return HttpResponse(t.render(c))

#sort_type = '1': fullname, '2': birthday, '3':'sex'
#sort_status = '0':ac '1':'dec

def teachers(request, sort_type=1, sort_status=0, page=1):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    pos = get_position(request)
    message = None
    form = TeacherForm()
    school = get_school(request)
    #print sort_type +' ' + sort_status
    if request.method == 'POST':
        if (request.POST['first_name'].strip()):
            name = request.POST['first_name'].split()
            last_name = ' '.join(name[:len(name)-1])
            first_name = name[len(name)-1]
        else:
            last_name = ''
            first_name = ''

        if (int(request.POST['birthday_year']) and int(request.POST['birthday_month']) and int(request.POST['birthday_day'])):
            try :
                birthday = date(int(request.POST['birthday_year']), int(request.POST['birthday_month']), int(request.POST['birthday_day']))
            except ValueError:
                birthday = None
        else:
            birthday = None
        data = {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'sex':request.POST['sex'], 'school_id':school.id, 'birth_place':request.POST['birth_place'].strip()}
        form = TeacherForm(data)
        if form.is_valid():
            add_teacher(first_name=data['first_name'], last_name=data['last_name'], school=get_school(request), birthday=birthday, sex=data['sex'], birthplace=data['birth_place'])
            message = 'Bạn vừa thêm một giáo viên mới'
            form = TeacherForm()
        else:
            if data['first_name'] != '':
                data['first_name'] = data['last_name'] + ' ' + data['first_name']
                form = TeacherForm(data)
            
			
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
    paginator = Paginator (teacherList, 20)
    try:
        teacher_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        teacher_list = paginator.page(paginator.num_pages)

    t = loader.get_template(os.path.join('school', 'teachers.html'))
    tmp = get_teacher(request)
    id = 0
    if (tmp):
        id = tmp.id
    c = RequestContext(request, {   'form': form,
                                    'message': message,
                                    'teacherList': teacher_list,
                                    'sort_type':sort_type, 
                                    'sort_status':sort_status, 
                                    'next_status':1-int(sort_status), 
                                    'base_order':(int (page)-1) * 20,
                                    'pos':pos,
                                    'teacher_id':id})
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
    if (pos==3) and (get_teacher(request).id == int(teacher_id)):
        pos = 4
    if (pos < 1):
        return HttpResponseRedirect('/')
    form = TeacherForm (instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            message = 'Bạn vừa cập nhật thành công'        
            
    
    t = loader.get_template(os.path.join('school', 'teacher_detail.html'))
    c = RequestContext(request, {   'form': form, 'message': message,
                                    'id': teacher_id,
                                    'pos': pos})
    return HttpResponse(t.render(c))

def subjectPerClass(request, class_id, sort_type=1, sort_status=0):
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
    school_id = cl.block_id.school_id.id
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
    form = SubjectForm(school_id)
    sfl = []
    for s in subjectList:
        sfl.append(SubjectForm(school_id, instance=s))
    list = zip(subjectList, sfl)
    if request.method == 'POST':
        hs_list = request.POST.getlist('hs')
        teacher_list = request.POST.getlist('teacher_id')
        i = 0
        for s in subjectList:
            data = {'name':s.name, 'hs':hs_list[i], 'class_id':class_id, 'teacher_id':teacher_list[i]}
            of = sfl[i]
            sfl[i] = SubjectForm(school_id, data, instance=s)
            if str(of) != str(sfl[i]):
                if sfl[i].is_valid():
                    sfl[i].save()
                    message = 'Danh sách môn học đã được cập nhật.'
            i = i + 1
        if teacher_list[i] != u'' or request.POST['name'] != u'' or hs_list[i] != u'':
            data = {'name':request.POST['name'], 'hs':hs_list[i], 'class_id':class_id, 'teacher_id':teacher_list[i]}
            form = SubjectForm(school_id, data)
            if form.is_valid():
                _class = Class.objects.get(id=class_id)
                if teacher_list[i] != u'':
                    teacher = Teacher.objects.get(id=int(data['teacher_id']))
                    add_subject(subject_name=data['name'], hs=float(data['hs']), teacher=teacher, _class=_class, term=term)
                    form = SubjectForm(school_id)
                else:
                    add_subject(subject_name=data['name'], hs=float(data['hs']), teacher=None, _class=_class, term=term)
                    form = SubjectForm(school_id)
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
    sfl = []
    year = get_current_year(request)
    classList = year.class_set.all()
    for s in subjectList:
        sfl.append(SubjectForm(school_id, instance=s))
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

def students(request, sort_type=1, sort_status=1, page=1):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    message = None
    school = get_school(request)
    form = PupilForm(school.id)
    
    if request.method == 'POST':
        #print request.POST
        if (request.POST['first_name']):
            name = request.POST['first_name'].split()
            last_name = ' '.join(name[:len(name)-1])
            first_name = name[len(name)-1]
        else:
            last_name = None
            first_name = None
        if (int(request.POST['birthday_year']) and int(request.POST['birthday_month']) and int(request.POST['birthday_day'])):
            birthday = date(int(request.POST['birthday_year']), int(request.POST['birthday_month']), int(request.POST['birthday_day']))
        else:
            birthday = None
        if (request.POST['school_join_date_year'] and request.POST['school_join_date_month'] and request.POST['school_join_date_day']):
            school_join_date = date(int(request.POST['school_join_date_year']), int(request.POST['school_join_date_month']), int(request.POST['school_join_date_day']))
        data = {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'sex':request.POST['sex'], 'ban_dk':request.POST['ban_dk'], 'school_join_date':school_join_date, 'start_year_id':request.POST['start_year_id'], 'class_id': request.POST['class_id']}
        #print request.POST['start_year_id']
        form = PupilForm(school.id, data)
        if form.is_valid():
            start_year = StartYear.objects.get(id=int(data['start_year_id']))
            _class = Class.objects.get(id=data['class_id'])
            data['ban'] = data['ban_dk']
            add_student(student=data, start_year=start_year, year=get_current_year(request), _class=_class, term=get_current_term(request), school=get_school(request), school_join_date=school_join_date)
            message = 'Bạn vừa thêm một học sinh mới'

            form = PupilForm(school.id)
        else:
            data['first_name'] = data['last_name'] + ' ' + data['first_name']
            form = PupilForm(school.id, data)
            
	
    if int(sort_type) == 1:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('first_name', 'last_name')
        else:
            studentList = school.pupil_set.order_by('-first_name', '-last_name')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('birthday')
        else:
            studentList = school.pupil_set.order_by('-birthday')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('sex')
        else:
            studentList = school.pupil_set.order_by('-sex')
    if int(sort_type) == 4:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('ban_dk')
        else:
            studentList = school.pupil_set.order_by('-ban_dk')
    if int(sort_type) == 5:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('school_join_date')
        else:
            studentList = school.pupil_set.order_by('-school_join_date')
	
    if int(sort_type) == 6:
        if int(sort_status) == 0:
            studentList = school.pupil_set.order_by('class_id__name')
        else:
            studentList = school.pupil_set.order_by('-class_id__name')
    paginator = Paginator (studentList, 20)
    try:
        student_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        student_list = paginator.page(paginator.num_pages)
		
    t = loader.get_template(os.path.join('school', 'students.html'))
    c = RequestContext(request, {'form': form, 'message': message, 'studentList': student_list, 'sort_type':sort_type, 'sort_status':sort_status, 'next_status':1-int(sort_status), 'base_order': (int(page)-1) * 20})
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
    if (pos==1) and (get_student(request).id==int(student_id)):
        pos = 4
    if (get_position(request) < 1):
        return HttpResponseRedirect('/')
    message = None
    pupil = Pupil.objects.get(id=student_id)
    school_id = pupil.school_id.id
    if in_school(request, pupil.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    form = PupilForm (school_id, instance=pupil)
    if request.method == 'POST':
        data = request.POST.copy()
        data.appendlist('school_id', school_id)
        form = PupilForm(school_id, data, instance=pupil)
        if form.is_valid():
            form.save()
            message = 'Bạn đã cập nhật thành công'        
            

    t = loader.get_template(os.path.join('school', 'student_detail.html'))
    c = RequestContext(request, {   'form': form, 
                                    'message': message, 
                                    'id': student_id,
                                    'class_id':pupil.class_id.id,
                                    'pos':pos
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
    if in_school(request, cl.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    url = '/school/dsnghi/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
    if (get_position(request) < 3):
        return HttpResponseRedirect(url)
    message = ''
    listdh = None
    term = None
    dncdata = {'date':date(int(year),int(month),int(day)),'class_id':class_id}
    year_id = get_current_year(request).id
    dncform = DateAndClassForm(year_id,dncdata)

    if request.method == 'POST':
        try:
            if (request.POST[u'date_day'] or request.POST[u'date_month'] or request.POST[u'date_year'] or request.POST[u'class_id']):
                dncform = DateAndClassForm(year_id,request.POST)
                if dncform.is_valid():
                    class_id = int(request.POST[u'class_id'])
                    day = int(request.POST[u'date_day'])
                    month = int(request.POST[u'date_month'])
                    year = int(request.POST[u'date_year'])
                    url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
                    return HttpResponseRedirect(url)
        except MultiValueDictKeyError:
            pass
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
                        print 11
                        diemdanh.loai = loai
                        diemdanh.save()
                
                message = student.full_name() + ': updated.'
                data = simplejson.dumps({'message': message})
                return HttpResponse( data, mimetype = 'json')    
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
                    message = message + u'---> ' + str(phone_number) + u': ' + sms_message + u'<br>'
                    if phone_number:
                        sendSMS(phone_number, sms_message, user)
            data = simplejson.dumps({'message':message})
            return HttpResponse(data, mimetype = 'json')
        else:
            raise Exception('StrangeRequestMethod')
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name')
    time = date(int(year), int(month), int(day))
    term = get_current_term(request)
    form = []
    for p in pupilList:
        try:
            dd = DiemDanh.objects.get(time__exact=time, student_id__exact=p.id, term_id__exact=term.id)
            form.append(DiemDanhForm(instance=dd))
        except ObjectDoesNotExist:
            form.append(DiemDanhForm())
    listdh = zip(pupilList, form)
    try:
        if request.method == 'POST':
            message = 'Điểm danh lớp ' + str(Class.objects.get(id=class_id)) + '. Ngày ' + str(time) + "đã xong."
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
                    i = i + 1
                except ObjectDoesNotExist:
                    if list[i] != 'k':
                        data = {'student_id':p.id, 'time':time, 'loai':list[i], 'term_id':term.id}
                        form[i] = DiemDanhForm(data)
                        if form[i].is_valid():
                            form[i].save()
                    i = i + 1
    except IndexError:
        message = None
    listdh = zip(pupilList, form)
    t = loader.get_template(os.path.join('school', 'diem_danh.html'))
    c = RequestContext(request, {'dncform':dncform, 'form':form, 'pupilList': pupilList, 'time': time, 'message':message, 'class_id':class_id, 'time':time, 'list':listdh,
                       'day':day, 'month':month, 'year':year, 'cl':cl})
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
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            day = int(request.POST['date_day'])
            month = int(request.POST['date_month'])
            year = int(request.POST['date_year'])
            url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'time_select.html'))
    c = RequestContext(request, {'form':form, 'class_id':class_id, 'message':message})
    return HttpResponse(t.render(c))

def tnc_select(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    year_id = get_current_year(request).id
    pos = get_position(request)
    if (pos < 2):
        return HttpResponseRedirect('/')
    message = 'Hãy chọn ngày và lớp học bạn muốn điểm danh'
    form = DateAndClassForm(year_id)
    if request.method == 'POST':
        form = DateAndClassForm(year_id,request.POST)
        if form.is_valid():
            class_id = str(request.POST['class_id'])
            day = str(request.POST['date_day'])
            month = str(request.POST['date_month'])
            year = str(request.POST['date_year'])
            url = '/school/diemdanh/' + str(class_id) + '/' + str(day) + '/' + str(month) + '/' + str(year)
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
    cl  = Class.objects.get(id=class_id)
    pupilList = Pupil.objects.filter(class_id=class_id).order_by('first_name', 'last_name')
    time = date(int(year), int(month), int(day))
    term = get_current_term(request)
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
    c = RequestContext(request, {'list':ds_nghi, 'class_id':class_id, 'time':time, 'day':day, 'month':month, 'year':year, 'cl':cl, 'pos':pos})
    return HttpResponse(t.render(c))
    
def diem_danh_hs(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pos = get_position(request)
    if (pos < 1):
        return HttpResponseRedirect('/')
    term = None
    pupil = Pupil.objects.get(id=student_id)
    c = pupil.class_id
    if in_school(request, c.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    term = get_current_term(request)
    if term == None:
        message = None
        t = loader.get_template(os.path.join('school', 'time_select.html'))
        ct = RequestContext(request, {'class_id':c.id, 'message':message})
        return HttpResponse(t.render(ct))
    ddl = DiemDanh.objects.filter(student_id=student_id, term_id=term.id).order_by('time')
    if (pos > 1):
        form = []
        iform = DiemDanhForm()
        for dd in ddl:
            form.append(DiemDanhForm(instance=dd))
        if request.method == 'POST':
            list = request.POST.getlist('loai')
            time_day = request.POST.getlist('time_day')
            time_month = request.POST.getlist('time_month')
            time_year = request.POST.getlist('time_year')
            i = 0
            for dd in ddl:
                if list[i] != 'k':
                    time = date(int(time_year[i]), int(time_month[i]), int(time_day[i]))
                    data = {'student_id':student_id, 'time':time, 'loai':list[i], 'term_id':term.id}
                    form[i] = DiemDanhForm(data, instance=dd)
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
                time = date(int(time_year[i]), int(time_month[i]), int(time_day[i]))
                data = {'student_id':student_id, 'time':time, 'loai':list[i], 'term_id':term.id}
                iform = DiemDanhForm(data)
                if iform.is_valid():
                    iform.save()
                    form.append(iform)
                    iform = DiemDanhForm  
        t = loader.get_template(os.path.join('school', 'diem_danh_hs.html'))
        c = RequestContext(request, {   'form': form, 
                                        'iform': iform, 
                                        'pupil':pupil, 
                                        'student_id':student_id, 
                                        'term':term,
                                        'pos':pos})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template(os.path.join('school', 'diem_danh_hs.html'))
        c = RequestContext(request, {   'form': ddl,  
                                        'pupil':pupil, 
                                        'student_id':student_id, 
                                        'term':term,
                                        'pos':pos})
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
    
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    try:
        sub = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return HttpResponseRedirect('/')
        
    class_id = sub.class_id    
    if in_school(request, class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    completely_del_subject(sub)
    url = '/school/subjectPerClass/' + str(class_id.id)
    return HttpResponseRedirect(url)

def deleteTeacher(request, teacher_id):
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
    
    if in_school(request, s.school_id) == False:
        return HttpResponseRedirect('/school/teachers')
    if (get_position(request) < 4):
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
    return HttpResponseRedirect('/school/teachers')

def deleteClass(request, class_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    message = "Đã xóa xong."
    try:
        s = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return HttpResponseRedirect('/school/classes')
    
    if in_school(request, s.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    s.delete()
    return HttpResponseRedirect('/school/classes')

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
    if in_school(request, class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
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
    
    if in_school(request, cl.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
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
    if in_school(request, sub.class_id.block_id.school_id) == False:

        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
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
    if in_school(request, sub.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if (get_position(request) < 1):
        return HttpResponseRedirect('/')
    message = ''
    ktl = KhenThuong.objects.filter(student_id=student_id).order_by('time')
    t = loader.get_template(os.path.join('school', 'khen_thuong.html'))
    c = RequestContext(request, {'ktl': ktl, 'message':message, 'student_id':student_id,'pupil':sub, 'pos':pos})
    return HttpResponse(t.render(c))
    
def add_khen_thuong(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    form = KhenThuongForm()
    pupil = Pupil.objects.get(id=student_id)
    if in_school(request, pupil.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    cl = Class.objects.get(id__exact=pupil.class_id.id)
    term = get_current_term(request)
    if request.method == 'POST':
        form = KhenThuongForm(request.POST)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/khenthuong/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'khen_thuong_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':student_id, 'term':term})
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
    if in_school(request, student.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
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
    if in_school(request, pupil.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    term = kt.term_id
    form = KhenThuongForm(instance=kt)
    if request.method == 'POST':
        form = KhenThuongForm(request.POST, instance=kt)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/khenthuong/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'khen_thuong_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':pupil.id, 'term':term})
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
    if in_school(request, student.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    pos = get_position(request)
    if (get_position(request) < 1):
        return HttpResponseRedirect('/')
    message = ''
    ktl = KiLuat.objects.filter(student_id=student_id).order_by('time')
    t = loader.get_template(os.path.join('school', 'ki_luat.html'))
    c = RequestContext(request, {'ktl': ktl, 'message':message, 'student_id':student_id, 'pupil':student, 'pos':pos})
    return HttpResponse(t.render(c))
    
def add_ki_luat(request, student_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    form = KiLuatForm()
    pupil = Pupil.objects.get(id=student_id)
    if in_school(request, pupil.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 2):
        return HttpResponseRedirect('/')
    cl = Class.objects.get(id__exact=pupil.class_id.id)
    term = get_current_term(request)
    if request.method == 'POST':
        form = KiLuatForm(request.POST)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/kiluat/' + str(student_id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'ki_luat_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':student_id, 'term':term})
    return HttpResponse(t.render(c))

def delete_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
        
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    kt = KiLuat.objects.get(id=kt_id)
    student = kt.student_id
    if in_school(request, student.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    kt.delete()
    url = '/school/khenthuong/' + str(student.id)
    return HttpResponseRedirect(url)

def edit_ki_luat(request, kt_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    kt = KiLuat.objects.get(id=kt_id)

    pupil = kt.student_id
    if in_school(request, pupil.class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    term = kt.term_id
    form = KiLuatForm(instance=kt)
    if request.method == 'POST':
        form = KiLuatForm(request.POST, instance=kt)
        if form.is_valid():
            kt = form.save(commit = False)
            kt.student_id = pupil
            kt.term_id = term
            kt.save()
            url = '/school/khenthuong/' + str(pupil.id)
            return HttpResponseRedirect(url)
    t = loader.get_template(os.path.join('school', 'ki_luat_detail.html'))
    c = RequestContext(request, {'form': form, 'p': pupil, 'student_id':pupil.id, 'term':term})
    return HttpResponse(t.render(c))    
#term_number = 1: ki 1. = 2: ki 2, = 3: ca nam.
def hanh_kiem(request, class_id, sort_type = 1, sort_status = 0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        school = get_school(request)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    c = Class.objects.get(id__exact=class_id)
    if in_school(request, c.block_id.school_id) == False:
        return HttpResponseRedirect('/')           
    
    pos=get_position(request)
    if (pos < 1):
        return HttpResponseRedirect('/')
    if (gvcn(request, class_id) == 1):
        pos = 4
    message = None
    listdh = None    
    pupilList = c.pupil_set.all()
    year = get_current_year(request)
    term = get_current_term(request)
    if int(sort_type) == 1:
        if int(sort_status) == 0:
            pupilList = c.pupil_set.order_by('first_name', 'last_name')
        else:
            pupilList = c.pupil_set.order_by('-first_name', '-last_name')
    if int(sort_type) == 2:
        if int(sort_status) == 0:
            pupilList = c.pupil_set.order_by('birthday')
        else:
            pupilList = c.pupil_set.order_by('-birthday')
    if int(sort_type) == 3:
        if int(sort_status) == 0:
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
        i = i + 1    
        
    if request.method == 'POST':
        message = 'Cập nhật thành công hạnh kiểm lớp ' + str(Class.objects.get(id=class_id))
        term1 = request.POST.getlist('term1')
        term2 = request.POST.getlist('term2')
        y = request.POST.getlist('year')
        i = 0
        for p in pupilList:            
            hk = p.hanhkiem_set.get(year_id__exact=year.id)
            if (term.number == 1):
                data = {'student_id':p.id, 'term1':term1[i], 'year_id':year.id}
            else:
                data = {'student_id':p.id, 'term1':hk.term1, 'term2':term2[i], 'year':y[i], 'year_id':year.id}
            form[i] = HanhKiemForm(data, instance=hk)
            form[i].save()        
            i = i + 1            
    classList = year.class_set.all()
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
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    
    if (get_position(request) < 4):
        return HttpResponseRedirect('/')
    sub = Subject.objects.get(id=subject_id)        
    class_id = sub.class_id    
    if in_school(request, class_id.block_id.school_id) == False:
        return HttpResponseRedirect('/')
    
    form = SubjectForm (class_id.block_id.school_id.id, instance = sub)
    message = None
    if request.method == 'POST':
        data = request.POST
        form = SubjectForm(class_id.block_id.school_id.id, data, instance = sub)
        if form.is_valid():
            primary = request.POST.get('primary', False)
            change_primary(sub, primary)
            form.save()                        
            message = 'Bạn đã cập nhật thành công'        
            
    t = loader.get_template(os.path.join('school', 'subject_detail.html'))
    c = RequestContext(request, {   'form':form, 
                                    'message':message,
                                    'id': subject_id,
                                    'class_id' : sub.class_id.id
                                    })
    return HttpResponse(t.render(c))
