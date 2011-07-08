from persistent_messages import notify
from persistent_messages import constants 

def add_message(request, level, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None, expires=None, close_timeout=None):
    """
    """
    if email:
        notify.email(level, message, extra_tags, subject, user, from_user)
    return request._messages.add(level, message, extra_tags, subject, user, from_user, expires, close_timeout)

def internal(request, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None, expires=None, close_timeout=None):
    """
    """
    level = constants.INTERNAL
    return add_message(request, level, message, extra_tags, fail_silently, subject, user, email, from_user, expires, close_timeout)

def sms(request, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None, expires=None, close_timeout=None):
    """
    """
    level = constants.SMS
    return add_message(request, level, message, extra_tags, fail_silently, subject, user, email, from_user, expires, close_timeout)

#def debug(request, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None, expires=None, close_timeout=None):
#    """
#    """
#    level = constants.DEBUG
#    return add_message(request, level, message, extra_tags, fail_silently, subject, user, email, from_user, expires, close_timeout)
