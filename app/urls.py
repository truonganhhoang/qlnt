from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app.models import User


urlpatterns = patterns('',
    # Add, remove, change personal information
#    url(r'user/$', ListView.as_view(
#			queryset=User.objects.all(),
#			context_object_name='user_list',
#			template_name='app/user/index.html')),
#    url(r'user/(?P<pk>\d+)$', DetailView.as_view(model=User,
#														template_name='app/user/detail.html')),
#    url('user/add$', 'app.views.user_add'),
#        
#    url(r'schoolstaff/$', ListView.as_view(
#    		queryset=User.objects.all(),
#    		context_object_name='user_list',
#    		template_name='app/schoolstaff/index.html')),
#    url(r'schoolstaff/(?P<pk>\d+)$', DetailView.as_view(model=User,
#    													template_name='app/schoolstaff/detail.html')),
#    url(r'schoolstaff/add$', 'app.views.user_add'),
#    
#     Them truong hoc, phong giao duc hoac so giao duc cung admin cua to chuc do
#    url(r'organization/$', )
#    url('organization/add$', 'app.views.organization_add')
)