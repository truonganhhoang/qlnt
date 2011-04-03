from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app.models import TimeTable

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'app.views.main_page'),
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
    url(r'^app/timetable/add$', 'app.views.time_table_add')
)
