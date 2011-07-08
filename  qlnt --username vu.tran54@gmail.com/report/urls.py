from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Add, remove, change personal information
    (r'^$', 'report.views.index'),
    (r'addreceiverreport/$', 'report.views.add_Receiver_Report'),
    (r'addsendreport/$', 'report.views.add_Send_Report'),
)
