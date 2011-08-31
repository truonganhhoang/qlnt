from django.conf.urls.defaults import patterns, include, url
import settings 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name = "index"),
    (r'^help/$', 'views.help'),
    (r'^app/contact/$', 'app.views.feedback'),
    (r'^thanks/$', 'views.thanks'),
    # the built-in sign-in/out module 
    url(r'^login/$', 'app.views.login', name = "login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'app/logout.html'}, name = "logout"),
    #(r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    #(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # urls for app app
    url(r'^app/', include('app.urls')),
    
    # url for school app
    url(r'^school/', include('school.urls')),
    
    url(r'^messages/', include('persistent_messages.urls')),
    
    url(r'^sms/', include('sms.urls')),
    
    url(r'^report', include('report.urls')),

    (r'^topdf/$', 'views.topdf'),
    url(r'^profiles/', include('profiles.urls')),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),

    #urls for django-sentry
    (r'^sentry/', include('sentry.web.urls')),
)
