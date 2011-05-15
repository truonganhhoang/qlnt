from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Add, remove, change personal information
    url(r'^$', 'report.views.base_report'),    
)
