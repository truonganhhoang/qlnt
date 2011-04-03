from django.db import models
from django.forms import ModelForm

# School year model
class SchoolYear (models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField (blank=True, null=True)
    end_date = models.DateField (blank=True, null=True)

# Time table model
class TimeTable(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    apply_date = models.DateField()
    comment = models.TextField()
    locked = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
class TimeTableForm(ModelForm):
    class Meta:
        model = TimeTable
