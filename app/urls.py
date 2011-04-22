from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app.models import TimeTable, SystemDataType 
from app.models import MarkByPeriod
from app.models import User
import settings 


urlpatterns = patterns('',
    # Add, remove, change personal information
    url(r'user/$', ListView.as_view(
			queryset=User.objects.all(),
			context_object_name='user_list',
			template_name = 'app/user/index.html')),
    url(r'user/(?P<pk>\d+)$', DetailView.as_view(model=TimeTable,
														template_name = 'app/user/detail.html')),
    url('user/add$', 'app.views.user_add'),
    
	url(r'timetable/$', ListView.as_view(
            queryset=TimeTable.objects.all(),
            context_object_name='time_table_list',
            template_name='app/timetable/index.html')),
    url(r'timetable/(?P<pk>\d+)$', DetailView.as_view(model=TimeTable,
                                                        template_name='app/timetable/detail.html')),
    url(r'timetable/add$', 'app.views.time_table_add'),
    url(r'school/add$', 'app.views.school_add'),
    
    url(r'systemdatatype/$', ListView.as_view(
            queryset=SystemDataType.objects.all(),
            context_object_name='system_datatype_list',
            template_name='app/systemdatatype/index.html')),
    url(r'systemdatatype/(?P<pk>\d+)$', DetailView.as_view(model=SystemDataType,
                                                        template_name='app/systemdatatype/detail.html')),
    url(r'systemdatatype/add$', 'app.views.system_datatype_add'),
    
    url(r'schoolstaff/$', ListView.as_view(
    		queryset=User.objects.all(),
    		context_object_name='user_list',
    		template_name='app/schoolstaff/index.html')),
    url(r'schoolstaff/(?P<pk>\d+)$', DetailView.as_view(model=User,
    													template_name='app/schoolstaff/detail.html')),
    url(r'schoolstaff/add$', 'app.views.user_add'),
    
     #==========================================================================
     # (r'app/markbyperiod/$', 'app/markbyperiod/index.html'),
     # (r'app/markbyperiod/(?P<markbyperiod_id>\d+)/$', DetailView.as_view(model=MarkByPeroid,
     #                                                   template_name='app/markbyperiod/detail.html'))
     #==========================================================================
     
     url(r'markbyperiod/$', ListView.as_view(
            queryset=MarkByPeriod.objects.all(),
            context_object_name='mark_by_period_list',
            template_name='app/markbyperiod/index.html')),
     url(r'markbyperiod/(?P<pk>\d+)$', DetailView.as_view(model=MarkByPeriod,
                                                         template_name='app/markbyperiod/detail.html')),
     url(r'markbyperiod/add$', 'app.views.mark_by_period_add'),
	)
