from django.db import models
GENDER_CHOICES = ((u'M', u'Nam'),(u'F', u'Nu'),)
TERM_CHOICES = (('1', '1'), ('2','2'),('3','3'))
class School(models.Model):
	school_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 200, unique = True)
	address = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 15, null = True)
	web_site = models.URLField(null = True)
	
	def __unicode__(self):
		return self.name

	def __unicode__(self):
		return self.name
		

class BasicPersonInfo(models.Model):
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
	def __unicode__(self):
		return self.first_name + self.last_name
		
	def __unicode__(self):
		return self.first_name + self.last_name 

class Teacher(BasicPersonInfo): pass

class Class(models.Model):
	class_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 20)
	school_id = models.ForeignKey(School)
	teacher_id = models.ForeignKey(Teacher) 
	def __unicode__(self):
		return self.name
	def __unicode__(self):
		return self.name
class Pupil(BasicPersonInfo):
	year = models.IntegerField()
	pupil_code = models.CharField(max_length = 20, unique = True)
	current_status = models.CharField(max_length = 200, blank = True)
	home_town = models.CharField(max_length = 100, blank = True) #nguyen quan
	disable = models.BooleanField(default = False)
	father_name = models.CharField(max_length = 45)
	father_birthday = models.DateField( null = True)
	father_phone = models.CharField(max_length = 15, blank = True)
	father_job = models.CharField(max_length = 100, blank = True)
	mother_name = models.CharField(max_length = 45)
	mother_birthday = models.DateField(null = True)
	mother_phone = models.CharField(max_length = 15, blank = True)
	mother_job = models.CharField(max_length = 100, blank = True)
	school_id = models.ForeignKey(School)
	class_id = models.ForeignKey(Class)

class Term(models.Model):
	number = models.IntegerField(choices = TERM_CHOICES)
	time = models.DateField(auto_now = True)

	def __unicode__(self):
		return self.number
	
class Subject(models.Model):
	subject_code = models.CharField(max_length = 15, unique = True) # can't be null
	class_code = models.CharField(max_length = 15, unique = True) # can't be null
	name = models.CharField(max_length = 45) # can't be null
	hs_m = models.FloatField( null = True)
	hs_15= models.FloatField( null = True)
	hs_45= models.FloatField( null = True)
	hs_ck= models.FloatField( null = True)
	#this field can be omitted at this iteration.
	teacher_id = models.IntegerField() # field nay de cung cap permission cho giao vien de nhap diem
	term_id = models.ForeignKey(Term)
	
	def __unicode__(self):
		return self.name
	
class Mark(models.Model):
	student_code = models.CharField(max_length = 15) # will link with pupil table from default db
	mieng_1 = models.FloatField( null = True)
	mieng_2 = models.FloatField( null = True)
	mieng_3 = models.FloatField( null = True)
	mieng_4 = models.FloatField( null = True)
	mieng_5 = models.FloatField( null = True)
	mlam_1 = models.FloatField( null = True)
	mlam_2 = models.FloatField( null = True)
	mlam_3 = models.FloatField( null = True)
	mlam_4 = models.FloatField( null = True)
	mlam_5 = models.FloatField( null = True)
	mot_tiet_1 = models.FloatField( null = True)
	mot_tiet_2 = models.FloatField( null = True)
	mot_tiet_3 = models.FloatField( null = True)
	mot_tiet_4 = models.FloatField( null = True)
	mot_tiet_5 = models.FloatField( null = True)
	ck = models.FloatField( null = True) # cuoi ky
	tb = models.FloatField( null = True) # trung binh
	# all fields can be null
	subject_id = models.ForeignKey(Subject)