from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from objectpermission.models import ObjectPermission

class ObjectPermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, perm_info=None):
        if not user_obj.is_authenticated():
            user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        if obj is None:
            return False

        try:
            perm = perm.split('.')[-1].split('_')[0]
            print perm
        except IndexError:
            return False

        p = ObjectPermission.objects.filter(content_type=ct,
                                            object_id=obj.id,
                                            user=user_obj)
        return p.filter(**{'can_%s' % perm: True}).exists()
