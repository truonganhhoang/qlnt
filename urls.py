from django.conf.urls.defaults import patterns, include, url
import settings 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^help/$', 'views.help'),
    # the built-in sign-in/out module 
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    #(r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    #(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
 
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
    
    #url(r'^grappelli/', include('grappelli.urls')),
    
    url(r'^rosetta/', include('rosetta.urls')),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )