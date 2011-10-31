# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import sms
from school.utils import *
import os
import datetime
import urllib
import urllib2
from suds.client import Client
#from SOAPpy import SOAPProxy, HTTPTransport, Config

from django.conf import settings
TEMP_FILE_LOCATION = settings.TEMP_FILE_LOCATION

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
#

def sendSMS(phone,content,user):
    try:
        phone = checkValidPhoneNumber(phone)
    except Exception as e:
        raise e
    try:
        school = user.userprofile.organization
        if phone:
            from suds.client import Client
            url = settings.SMS_WSDL_URL
            username = settings.WSDL_USERNAME
            password = settings.WSDL_PASSWORD
            mt_username = settings.MT_USERNAME
            mt_password = settings.MT_PASSWORD
            time = '/'.join([str(datetime.date.today().day),
                             str(datetime.date.today().month),
                             str(datetime.date.today().year) ])
            content =to_en1(u'Trường ' + unicode(school) + u': Ngày ' + str(time) + u'TK:' +
                            unicode(user)  + '.\n' + content)
            s = sms(phone=phone, content=content, sender=user, recent=True, success=True)
            s.save()

            client = Client(url, username = username, password = password)
            message = \
        '''<?xml version="1.0" encoding="UTF-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <InsertMT xmlns="http://tempuri.org/">
      <User>%s</User>
      <Pass>%s</Pass>
      <CPCode>160</CPCode>
      <RequestID>4</RequestID>
      <UserID>%s</UserID>
      <ReceiveID>%s</ReceiveID>
      <ServiceID>8062</ServiceID>
      <CommandCode>CNHN1</CommandCode>
      <ContentType>0</ContentType>
	<Info>%s</Info>
    </InsertMT>
  </soap12:Body>
</soap12:Envelope>''' % (mt_username, mt_password, phone, phone, content)
            return client.service.InsertMT(__inject= {'msg': str(message)})
        else:
            raise Exception("InvalidPhoneNumber")
    except Exception as e:
        print e
        raise e

def checkValidPhoneNumber(phone):
    if not int(phone[0]):
        phone = '84' + phone[1:]
        return phone
    elif phone[:2] != '84':
        return None
    else:
        return phone
        


def getUserFromPhone(phone):
    user_list = User.objects.all()
    for u in user_list:
        try:
            if phone == u.get_profile().phone:
                return u
        except Exception as e:
            pass
    return ""


def save_file(file):
    saved_file = open(os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls'), 'wb+')
    for chunk in file.chunks():
        saved_file.write(chunk)
    saved_file.close()
    return 'sms_input.xls'
