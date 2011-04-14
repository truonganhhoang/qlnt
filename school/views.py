# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from school.models import *

def school(request, school_code = None):
	class_list = Class.objects.all()
	context = RequestContext(request, {'class_list':class_list , 'school_code':school_code})
	return render_to_response(r'school/school.html',context_instance = context)
