from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView
from sms.models import sms
from datetime import datetime, timedelta

urlpatterns = patterns('',
    url(r'^manual_sms/$', 'sms.views.manual_sms'),
    url(r'^excel_sms/$', 'sms.views.excel_sms'),
    url(r'^sent_sms/$', 'sms.views.sent_sms'),
    url(r'^failed_sms/$', 'sms.views.failed_sms'),
)
