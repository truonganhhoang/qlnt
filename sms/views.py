from django.views.generic.list import ListView
from sms.models import sms, smsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

def index(request):
    return render_to_response("sms/index.html", context_instance=RequestContext(request))

def manual_sms(request):
    if request.method == 'POST':
        form = smsForm(request.POST)
        if form.is_valid():
            phone_list = form.cleaned_data.get('phone')
            content = form.cleaned_data.get('content')
            
            phone = phone_list.split(',')
            for p in phone:            
                '''Save to db'''
                s = sms(phone=p, content=content)
                s.save()
                '''Send sms via Viettel system'''
                '''Implement Me'''
            
            return HttpResponseRedirect('/sms/sent_sms/')
#            return HttpResponse(phone_list)
    else:
        form = smsForm()    
    t = loader.get_template('sms/manual_sms.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))
