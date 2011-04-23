import persistent_messages
from persistent_messages.models import Message, MessageForm
from persistent_messages.storage import get_user
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User 

def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            admin = User.objects.get(username='admin')
            persistent_messages.add_message(request, persistent_messages.SUCCESS, 'Hi Admin, here is a message to you.', subject='Success message', user=admin)
            return HttpResponseRedirect('/messages/')
    else:
        form = MessageForm()    
    t = loader.get_template('persistent_messages/message/add_message.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))

def message_detail(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()
    return render_to_response('persistent_messages/message/detail.html', {'message': message},
        context_instance=RequestContext(request))

def message_mark_read(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')

def message_mark_all_read(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    Message.objects.filter(user=user).update(read=True)
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')
