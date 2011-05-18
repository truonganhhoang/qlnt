from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from app.models import UserForm, Organization, UserProfile
#from app.models import PositionTypeForm
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render_to_response
from objectpermission.decorators import object_permission_required
from reportlab.pdfgen import canvas
from django.core.exceptions import ObjectDoesNotExist

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

@object_permission_required('view_level=T', Organization)
def organization_delete(request, id):
    o = Organization.objects.get(pk=id)
    o.delete()
    return HttpResponse('Deleted')

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
        user_all = User.objects.all()
        user = []
        for u in user_all:
            try:
                if (u.get_profile().position != 'HOC_SINH'):
                    user.append(u)
            except:
                pass

    t = loader.get_template('app/school_admin_add.html')
    c = RequestContext(request,{'user': user})
    return HttpResponse(t.render(c))

# Developer: Do Duc Binh    
def list_org (request):
    user = request.user
#    query = Organization.objects.all()
    if user.is_superuser:
        query = Organization.objects.filter(level = 'S')
    else:
        query = Organization.objects.filter(upper_organization = user.userprofile.organization_id)
        
    list = []
    for q in query:
        list.append(q)
    t = loader.get_template('app/list_org.html')
    c = RequestContext(request, {'list': list})
    return HttpResponse(t.render(c))

def list_under_org (request):
    org = request.GET
    if org.level == 'S' or org.level == 'P':
        query = Organization.objects.filter(upper_organization = org.id)
        
    list = []
    for q in query:
        list.append(q)
    t = loader.get_template('app/list_under_org.html')
    c = RequestContext(request, {'list': list, 'org': org})
    return HttpResponse(t.render(c))