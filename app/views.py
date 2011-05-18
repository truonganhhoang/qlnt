from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from app.models import UserForm, Organization, UserProfile, ChangePasswordForm, ContactForm
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

        self.fields['full_name'].choices = [(i.id, i.last_name + ' ' + i.first_name) for i in users]
        self.fields['school'].choices = [(o.id, o.name) for o in Organization.objects.all() if o.level == 'T']

    full_name = forms.ChoiceField()
    school = forms.ChoiceField()
   
def school_admin_add(request):
    form = SchoolAdminAddForm(request.POST)
    if request.method == 'POST':
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
    c = RequestContext(request,{'form': form})
    return HttpResponse(t.render(c))

# Developer: Do Duc Binh    
def list_org (request):
    list_s = Organization.objects.filter(level = 'S')
    list_p = Organization.objects.filter(level = 'P')
    list_t = Organization.objects.filter(level = 'T')
    
    t = loader.get_template('app/list_org.html')
    c = RequestContext(request, {'list_s':list_s, 'list_p': list_p, 'list_t':list_t})
    return HttpResponse(t.render(c))

# quyendt
def change_password(request,
                    template_name='app/change_password.html',
                    post_change_redirect=None,
                    password_change_form=ChangePasswordForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('app.views.change_password_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))
    
# quyendt
def change_password_done(request):
    t = loader.get_template('app/change_password_done.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def contact(request):
#hainhh
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
        
            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)
        
            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })