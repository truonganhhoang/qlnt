from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView
from persistent_messages.models import Message

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
            queryset=Message.objects.all(),
            context_object_name='messages',
            template_name='persistent_messages/message/includes/messages.html')),
    url(r'^all_messages/$', ListView.as_view(
            queryset=Message.objects.all(),
            context_object_name='message_list',
            template_name='persistent_messages/message/index.html')),
    url(r'^add_message/$', 'persistent_messages.views.add_message'),
    url(r'^detail/(?P<message_id>\d+)/$', 'persistent_messages.views.message_detail', name='message_detail'),
    url(r'^mark_read/(?P<message_id>\d+)/$', 'persistent_messages.views.message_mark_read', name='message_mark_read'),
    url(r'^mark_read/all/$', 'persistent_messages.views.message_mark_all_read', name='message_mark_all_read'),
)
