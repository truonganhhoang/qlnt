from django.db import models
GENDER_CHOICES = ((u'Nam', u'Nam'),(u'Nu', u'Nu'),)

class School(models.Model):
	school_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 200, unique = True)
	address = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 15)
	web = models.URLField()
	
class Teacher(models.Model):
	name = models.CharField(max_length = 45)
	birthday = models.DateField()
	birth_place = models.CharField(max_length = 200)
	sex = models.CharField(max_length = 4, choices = GENDER_CHOICES)
	phone = models.CharField(max_length = 15)
	current_address = models.CharField(max_length = 200)
	email = models.EmailField()
	
class Class(models.Model):
	class_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 20)
	school_id = models.ForeignKey(School)
	teacher_id = models.ForeignKey(Teacher)
	
class Pupil(models.Model):
	name = models.CharField(max_length = 45)
	birthday = models.DateField()
	sex = models.CharField(max_length = 4, choices = GENDER_CHOICES)
	year = models.IntegerField()
	pupil_code = models.CharField(max_length = 20, unique = True)
	current_status = models.CharField(max_length = 200)
	birth_place = models.CharField(max_length = 100)
	home_town = models.CharField(max_length = 100) #nguyen quan
	email = models.EmailField()
	disable = models.BooleanField(default = FALSE)
	current_address = models.CharField(max_length = 200)
	phone_number = models.CharField(max_length = 15)
	father_name = models.CharField(max_length = 45)
	father_birthday = models.DateField()
	father_phone = models.CharField(max_length = 15)
	father_job = models.CharField(max_leng = 100)
	mother_name = models.CharField(max_length = 45)
	mother_birthday = models.DateField()
	mother_phone = models.CharField(max_length = 15)
	mother_job = models.CharField(max_leng = 100)
	school_id = models.ForeignKey(School)
	class_id = models.ForeignKey(Class)