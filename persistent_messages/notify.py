# -*- coding: utf-8 -*-
from django.core.mail import send_mail

def email(level, message, extra_tags, subject, user, from_user):
    if not user or not user.email:
        raise Exception('Người sử dụng phải đăng ký email để nhận được thông báo.')
    
    send_mail(subject, message, from_user.email if from_user else None, [user.email], fail_silently=False)

def sms(level, message, extra_tags, subject, user, from_user):
    if not user or not user.email:
        raise Exception('Người sử dụng phải đăng ký điện thoại di động để nhận được thông baó.')
    
    #TODO send sms.
