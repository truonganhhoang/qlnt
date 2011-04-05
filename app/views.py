from django.http import HttpResponse, HttpResponseRedirect
from app.models import TimeTableForm
from app.models import SystemDataTypeForm, UserTypeDataType
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template import Context
from django.template.loader import get_template

def time_table_add(request):
    if request.method == 'POST':
        form = TimeTableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/timetable/')
    else:
        form = TimeTableForm()
    t = loader.get_template('app/timetable/add.html')
    c = RequestContext(request, {'form' : form})
    return HttpResponse(t.render(c))

def main_page(request):
    template = get_template('main_page.html')
    variables = Context({
        'head_title': 'School Administration',
        'page_title': 'School Administration',
        'page_body': 'Body '
    })
    output = template.render(variables)
    return HttpResponse(output)

def timetable(request):
    template = get_template('app/timetable.html')
    variables = Context({
        'head_title': 'Quan Ly Nha Truong',
        'page_title': 'This is title of timetable page',
        'page_body': 'This is body of timetable page',
    })
    output = template.render(variables)
    return HttpResponse(output)

def system_datatype_add(request):
    if request.method == 'POST':
        form = SystemDataTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/systemdatatype/')
    else:
        form = SystemDataTypeForm()
    t = loader.get_template('app/systemdatatype/add.html')
    c = RequestContext(request, {'form' : form})
    return HttpResponse(t.render(c))

def user_type_data_type(request):
    pass