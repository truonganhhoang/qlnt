# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from school.models import *

def school(request):
	class_list = Class.objects.all()
	return render_to_response(r'school/school.html')
