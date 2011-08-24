# -*- coding: utf-8 -*-


from school.forms import *
from school.school_settings import *
from sms.views import *
#from SOAPpy import WSDL


SYNC_RESULT = os.path.join('helptool','recover_marktime.html')
SYNC_SUBJECT = os.path.join('helptool','sync_subject.html')



def recover_marktime(request):
    
    marks = Mark.objects.all()
    number_of_defect = 0
    
    if request.method == 'POST':
        for mark in marks:
            try:
                temp = mark.marktime
            except Exception as e:
                a = MarkTime()
                a.mark_id = mark
                a.save()
                number_of_defect +=1
        message = u'Bạn vừa tạo ' + str(number_of_defect) + u' MarkTime records'
    else:
        for mark in marks:
            try:
                temp = mark.marktime
            except Exception as e:
                number_of_defect += 1
        message = u'Thiếu ' + str(number_of_defect) + u'MarkTime records'
    context = RequestContext(request)
    return render_to_response( SYNC_RESULT, { 'message' : message},
                               context_instance = context )
@transaction.commit_on_success
def sync_index(request):

    classes = Class.objects.all()
    message = ''
    try:
        for _class in classes:
            students = _class.pupil_set.order_by('first_name', 'last_name')
            index = 0
            for student in students:
                index +=1
                print index
                if not student.first_name.strip():
                    message += '\n' + student.last_name + ': wrong name'
                    names = student.last_name.strip().split(' ')
                    last_name = ' '.join(names[:len(names)-1])
                    first_name = names[len(names)-1]
                    try:
                        student.first_name = first_name
                        student.last_name = last_name
                        student.save()
                    except Exception as e:
                        print e
                if student.index != index:
                    student.index = index
                    student.save()

    except Exception as e:
        print e
    message += '\n' + u'Sync xong index.'
    context = RequestContext(request)
    return render_to_response( SYNC_RESULT, { 'message' : message},
                               context_instance = context )

@transaction.commit_on_success
def sync_subject(request):
    classes = Class.objects.all()
    print classes
    message = ''
    number = 0
    try:
        if request.method == 'GET':
            print 'get'
            for _class in classes:
                if not _class.subject_set.count():
                    number+=1
            print 'message'
            message = u'<p>Have ' + str(number) + ' classes those have no subject.</p>'

            number = 0
            subjects = Subject.objects.all()
            for subject in subjects:
                if subject.primary:
                    number += 1
            message += u'<br><p>%s subjects in database have non zero primary </p>' % number
        elif  request.method == 'POST':
            print 'POST'
            if 'sync' in request.POST:
                for _class in classes:
                    school = _class.year_id.school_id
                    if not school.status:
                        school.status = 1
                        school.save()
                    if school.school_level == '1': ds_mon_hoc = CAP1_DS_MON
                    elif school.school_level == '2': ds_mon_hoc = CAP2_DS_MON
                    elif school.school_level == '3': ds_mon_hoc = CAP3_DS_MON
                    else: raise Exception('SchoolLevelInvalid')

                    if not _class.subject_set.count():
                        index = 0
                        for mon in ds_mon_hoc:
                            index +=1
                            print index
                            add_subject(subject_name= mon, subject_type= mon, _class=_class, index=index)
                message = '<p>Syncing subject from all classes: Done </p>'
                print 'tag'
                subjects = Subject.objects.all()
                for subject in subjects:
                    if subject.primary == 1:
                        subject.primary = 0
                        subject.save()
                message += "<br><p>Syncing subject's primary: Done</p>"
        context = RequestContext(request)
        return render_to_response(SYNC_SUBJECT, {'message': message, 'number': number},
                                  context_instance = context)
    except Exception as e:
        print e

@transaction.commit_on_success
def sync_subject_type(request):
    message = ''
    number = 0
    try:
        if request.method == 'GET':
            print 'get'
            number = 0
            subjects = Subject.objects.all()
            for subject in subjects:
                if not subject.type:
                    number += 1
            message += u'<br><p>%s subjects in database do not have correct type </p>' % number
        elif  request.method == 'POST':
            print 'POST'
            if 'sync' in request.POST:
                print 'tag'
                subjects = Subject.objects.all()
                for subject in subjects:
                    if not subject.type:
                        if subject.name.lower() == u'Giáo dục quốc phòng'.lower():
                            subject.type = u'GDQP-AN'
                        elif subject.name.lower() == u'Giáo dục công dân'.lower():
                            subject.type = u'GDCD'
                        else:
                            subject.type = subject.name
                        subject.save()
                message += "<br><p>Syncing subject's type: Done</p>"
        context = RequestContext(request)
        return render_to_response(SYNC_SUBJECT, {'message': message, 'number': number},
                                  context_instance = context)
    except Exception as e:
        print e

@transaction.commit_on_success
def sync_subject_primary(request):
    subjects = Subject.objects.all()
    for subject in subjects:
        if subject.primary:
            subject.primary = 0
            subject.save()
    message = "Syncing subject's primary is done"
    context = RequestContext(request)
    return render_to_response( SYNC_RESULT, { 'message' : message},
                               context_instance = context )





#class myHTTPTransport(HTTPTransport):
#    username = None
#    password = None
#    @classmethod
#    def setAuthen(cls, u, p):
#        cls.username = u
#        cls.password = p
#    def call(self, addr, data, namespace, soapaction=None,
#             encoding=None, http_proxy=None, config=Config, timeout=None):
#        if not isinstance(addr, SOAPAddress):
#            addr=SOAPAddress(addr, config)
#        if self.username != None:
#            addr.user = self.username + ':' + self.password
#        return HTTPTransport.call(self, addr, data, namespace, soapaction, encoding, http_proxy, config, timeout)
