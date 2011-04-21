#sua mot chut model de lam tren 1 database

from django.db import models
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from datetime import date
GENDER_CHOICES = ((u'M', u'Nam'),(u'F', u'Nu'),)
TERM_CHOICES = ((1, u'1'), (2, u'2'),(3, u'3'),)
HK_CHOICES = ((u'T', u'Tot'), (u'K', u'Kha'),(u'TB',u'Trung Binh'),(u'Y', u'Yeu'),)
#validate mark of pupil
#mark must be between 0 and 10
def validate_mark(value):
    if value < 0 or value > 10:
        raise ValidationError(u'mark must between 0 and 10')

#validate the phone format
def validate_phone(value):
    if len(value) <= 5:
        raise ValidationError(u'Phone must have more than 5 digit')
    try:
        int(value)
    except ValueError:
        raise ValidationError(u'Invalid phone format')

#validate birthday. set range between 1990 and current year
def validate_birthday(value):
	if value < date(1900,1,1) or value > date.today():
		raise ValidationError(u'Invalid date range')

#validate the year that pupil go to class 1. Ragne between 1990 and this year
def validate_year(value):
    if value < 1990 or value > date.today().year:
        raise ValidationError(u'Invalid year value')

#validate he so diem cua mon    
def validate_hs(value):
	if value <= 0:
		raise ValidationError(u'hs must be larger than 0')
	       
class School(models.Model):
    
	#school_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 200, unique = True)
	address = models.CharField(max_length = 200, blank = True)
	phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	web_site = models.URLField(null = True, blank = True)
	
	def __unicode__(self):
		return self.name	
    
	#class Admin: pass

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School

class BasicPersonInfo(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45, blank = True) # tach ra first_name and last_name de sort va import from excel file
	birthday = models.DateField(null = True, validators = [validate_birthday])
	birth_place = models.CharField(max_length = 200, null = True, blank = True)
	sex = models.CharField(max_length = 2, choices = GENDER_CHOICES, blank = True, default = 'M')
	phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	current_address = models.CharField(max_length = 200, blank = True, null = True)
	email = models.EmailField(null = True, blank = True)
	
	class Meta:
		abstract = True
		
	def __unicode__(self):
		return self.first_name + self.last_name
		
	#class Admin: pass

class Teacher(BasicPersonInfo): pass

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher

class Year(models.Model):
    time = models.DateField() # date field but just use Year
    school_id = models.ForeignKey(School)
    
class StartYear(models.Model):
    time = models.DateField() # date field but use Year only
    school_id = models.ForeignKey(School)
    
class Term(models.Model):
    number = models.IntegerField(max_length=1, choices = TERM_CHOICES)
    year_id= models.ForeignKey(Year)
    def __unicode__(self):
		return str(self.number)
	#class Admin: pass

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
 

class Class(models.Model):
    
    #cai nay sau cung bo di    
	#class_code = models.CharField(max_length = 20, unique = True)    
	name = models.CharField(max_length = 20)
	year_id = models.ForeignKey(Year)
	khoi = models.IntegerField(max_length = 2)
	teacher = models.IntegerField() #lien ket den giao vien chu nhiem
	
	def __unicode__(self):
		return self.name
	#class Admin: pass
    
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
	    
class Pupil(BasicPersonInfo):
    	
    year = models.IntegerField(validators = [validate_year]) #year that pupil go to class 1    
    #cai nay t nghi co the bo di
    #pupil_code = models.CharField(max_length = 20, unique = True)
    current_status = models.CharField(max_length = 200, null = True, default = 'OK')	
    home_town = models.CharField(max_length = 100, null = True, blank = True) #nguyen quan
    disable = models.BooleanField(default = False)
    father_name = models.CharField(max_length = 45, blank = True)
    father_birthday = models.DateField( null = True, blank = True)
    father_phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
    father_job = models.CharField(max_length = 100, null = True, blank = True)
    mother_name = models.CharField(max_length = 45, blank = True)
    mother_birthday = models.DateField(null = True, blank = True)
    mother_job = models.CharField(max_length = 100, null = True, blank = True)    
    mother_phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
    #cay nay sau cung bo di dc
    start_year_id = models.ForeignKey(StartYear)
    class_id = models.ForeignKey(Class)

class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil


class Subject(models.Model):    
    name = models.CharField(max_length = 45) # can't be null
    hs = models.FloatField( validators = [validate_hs])
    loai = models.IntegerField(max_length = 3)
    #subject_code = models.CharField(max_length = 15, unique = True) # can't be null
    class_id = models.ForeignKey(Class)    
    teacher_id = models.ForeignKey(Teacher) # field nay de cung cap permission cho giao vien de nhap diem
    term_id = models.ForeignKey(Term)    
	
    def __unicode__(self):
		return self.name
	
	#class Admin: pass

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject

class Mark(models.Model):
    
    mieng_1 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mieng_2 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mieng_3 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mieng_4 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mieng_5 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mlam_1 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mlam_2 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mlam_3 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mlam_4 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mlam_5 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mot_tiet_1 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mot_tiet_2 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mot_tiet_3 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mot_tiet_4 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    mot_tiet_5 = models.FloatField( null = True, blank = True, validators = [validate_mark])
    ck = models.FloatField( null = True, blank = True, validators = [validate_mark])
    tb = models.FloatField( null = True, blank = True, validators = [validate_mark])
    tb_nam = models.FloatField( null = True, blank = True, validators = [validate_mark])
	# all fields can be null
    
    subject_id = models.ForeignKey(Subject)
    #sua cho nay
    student_id = models.ForeignKey(Pupil)    	
	#class Admin: pass

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        
class KhenThuong(models.Model):
    student_id = models.ForeignKey(Pupil)
    term_id = models.ForeignKey(Term)
    time = models.DateField(blank = True)
    danh_hieu = models.CharField(max_length = 100)
    place= models.CharField(max_length = 100, blank = True)
    des = models.CharField(max_length = 400, blank = True) # description
    
class KiLuat(models.Model):
    student_id = models.ForeignKey(Pupil)
    term_id = models.ForeignKey(Term)
    time = models.DateField(blank = True)
    hinh_thuc = models.CharField(max_length = 100)
    des = models.CharField(max_length = 400, blank = True) # description

class HanhKiem(models.Model):
    student_id = models.ForeignKey(Pupil)
    term_id = models.ForeignKey(Term)
    loai = models.CharField( max_length = 2, choices = HK_CHOICES, default = 'K')    

class TBNam(models.Model):
    student_id = models.ForeignKey(Pupil)
    term_id = models.ForeignKey(Term)
    tb_nam = models.FloatField( validators = [validate_mark])
