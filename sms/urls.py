from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView
from sms.models import sms
from datetime import datetime, timedelta

urlpatterns = patterns('',
    url(r'^manual_sms/$', 'sms.views.manual_sms'),
    url(r'^excel_sms/$', 'sms.views.excel_sms'),
    url(r'^sent_sms/$', ListView.as_view(
            queryset=sms.objects.filter(created__range=(datetime.now() - timedelta(hours=0, minutes=1, seconds=0),datetime.now())),
            context_object_name='sms_list',
            template_name='sms/sent_sms.html')),
    url(r'^export_excel/$', 'sms.views.export_excel')
)
