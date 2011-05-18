# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ObjectPermissionManager(models.Manager):
    def create_permission(self, owner, permission, model, condition):
        owner_ct = ContentType.objects.get_for_model(owner)
        model_ct = ContentType.objects.get_for_model(model)
        field_name = condition.split('=')[0]
        allowed_value = condition.split('=')[1]
        return ObjectPermission.objects.create(owner_id=owner.id, owner_ct=owner_ct, permission=permission, model_ct=model_ct, field_name=field_name, allowed_value=allowed_value)

class ObjectPermission(models.Model):
    owner_id = models.PositiveIntegerField()
    owner_ct = models.ForeignKey(ContentType, related_name='owner_ct')
    owner = generic.GenericForeignKey('owner_ct', 'owner_id')
    permission = models.CharField(max_length=255) # vi du: vote, view, change
    model_ct = models.ForeignKey(ContentType, related_name='model_ct')
    field_name = models.CharField(max_length=255)
    allowed_value = models.CharField(max_length=255)

    objects = ObjectPermissionManager()
    
    class Meta:
        verbose_name_plural = "Phân quyền đối tượng"
        unique_together = ('owner_id', 'owner_ct', 'model_ct', 'field_name', 'allowed_value', 'permission')
        
    def __unicode__(self):
        return '%s | %s | %s | %s=%s' % (self.owner, self.permission, \
                         self.model_ct, self.field_name, self.allowed_value)
