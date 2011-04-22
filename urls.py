from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView
from persistent_messages.models import Message
import settings 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'app.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^help/$', 'app.views.help'),
    #(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
    # the built-in sign-in/out module 
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
 
    # Examples:
    # url(r'^$', 'qlnt.views.home', name='home'),
    # url(r'^qlnt/', include('qlnt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
                      
    # urls for app app
    
    url(r'^app/', include('app.urls')),
    # urls for batchimport app
    url(r'^school/', include('batchimport.urls')),
    # url for school app
    url(r'^school/', include('school.urls')),
    
    url(r'^messages/', include('persistent_messages.urls')),
    
)
