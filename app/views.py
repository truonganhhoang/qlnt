from django.http import HttpResponse, HttpResponseRedirect
from app.models import UserForm, Organization
#from app.models import PositionTypeForm
from django.template import RequestContext, loader
from objectpermission.decorators import permission_required

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

def organization_add (request):
    if request.method == 'POST':
        form = OrganizationForm (request.POST)
        if form.is_valid() or form.upper_organization == None :
            form.save()
            return HttpResponseRedirect ('/app/organization/add/')
    else:
        form = OrganizationForm()
    t = loader.get_template('app/organization/add.html')
    c = RequestContext (request, {'form': form})
    return HttpResponse (t.render(c))

@permission_required('Organization.level_delete', 'T')
def organization_delete(request, id):
    o = Organization.objects.get(pk=id)
    o.delete()
    return HttpResponse('Deleted')


#def positiontype_add(request):
#    if request.method == 'POST':
#        form = PositionTypeForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/app/positiontype/')
#        else:
#            form = PositionTypeForm()
#        t = loader.get_template('app/positiontype/add.html')
#        c = RequestContext(request, {'form' : form})
#        return HttpResponse(t.render(c))
