from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class PermissionInfo(models.Model):
    table_name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)

class AllowedValues(models.Model):
    value = models.CharField(max_length=255)
    perm_info = models.ForeignKey(PermissionInfo)

class ObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    perm_info = models.OneToOneField(PermissionInfo)
