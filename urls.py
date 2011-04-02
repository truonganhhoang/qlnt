from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from app.models import TimeTable

urlpatterns = patterns('',
    (r'^$', main_page),
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
            template_name='app/timetable/index.djhtml'))
)
