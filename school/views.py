# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template import Context
from django.template.loader import get_template
from school.models import *


def school(request, school_code = None):
	class_list = Class.objects.all()
	context = RequestContext(request)
	return render_to_response(r'school/school.html', context_instance = context)
	
def add_class(request):
    message = None
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_code = form.cleaned_data['class_code']
            name = form.cleaned_data['name']
            school_id = form.cleaned_data['school_id']
            teacher_id = form.cleaned_data['teacher_id']
            new_class = Class.objects.create(class_code  = class_code, \
             								name = name, school_id = school_id, teacher_id = teacher_id)
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
            new_teacher = Teacher.objects.create(first_name = fn, last_name=ls,\
            									 birthday = bd, birth_place = bl,\
            									 sex = s, phone = p, current_address = ca, email = e)
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
            subject_code = form.cleaned_data['subject_code']
            class_code = form.cleaned_data['class_code']
            name = form.cleaned_data['name']
            hs = form.cleaned_data['hs']
            teacher_id = form.cleaned_data['teacher_id']
            term_id = form.cleaned_data['term_id']
            new_subject = Subject.objects.create(subject_code = subject_code, \
            									class_code  = class_code, name = name, \
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

