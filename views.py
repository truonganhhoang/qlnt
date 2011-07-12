from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import models

import cStringIO as StringIO
from cgi import escape
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf

OVER_SCHOOL = ['GIAM_DOC_SO', 'TRUONG_PHONG']

def index(request):
    if not request.user.is_authenticated():
        return render_to_response("index.html", context_instance=RequestContext(request)) 
    elif request.user.get_profile().position in OVER_SCHOOL or\
    request.user.is_superuser:
        return render_to_response("index.html", context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect(reverse('school_index'))

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def help(request):
    if request.method == "POST":
        if request.POST['clickedButton'] == "export_pdf":
            return render_to_response("base.html", context_instance=RequestContext(request))
    return render_to_response("help.html", context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('thanks.html', context_instance=RequestContext(request))

def topdf(request):
    return render_to_pdf('app/list_org.html',{
        'pagesize': 'A4'})
    
#method routes to the view ``profiles.views.profile_detail``, passing the username
@models.permalink
def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
get_absolute_url = models.permalink(get_absolute_url)
