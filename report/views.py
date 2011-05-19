from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from report.models import ReceiverReportForm, SendReportForm
#from app.models import PositionTypeForm
from django.template import RequestContext, loader
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import *

# Create your views here.
def index(request): 
    return render_to_response("report/index.html", context_instance=RequestContext(request))

def addReceiverReport(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    if request.method =='POST':
        form = ReceiverReportForm(request.POST)
        if form.is_valid():
            t = loader.get_template('report/add_report_success.html')
            c = RequestContext(request, {})
            return HttpResponse(t.render(c))
    else:
        form = ReceiverReportForm()
    t= loader.get_template('report/add_receiver_report.html')
    c= RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))

def addSendReport(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    if request.method =='POST':
        form = SendReportForm(request.POST)
        if form.is_valid():
            t = loader.get_template('report/add_report_success.html')
            c = RequestContext(request, {})
            return HttpResponse(t.render(c))
    else:
        form = SendReportForm()
    t= loader.get_template('report/add_send_report.html')
    c= RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))