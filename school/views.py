# -*- coding: utf-8 -*-

# Create your views here.

import os.path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template import Context
from django.template.loader import get_template
from school.models import *

import xlrd
import xlwt

NHAP_DANH_SACH_TRUNG_TUYEN = r'school/import/nhap_danh_sach_trung_tuyen.html'
DANH_SACH_TRUNG_TUYEN = r'school/import/danh_sach_trung_tuyen.html'
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
def school(request):
	class_list = Class.objects.all()
	context = RequestContext(request)
	return render_to_response(r'school/school.html', context_instance = context)
	
def add_class(request):
    message = None
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            year_id = form.cleaned_data['year_id']
            teacher = form.cleaned_data['teacher']
            khoi = form.cleaned_data['khoi']
            new_class = Class.objects.create(khoi = khoi, \
             								name = name, teacher = teacher, year_id = year_id)
            new_class.save()
            message = 'You have added new class'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/add_class.html')
    c = RequestContext(request, {'form' : form, 'message' : message})
    return HttpResponse(t.render(c))
    
def add_teacher(request):
    message = None
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            fn = form.cleaned_data['first_name']
            ls = form.cleaned_data['last_name']
            bd = form.cleaned_data['birthday']
            bl = form.cleaned_data['birth_place']
            s = form.cleaned_data['sex']
            p = form.cleaned_data['phone']
            ca = form.cleaned_data['current_address']
            e = form.cleaned_data['email']
            school_id = form.cleaned_data['school_id']
            new_teacher = Teacher.objects.create(first_name = fn, last_name=ls,\
            									 birthday = bd, birth_place = bl,\
            									 sex = s, phone = p, current_address = ca, \
            									 school_id = school_id, email = e)
            new_teacher.save()
            message = 'You have added new teacher'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/add_teacher.html')
    c = RequestContext(request, {'form' : form, 'message' : message})
    return HttpResponse(t.render(c))

def add_subject(request ):
    message = None
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            hs = form.cleaned_data['hs']
            loai = form.cleaned_data['loai']
            class_id = form.cleaned_data['class_id']
            teacher_id = form.cleaned_data['teacher_id']
            term_id = form.cleaned_data['term_id']
            new_subject = Subject.objects.create(loai = loai, \
            									class_id  = class_id, name = name, \
            									hs = hs, teacher_id = teacher_id, term_id = term_id)
            new_subject.save()
            message = 'You have added new subject'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/add_subject.html')
    c = RequestContext(request, {'form' : form, 'message' : message})
    return HttpResponse(t.render(c))

def add_pupil(request):
    message = None
    form = PupilForm()
    if request.method == 'POST':
        form = PupilForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'You have added new student'
        else:
            message = 'Please check your information, something is wrong'

    t = loader.get_template('school/add_pupil.html')
    c = RequestContext(request, {'form' : form, 'message' : message})
    return HttpResponse(t.render(c))

#cac chuc nang:
#hien thu bang diem cua mot lop, cho edit roi save lai
def mark_table(request, school_code = None):
	message = None
	
	#subjectForm = SubjectForm()
	#termForm    = TermForm()
	#classForm   =ClassForm()
	
	subjectList =Subject.objects.all()
	classList   =Class.objects.all()
	
	pupilList=None
	termChoice =-1
	classChoice=-1
	subjectChoice=-1
	
	markList=[]
	list=None
	idList=[]	
	ttt="abc "	
	ttt1="def "
	tttt="kkk "
	if request.method == 'POST':
		classChoice=request.POST['class1']
		subjectChoice=request.POST['subject']
		termChoice   =request.POST['term']
		
		pupilList = Pupil.objects.filter(class_id=classChoice)
		
		i=1;				
		for p in pupilList:
			m = p.mark_set.get(subject_id=subjectChoice)
			markList.append(m)
			
			k=i*100
			id=MarkID(k+1,k+2,k+3,k+4,k+5,k+6,k+7,k+8,k+9,k+10,k+11,k+12,k+13,k+14,k+15,k+16)
			idList.append(id)
			i=i+1
			
		list=zip(pupilList,markList,idList)
		if request.POST['submitChoice']=="luulai":
			#for m in markList:
			i=0;			
			for m in markList:
				sum=0
				foctorSum=0
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
					foctorSum+=1
					
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
					foctorSum+=1
					
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
					foctorSum+=1
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
					foctorSum+=1

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
					foctorSum+=1

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
					foctorSum+=1

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
					foctorSum+=1
					
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
					foctorSum+=1
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
					foctorSum+=1

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
					foctorSum+=1
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
					foctorSum+=2
					
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
					foctorSum+=2
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
					foctorSum+=2
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
					foctorSum+=2
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
					foctorSum+=2
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
					foctorSum+=3
				if foctorSum==0:
					m.tb=0
				else:						
					m.tb=sum/foctorSum	
				m.save()
				i=i+1							

	t = loader.get_template('school/mark_table.html')
	
	c = RequestContext(request, { 
								'message' : message,
								'subjectList':subjectList,
								'classList' :classList,
								'classChoice':classChoice,
								'subjectChoice':subjectChoice,
								'termChoice':termChoice,								
								'list':list,
								'ttt':ttt,
								'ttt1':ttt1,
								'tttt':tttt,
								}
					   )
	

	return HttpResponse(t.render(c))
#----------- Exporting and Importing form Excel -------------------------------------

class UploadImportFileForm(forms.Form):
    import_file = forms.FileField(label=u'Chọn file excel:')
    
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
                if ( sheet.cell_value(r, c) == u'Mã học sinh'):
                    start_row = r
                    flag = True
                    break
            if flag: break
        #                                                             CHUA BIEN LUAN TRUONG HOP: start_row = -1, ko co cot ten: Mã học sinh
        # start_row != 0
        c_code =-1
        c_school_code =-1
        c_nguyen_vong =-1
        c_diem =-1
        for c in range(0, sheet.ncols):
            value = sheet.cell_value(start_row, c)
            if ( value == u'Mã học sinh'):
                c_code = c
            elif ( value == u'Mã trường'):
                c_school_code = c
            elif ( value == u'Nguyện vọng'):
                c_nguyen_vong = c
            elif ( value == u'Điểm'):
                c_diem = c
        column_index = 0
        for r in range(start_row + 1, sheet.nrows):
            code = sheet.cell_value( r, c_code)
            school_code = sheet.cell_value( r, c_school_code)
            nv = sheet.cell_value( r, c_nguyen_vong)
            diem = sheet.cell_value( r, c_diem)
            student_list.append( { 'ma_hoc_sinh': code,\
                                   'ma_truong': school_code,\
                                   'nguyen_vong': nv, \
                                   'diem': diem, }) 
        return student_list
    else: task == ""
    
    return None

def nhap_danh_sach_trung_tuyen(request):
    school = School.objects.all()[0] # it's for testing, actually, it should be: school = School.objects.get(id = request['school_id'])
    if request.method == 'POST':
        form = UploadImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            save_file_name = save_file(form.cleaned_data['import_file'], request.session)
            print save_file_name
            request.session['save_file_name'] = save_file_name
            
            student_list = process_file(file_name = save_file_name, \
                                        task = "Nhap danh sach trung tuyen")
            print student_list
            context = RequestContext(request, {'school':school,})
            return render_to_response(DANH_SACH_TRUNG_TUYEN,\
                                    {'student_list':student_list,}, \
                                    context_instance = context)
    else:
        form = UploadImportFileForm()
    context = RequestContext(request, {'form':form, 'school':school})
    return render_to_response(NHAP_DANH_SACH_TRUNG_TUYEN, context_instance = context)
        
def danh_sach_trung_tuyen(request):
    context = RequestContext(request)
    return render_to_response(DANH_SACH_TRUNG_TUYEN, context_instance = context)
#------------------------------------------------------------------------------------


def test(request, school_code = None):
	t = loader.get_template('school/test.html')
	
	c = RequestContext(request)

	return HttpResponse(t.render(c))
