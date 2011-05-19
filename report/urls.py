from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Add, remove, change personal information
    (r'^$', 'report.views.index'),
    (r'addreceiverreport/$', 'report.views.addReceiverReport'),
    (r'addsendreport/$', 'report.views.addSendReport'),
)
