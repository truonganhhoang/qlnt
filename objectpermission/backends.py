from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from objectpermission.models import ObjectPermission

class ObjectPermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, value=None):
        """ perm parameter must has value like:
        table_name.field_name_permission
        Eg: Organization.name_view
        """
        if not user_obj.is_authenticated():
            user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        if value is None:
            return False

        try:
            table_name = perm.split('.')[0]
            field_name = perm.split('.')[1].split('_')[0]
            permission = perm.split('.')[1].split('_')[-1]
        except IndexError:
            return False

        p = ObjectPermission.objects.filter(user=user_obj,
                                            table_name=table_name,
                                            field_name=field_name,
                                            value=value)
        return p.filter(**{'can_%s' % permission: True}).exists()
