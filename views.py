from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import cStringIO as StringIO
from cgi import escape
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context

def index(request): 
    return render_to_response("index.html", context_instance=RequestContext(request))

def help(request):
    return render_to_response("help.html", context_instance=RequestContext(request))

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

def topdf(request):
    return render_to_pdf('base.html',{
                                        
        'pagesize': 'A4'})