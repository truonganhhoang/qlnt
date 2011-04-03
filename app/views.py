from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def main_page(request):
    template = get_template('main_page.html')
    variables = Context({
        'head_title': 'Quan Ly Nha Truong',
        'page_title': 'This is title of main_page',
        'page_body': 'This is body of main_page.'
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