from django.db import models
GENDER_CHOICES = ((u'M', u'Nam'),(u'F', u'Nu'),)

class School(models.Model):
	school_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 200, unique = True)
	address = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 15, null = True)
	web = models.URLField(null = True)

class CommonInfo(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45) # tach ra first_name and last_name de sort va import from excel file
   birthday = models.DateField()
	birth_place = models.CharField(max_length = 200)
	sex = models.CharField(max_length = 2, choices = GENDER_CHOICES)
	phone = models.CharField(max_length = 15, null = True)
	current_address = models.CharField(max_length = 200)
	email = models.EmailField(null = True)
	class Meta:
		abstract = True
		
class Teacher(CommonInfo): pass
	
class Class(models.Model):
	class_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 20)
	school_id = models.ForeignKey(School)
	teacher_id = models.ForeignKey(Teacher)
	
class Pupil(CommonInfo):
	year = models.IntegerField()
	pupil_code = models.CharField(max_length = 20, unique = True)
	current_status = models.CharField(max_length = 200, blank = True)
	home_town = models.CharField(max_length = 100) #nguyen quan
	disable = models.BooleanField(default = FALSE)
	father_name = models.CharField(max_length = 45)
	father_birthday = models.DateField()
	father_phone = models.CharField(max_length = 15, null = True)
	father_job = models.CharField(max_length = 100)
	mother_name = models.CharField(max_length = 45)
	mother_birthday = models.DateField()
	mother_phone = models.CharField(max_length = 15, null = True)
	mother_job = models.CharField(max_length = 100)
	school_id = models.ForeignKey(School)
	class_id = models.ForeignKey(Class)