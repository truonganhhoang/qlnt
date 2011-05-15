from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from app.models import UserForm, Organization, UserProfile
#from app.models import PositionTypeForm
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render_to_response
# Create your views here.
def base_report(request): 
    return render_to_response("base_report.html", context_instance=RequestContext(request))
