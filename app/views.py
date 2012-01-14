# -*- coding: utf-8 -*-
import os.path
import urlparse
import smtplib
import thread
from email.mime.text import MIMEText
from datetime import date
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from app.models import UserForm, Organization, UserProfile, ChangePasswordForm, FeedbackForm, AuthenticationForm, Feedback, ResetPassword, ResetPasswordForm
import django.template
from django import forms
from django.shortcuts import render_to_response
from django.utils import simplejson
#from objectpermission.decorators import object_permission_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from school.utils import *
from school.models import *

REGISTER = os.path.join('app', 'register.html')
MANAGE_REGISTER = os.path.join('app', 'manage_register.html')

def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/user/')
    else:
        form = UserForm()
    t = django.template.loader.get_template('app/user/add.html')
    c = django.template.RequestContext(request, {'form' : form})
    return HttpResponse(t.render(c))

#@object_permission_required('view_level=T', Organization)
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
            t = django.template.loader.get_template(os.path.join('app', 'school_admin_add_success.html'))
            c = django.template.RequestContext(request, {})
            return HttpResponse(t.render(c))
    else:
        user_all = User.objects.all()
        user = []
        for u in user_all:
            try:
                if u.get_profile().position != 'HOC_SINH':
                    user.append(u)
            except Exception as e:
                pass

    t = django.template.loader.get_template(os.path.join('app', 'school_admin_add.html'))
    c = django.template.RequestContext(request,{'form': form})
    return HttpResponse(t.render(c))

# Developer: Do Duc Binh    
def list_org (request):
    list_s = Organization.objects.filter(level = 'S')
    list_p = Organization.objects.filter(level = 'P')
    list_t = Organization.objects.filter(level = 'T')

    t = django.template.loader.get_template(os.path.join('app', 'list_org.html'))
    c = django.template.RequestContext(request, {'list_s':list_s, 'list_p': list_p, 'list_t':list_t})
    return HttpResponse(t.render(c))

def register(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('school_index'))
        else:
            message = ''
            if request.method == 'POST':
                data = request.POST.copy()
                data['status'] = 'CHUA_CAP'
                data['register_date'] = date.today()
                register_form = RegisterForm(data= data)
                if register_form.is_valid():
                    register_form.save()
                    message = u'Bạn đã đăng ký thành công. Tài khoản của bạn sẽ được gửi vào email sớm nhất có thể.'
                    success = True
                    if request.is_ajax():
                        response = simplejson.dumps({
                            'success': success,
                            'message': message
                        })
                        return HttpResponse(response, mimetype='json')
                else:
                    message = u"Có lỗi ở thông tin nhập vào"
                    success = False
                    for e in register_form:
                        if e.errors:
                            print e
                    if request.is_ajax():
                        response = simplejson.dumps({
                            'success': success,
                            'message': message
                        })
                        return HttpResponse(response, mimetype='json')
            province_list = TINH_CHOICES
            level_list = KHOI_CHOICES
            context = RequestContext(request)
            return render_to_response(REGISTER,
                    {'province_list': province_list,
                     'level_list': level_list,
                     'message': message},
                                      context_instance = context)
    except Exception as e:
        print e
        raise e

def manage_register(request, sort_by_date=0, sort_by_status=0):
    try:
        if not request.user.is_superuser:
            return HttpResponseRedirect( reverse('school_index'))
        if request.method == 'POST':
            if request.is_ajax():
                request_type = request.POST['request_type']
                if request_type == 'del':
                    ids = request.POST['data'].split('-')
                    print ids
                    try:
                        for id in ids:
                            if id:
                                register = Register.objects.get(id= int(id))
                                register.delete()
                        message = u'Xóa thành công'
                        success = True
                        data = simplejson.dumps({
                            'message': message,
                            'success': success
                        })
                        return HttpResponse(data, mimetype='json')
                    except Exception as e:
                        print e
                        message = u'Không thể xóa đăng ký'
                        success = False
                        data = simplejson.dumps({
                            'message': message,
                            'success': success
                        })
                        return HttpResponse(data, mimetype='json')
                elif request_type == 'create_acc':
                    ids = request.POST['data'].split('-')
                    print ids
                    try:
                        account_info = ''
                        for id in ids:
                            if id:
                                register = Register.objects.get(id= int(id))
                                org_name = register.school_name
                                org_level = 'T'
                                org_school_level = register.school_level
                                org_status = 0
                                org_manager_name = register.register_name
                                org_address = register.school_address
                                phone = register.register_phone
                                email = register.register_email
                                school = Organization.objects.create(
                                                            name= org_name,
                                                            level= org_level,
                                                            school_level= org_school_level,
                                                            status= org_status,
                                                            manager_name= org_manager_name,
                                                            address= org_address,
                                                            phone= phone,
                                                            email= email
                                                        )
                                user = User()
                                user.username = make_username( full_name=org_manager_name)
                                user.password = make_default_password( user.username )
                                user.save()
                                userprofile = UserProfile()
                                userprofile.user = user
                                userprofile.organization = school
                                userprofile.position = 'HIEU_TRUONG'
                                userprofile.save()
                                register.status = 'DA_CAP'
                                register.default_user_name = user.username
                                register.default_password = user.password
                                register.save()
                                #TODO send an email about account information to customers.
                                account_info += str(id) + '-' + user.username + ','
                        message = u'Tạo tài khoản thành công'
                        success = True
                        data = simplejson.dumps({
                            'message': message,
                            'account_info': account_info,
                            'success': success
                        })
                        print data
                        return HttpResponse(data, mimetype='json')
                    except Exception as e:
                        print e
                        message = u'Tạo tài khoản không thành công'
                        success = False
                        data = simplejson.dumps({
                            'message': message,
                            'success': success
                        })
                        return HttpResponse(data, mimetype='json')
                else:
                    raise Exception("BadRequest")
        if sort_by_date: sort_by_date = '-'
        else: sort_by_date = ''
        if sort_by_status: sort_by_status = '-'
        else: sort_by_status = ''

        registers = Register.objects.order_by(sort_by_date+'register_date', sort_by_status+'status')
        if sort_by_date == '-': sort_by_date = 0
        else: sort_by_date = 1
        if sort_by_status == '-': sort_by_status = 0
        else: sort_by_status = 1
        context = RequestContext(request)
        return render_to_response(MANAGE_REGISTER, {
            'registers': registers,
            'short_by_date': sort_by_date,
            'short_by_status': sort_by_status
        }, context_instance = context)

    except Exception as e:
        print e
        raise e
# quyendt
@csrf_protect
@never_cache
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
                              context_instance=django.template.RequestContext(request, current_app=current_app))

# quyendt
def change_password_done(request):
    t = django.template.loader.get_template(os.path.join('app', 'change_password_done.html'))
    c = django.template.RequestContext(request)
    return HttpResponse(t.render(c))

# quyendt
@csrf_protect
@never_cache
def login(request, template_name='app/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):

    """
    login the system
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            log_action(request, form.get_user(), "logged in")

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    context = {
        'form': form,
        redirect_field_name: redirect_to
    }
    return render_to_response(template_name, context,
                              context_instance=django.template.RequestContext(request))

GMAIL_LOGIN = 'qlnt.feedback@gmail.com'
GMAIL_PASSWORD = 'freeschool2011'
def send_email(subject, message, from_addr=GMAIL_LOGIN, to_addr= None):
    msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587 
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN,GMAIL_PASSWORD)
    for to_address in to_addr:
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_address
        server.sendmail(from_addr, to_address, msg.as_string())
    server.close()

def feedback(request):
#hainhh
    print 0
    if request.method == 'POST': # If the form has been submitted...
        if request.is_ajax():
            url = 'url: ' + request.POST['feedback_url']
            user = 'user: ' + unicode(request.user)
            school = 'school: ' + unicode(get_school(request))
            content = request.POST['content']
            subject = u'[qlnt] User feedback'
            message = '\n'.join([url, user, school, content])
            #print message
            #send_email( subject = subject, message = message,
            #                          to_addr= ['vu.tran54@gmail.com', 'truonganhhoang@gmail.com'])
            Feedback.objects.create(content = content, title = url, email = school)
            thread.start_new_thread(send_email, (subject, message, GMAIL_LOGIN, ['vu.tran54@gmail.com', 'truonganhhoang@gmail.com','luulethe@gmail.com']))
            return HttpResponse(simplejson.dumps({'success': True}), mimetype='json')
        else:
            form = FeedbackForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                c = Feedback(fullname = form.cleaned_data['fullname'] ,
                             phone = form.cleaned_data['phone'],
                             email = form.cleaned_data['email'],
                             title = form.cleaned_data['title'],
                             content = form.cleaned_data['content'],
                             )
                c.save()
                return HttpResponseRedirect('/app/contact') # Redirect after POST
    else:
        form = FeedbackForm() # An unbound form

    return render_to_response('contact.html', {'form': form}, django.template.RequestContext(request))

def reset_password_request(request):
    #hainhh
    '''send a link to reset password to user's email'''
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = get_username(form.cleaned_data['email'])
            if username == '':
                # email is not in database
                #todo
                print 'invalid'
            else:
                code = str(random.randint(0,10000000))
                r = ResetPassword(username = username, code = code)
                r.save()
                #sendMail() #todo

def is_reset_pass_request_valid(username, code):
    return False
    #todo

def reset_password(request):
    '''reset password if email is valid'''
    if request.method == 'GET':
        username = request.GET[username]
        code = request.GET['code']
        if is_reset_pass_request_valid(username, code):
            password = str(random.randint(0,1000000))
