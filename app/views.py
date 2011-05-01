from django.http import HttpResponse, HttpResponseRedirect
from app.models import UserForm
#from app.models import PositionTypeForm
from django.template import RequestContext, loader

def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/user/')
    else:
        form = UserForm()
    t = loader.get_template('app/user/add.html')
    c = RequestContext(request, {'form' : form})
    return HttpResponse(t.render(c))

