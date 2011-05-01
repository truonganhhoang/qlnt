from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class ObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    table_name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    allowed_value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'table_name', 'field_name', 'allowed_value')
