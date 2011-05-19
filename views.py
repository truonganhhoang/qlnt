from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import cStringIO as StringIO
from cgi import escape
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf


#login logout
from django import forms
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

OVER_SCHOOL = ['GIAM_DOC_SO', 'TRUONG_PHONG']

#def index(request):
##    if not request.user.is_anonymous() and request.user.get_profile().position in OVER_SCHOOL or\
#    if request.user.get_profile().position in OVER_SCHOOL or\
#    request.user.is_superuser:
#        return render_to_response("index.html", context_instance=RequestContext(request))
#    else:
#        return HttpResponseRedirect('/school/')
def index(request): 
    return render_to_response("index.html", context_instance=RequestContext(request))


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


def topdf(request):
    return render_to_pdf('base.html',{        
        'pagesize': 'A4'})