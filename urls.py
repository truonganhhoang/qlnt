from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app.models import TimeTable, SystemDataType 
from app.models import MarkByPeriod
from app.models import User
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
    
                       
    url(r'^app/timetable/$', ListView.as_view(
            queryset=TimeTable.objects.all(),
            context_object_name='time_table_list',
            template_name='app/timetable/index.html')),
    url(r'^app/timetable/(?P<pk>\d+)$', DetailView.as_view(model=TimeTable,
                                                        template_name='app/timetable/detail.html')),
    url(r'^app/timetable/add$', 'app.views.time_table_add'),
    url(r'^app/school/add$', 'app.views.school_add'),
    url(r'^app/systemdatatype/$', ListView.as_view(
            queryset=SystemDataType.objects.all(),
            context_object_name='system_datatype_list',
            template_name='app/systemdatatype/index.html')),
    url(r'^app/systemdatatype/(?P<pk>\d+)$', DetailView.as_view(model=SystemDataType,
                                                        template_name='app/systemdatatype/detail.html')),
    url(r'^app/systemdatatype/add$', 'app.views.system_datatype_add'),
    
    url(r'^app/schoolstaff/$', ListView.as_view(
    		queryset=User.objects.all(),
    		context_object_name='user_list',
    		template_name='app/schoolstaff/index.html')),
    url(r'app/schoolstaff/(?P<pk>\d+)$', DetailView.as_view(model=User,
    													template_name='app/schoolstaff/detail.html')),
    url(r'^app/schoolstaff/add$', 'app.views.user_add'),
    
     #==========================================================================
     # (r'app/markbyperiod/$', 'app/markbyperiod/index.html'),
     # (r'app/markbyperiod/(?P<markbyperiod_id>\d+)/$', DetailView.as_view(model=MarkByPeroid,
     #                                                   template_name='app/markbyperiod/detail.html'))
     #==========================================================================
     
     url(r'^app/markbyperiod/$', ListView.as_view(
            queryset=MarkByPeriod.objects.all(),
            context_object_name='mark_by_period_list',
            template_name='app/markbyperiod/index.html')),
     url(r'^app/markbyperiod/(?P<pk>\d+)$', DetailView.as_view(model=MarkByPeriod,
                                                         template_name='app/markbyperiod/detail.html')),
     url(r'^app/markbyperiod/add$', 'app.views.mark_by_period_add'),
    
    # url for school app
    
    url(r'^school/$','school.views.school'), 
    url(r'^school/', include('batchimport.urls')),
    url(r'^school/classes/add$', 'school.views.add_class'),
    url(r'^school/teachers/add$', 'school.views.add_teacher'),
    url(r'^school/subjects/add$', 'school.views.add_subject'),
    url(r'^school/students/add$', 'school.views.add_pupil'),
)
