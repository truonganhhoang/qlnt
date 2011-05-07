from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView
from sms.models import sms

urlpatterns = patterns('',
    url(r'^$', 'sms.views.index'),
    url(r'^manual_sms/$', 'sms.views.manual_sms'),
    url(r'^upload_excel/$', 'sms.views.upload_excel'),
    url(r'^preview_sms/$', 'sms.views.preview_sms'),
    url(r'^sent_sms/$', ListView.as_view(
            queryset=sms.objects.all(),
            context_object_name='sms_list',
            template_name='sms/sent_sms.html')),
    url(r'^export_excel/$', 'sms.views.export_excel')
)
