from django.db import models
from django import forms

class Organization(models.Model):
    ORGANIZATION_TYPE_CHOICES = (('T', 'Truong'),
                                 ('P', 'Phong'),
                                 ('S', 'So'))
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)
    email_adress = models.CharField(max_length=50)
    organization_type = models.CharField(max_length=2, choices=ORGANIZATION_TYPE_CHOICES)
    upper_organization = models.ForeignKey('self', blank=True, null=True)
    manager_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=1)
    adress = forms.CharField(max_length=255, min_length=1)
    phone_number = forms.CharField(max_length=40, min_length=9)
    email_adress = forms.EmailField()
    manager_name = forms.CharField(max_length=100, min_length=1)

class PositionType(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

# form validate for PositionType
class PositionTypeForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=1)

class User(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=40)
    #------------------------------ fax_number = models.CharField(max_length=50)
    email = models.EmailField()
    position = models.ForeignKey(PositionType)
    organization = models.ForeignKey(Organization)
    
    def __unicode__(self):
        return self.name

class UserForm(forms.ModelForm):
    class Meta:
        model = User

class SchoolYear(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    active_year = models.BooleanField()
    
    def __unicode__(self):
        return self.name

class SchoolYearForm(forms.Form):
    name = forms.CharField(max_length=100 , min_length=1)
    start_date = forms.DateField()
    end_date = forms.DateField()
    active_year = forms.BooleanField()

class Semester(models.Model):
    name = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear)
#    school_id = models.ForeingKey(School)
    start_date = models.DateField()
    end_date = models.DateField()
    post_start_date = models.DateField()
    post_end_date = models.DateField()
    does_grades = models.CharField(max_length=300)
    does_exam = models.CharField(max_length=100)
    does_comments = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.name

class SemesterForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=1)
    start_date = forms.DateField()
    end_date = forms.DateField()
    post_start_date = forms.DateField()
    post_end_date = forms.DateField()
    does_grades = forms.CharField(max_length=300, min_length=1)
    does_exam = forms.CharField(max_length=100, min_length=1)
    does_comments = forms.CharField(max_length=500, min_length=1)

class SchoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['upper_organization'].choices = [(-1, '----------')] + [(i.id, i.name) for i in Organization.objects.all() \
                                                                            if i.organization_type == 'S' or i.organization_type == 'P']
    
    name = forms.CharField(max_length=100, min_length=1)
    address = forms.CharField(max_length=255, min_length=1)
    phone_number = forms.CharField(max_length=40, min_length=9)
    upper_organization = forms.ChoiceField()
