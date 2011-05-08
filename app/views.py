from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from app.models import UserForm, Organization, UserProfile
#from app.models import PositionTypeForm
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render_to_response
from objectpermission.decorators import object_permission_required
from reportlab.pdfgen import canvas

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

#def organization_add (request):
#    if request.method == 'POST':
#        form = OrganizationForm (request.POST)
#        if form.is_valid() or form.upper_organization == None :
#            form.save()
#            return HttpResponseRedirect ('/app/organization/add/')
#    else:
#        form = OrganizationForm()
#    t = loader.get_template('app/organization/add.html')
#    c = RequestContext (request, {'form': form})
#    return HttpResponse (t.render(c))

@object_permission_required('view_level=T', Organization)
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

class SchoolAdminAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SchoolAdminAddForm, self).__init__(*args, **kwargs)
        users = [i.user for i in UserProfile.objects.all() if i.organization is None or i.organization.level == 'T']
        
        for u in User.objects.all():
            if u in users:
                continue
            try:
                org = u.get_profile().organization
                if org is None or org.level == 'T':
                    users.append(u)
            except UserProfile.DoesNotExist:
                users.append(u)

        self.fields['username'].choices = [(i.id, i.username) for i in users]
        self.fields['school'].choices = [(o.id, o.name) for o in Organization.objects.all() if o.level == 'T']

    username = forms.ChoiceField()
    school = forms.ChoiceField()
    
def school_admin_add(request):
    if request.method == 'POST':
        form = SchoolAdminAddForm(request.POST)
        if form.is_valid():
            # TODO Add initial permission here
            t = loader.get_template('app/school_admin_add_success.html')
            c = RequestContext(request, {})
            return HttpResponse(t.render(c))
    else:
        form = SchoolAdminAddForm()

    t = loader.get_template('app/school_admin_add.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))
