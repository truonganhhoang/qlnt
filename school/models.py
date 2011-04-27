# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from datetime import date

GENDER_CHOICES = ((u'M', u'Nam'),(u'F', u'Nữ'),)
TERM_CHOICES = ((1, u'1'), (2, u'2'),(3, u'3'),)
HK_CHOICES = ((u'T', u'Tốt'), (u'K', u'Khá'),(u'TB',u'Trung Bình'),(u'Y', u'Yếu'),)
HL_CHOICES = ((u'G', u'Giỏi'), (u'K', u'Khá'),(u'TB',u'Trung Bình'),(u'Y', u'Yếu'),(u'Kem', u'Kém'))
#k co nghia la khong duoc danh hieu gi
DH_CHOICES = ((u'XS', u'học sinh xuất sắc'),(u'G', u'hoc sinh giỏi'), (u'TT', u'hoc sinh tiên tiến'),(u'k',u''))

SCHOOL_LEVEL_CHOICE = ((1, u'1'), (2, u'2'), (3, u'3'))
DIEM_DANH_TYPE = ((u'C', u'Có phép'),(u'K', u'Không phép'),(u'BT', u'Bỏ tiết'))
BAN_CHOICE = ((u'KHTN',u'Ban KHTN'),(u'KHXH',u'Ban KHXH-NV'),(u'CBA',u'Ban Cơ bản A'),
			  (u'CBB',u'Ban Cơ bản B'),(u'CBB',u'Ban Cơ bản C'),
			  (u'CBD',u'Ban Cơ bản D'),(u'CB',u'Ban Cơ bản'))
KHOI_CHOICE=((1,u'Khối 1'),(2,u'Khối 2'),(3,u'Khối 3'),(4,u'Khối 4'),(5,u'Khối 5'),(6,u'Khối 6'),(7,u'Khối 7'),			 
			(8,u'Khối 8'),(9,u'Khối 9'),(10,u'Khối 10'),(11,u'Khối 11'),(12,u'Khối 12'))			
KV_CHOICE =((u'1',u'KV1'),(u'2A','KV2'),(u'2B','KV2-NT'),(u'3',u'KV3'))
DT_CHOICE = ((1,u'Kinh (Việt)'),(2,u'Tày'),(3,u'Nùng'),(4,u'Hmông (Mèo)'),(5,u'Mường'),(6,u'Dao'),(7,u'Khmer'),
			(8,u'Êđê'),(9,u'CaoLan'),(10,u'Thái'),(11,u'Gia rai'),(12,u'La chư'),(13,u'Hà nhì'),(14,u'Giáy'),
			(15,u"M'nông"),(16,u'Cơ tu'),(17,u'Xê đăng'),(18,u"X'tiêng"),(19,u"Ba na"),(20,"H'rê"),(21,u'Giê-Triêng'),
			(22,u'Chăm'),(23,u'Cơ ho'),(24,u'Mạ'),(25,u'Sán Dìu'),(26,u'Thổ'),(27,u'Khơ mú'),(28,u'Bru - Vân Kiều'),
			(29,u'Tà ôi'),(30,u'Co'),(31,u'Lào'),(32,u'Xinh mun'),(33,u'Chu ru'),(35,u'Phù lá'),(36,u'La hú'),(37,u'Kháng'),
			(38,u'Lự'),(39,u'Pà Thén'),(40,u'Lô lô'),(41,u'Chứt'),(42,u'Mảng'),(43,u'Cơ lao'),(44,u'Bố y'),(45,u'La ha'),
			(46,u'Cống'),(47,u'Ngái'),(48,u'Si la'),(49,u'Pu Péo'),(50,u'Brâu'),(51,u'Rơ măm'),(52,u'Ơ đu'),(53,u'Hoa'),
			(54,u'Raglay'),(55,u'HMông'),(56,u'Pacô'),(57,u'Pahy'),(60,u'Jơ lơng'),(61,u'Rơ ngao'),(62,u'Ra dong'),
			(63,u'Sơ rá'),(64,u'Jẻ'),(65,u'Mơ nâm'),(66,u'Hơ lăng'),(67,u'Hoa (Hán)'),(68,u'Sán chay (Cao Lan, Sán Chỉ)'),
			(69,u'CaDong'),(70,u'Chơ ro'))
LENLOP_CHOICES=((True,u'Được lên lớp'),(False,u'Không được lên lớp'))
#validate mark of pupil
#mark must be between 0 and 10
def validate_mark(value):
	if value < 0 or value > 10:
		raise ValidationError(u'Điểm phải nằm trong khoảng từ 0 đến 10')

#validate the phone format
def validate_phone(value):
	if len(value) <= 5:
		raise ValidationError(u'Điện thoạt phải có trên 5 chữ số')
	try:
		int(value)
	except ValueError:
		raise ValidationError(u'Không đúng định dạng')

#validate birthday. set range between 1990 and current year
def validate_birthday(value):
	if value < date(1900,1,1) or value > date.today():
		raise ValidationError(u'Ngày nằm ngoài khoảng cho phép')

#validate the year that pupil go to class 1. Ragne between 1990 and this year
def validate_year(value):
	if value < 1990 or value > date.today().year:
		raise ValidationError(u'Năm nằm ngoài khoảng cho phép')

#validate the date that pupil join school
def validate_join_date(value):
	if value < date(1990,1,1):
		raise ValidationError(u'Ngày nằm ngoài khoảng cho phép')
		
#validate he so diem cua mon	
def validate_hs(value):
	if value <= 0:
		raise ValidationError(u'hs must be larger than 0')
		
#validator for class->khoi
def validate_khoi(value):
	if not ( 1<= value <= 12 ):
		raise ValidationError(u'khoi must be between 1 and 12')

class School(models.Model):
	
	#school_code = models.CharField(max_length = 20, unique = True)
	name = models.CharField(max_length = 200, unique = True)
	address = models.CharField(max_length = 200, blank = True)
	phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	web_site = models.URLField(null = True, blank = True)
	school_level = models.IntegerField( choices = SCHOOL_LEVEL_CHOICE )
	
	def __unicode__(self):
		return self.name	
	
	#class Admin: pass

class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
	#cac khoi trong 1 truong	
class Block(models.Model):
	number=models.SmallIntegerField(max_length = 2, choices=KHOI_CHOICE)
	school_id = models.ForeignKey(School)
	
	def __unicode__(self):
		return str(self.number)	
	
class BlockForm(forms.ModelForm):
	class Meta:
		model = Block
class BasicPersonInfo(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45, blank = True) # tach ra first_name and last_name de sort va import from excel file
	birthday = models.DateField(null = True, validators = [validate_birthday])
	birth_place = models.CharField(max_length = 200, null = True, blank = True)
	dan_toc = models.IntegerField(choices = DT_CHOICE, blank = True, null = True, default = 1)
	ton_giao = models.CharField(max_length = 20, blank = True, null = True)
	quoc_tich = models.CharField(max_length = 20, blank = True, null = True, default = 'Viet Nam')
	home_town = models.CharField(max_length = 100, null = True, blank = True) #nguyen quan
	sex = models.CharField(max_length = 2, choices = GENDER_CHOICES, blank = True, null = True, default = 'M')
	phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	current_address = models.CharField(max_length = 200, blank = True, null = True)
	email = models.EmailField(null = True, blank = True)
	
	class Meta:
		abstract = True
		
	def __unicode__(self):
		return self.last_name + " " + self.first_name
		
	#class Admin: pass

class Teacher(BasicPersonInfo): 
	school_id = models.ForeignKey(School,null=True,blank=True)

class TeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher

class Year(models.Model):
	time = models.DateField() # date field but just use Year
	school_id = models.ForeignKey(School)
	
	def __unicode__(self):
		return str(self.time.year)+"-"+str(self.time.year+1)
class StartYear(models.Model):
	time = models.DateField() # date field but use Year only   
	school_id = models.ForeignKey(School)
	def __unicode__(self):
		return str(self.time.year)
	
class Term(models.Model):
	number = models.IntegerField(max_length=1, choices = TERM_CHOICES)
	year_id= models.ForeignKey(Year)
	def __unicode__(self):
		return str(self.number)+" "+str(self.year_id.time.year)		 
	#class Admin: pass

class TermForm(forms.ModelForm):
	class Meta:
		model = Term

class Class(models.Model):
	
	#cai nay sau cung bo di	
	#class_code = models.CharField(max_length = 20, unique = True)	
	name = models.CharField(max_length = 20)
	year_id = models.ForeignKey(Year)
	#lop nay thuoc khoi nao
	block_id = models.ForeignKey(Block)
	teacher_id = models.ForeignKey(Teacher,null=True,blank=True) #field nay chi dung de phan quyen, vi vay chi gan 1 gia tri nhan dang
	
	def __unicode__(self):
		return self.name
	#class Admin: pass
	
class ClassForm(forms.ModelForm):
	class Meta:
		model = Class
		
class Pupil(BasicPersonInfo):
		
	year = models.IntegerField(validators = [validate_year], blank = True, null = True) #year that pupil go to class 1
	school_join_date = models.DateField(default = date.today(),validators=[validate_join_date])
	ban_dk = models.CharField(max_length = 5, choices = BAN_CHOICE)
	school_join_mark = models.IntegerField(null = True, blank = True)
	#thong tin ca nhan
	khu_vuc = models.CharField(max_length = 3, choices = KV_CHOICE, blank = True, null = True)
	doan = models.BooleanField(blank = True, default = False)
	ngay_vao_doan = models.DateField(blank = True, null = True)
	doi = models.BooleanField(blank = True, default = False)
	ngay_vao_doi = models.DateField(blank = True, null = True)
	dang = models.BooleanField(blank = True, default = False)
	ngay_vao_dang = models.DateField(blank = True, null = True)
		
	#thong tin gia dinh
	father_name = models.CharField(max_length = 45, blank = True, null = True)
	father_birthday = models.DateField( null = True, blank = True)
	father_phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	father_job = models.CharField(max_length = 100, null = True, blank = True)
	mother_name = models.CharField(max_length = 45, blank = True, null = True)
	mother_birthday = models.DateField(null = True, blank = True)
	mother_job = models.CharField(max_length = 100, null = True, blank = True)	
	mother_phone = models.CharField(max_length = 15, null = True, blank = True, validators = [validate_phone])
	
	current_status = models.CharField(max_length = 200, blank = True, null = True, default = 'OK')
	disable = models.BooleanField(default = False)
	start_year_id = models.ForeignKey(StartYear)
	class_id = models.ForeignKey(Class)

class PupilForm(forms.ModelForm):
	class Meta:
		model = Pupil


class Subject(models.Model):	
	name = models.CharField(max_length = 45) # can't be null
	hs = models.FloatField( validators = [validate_hs])

	class_id = models.ForeignKey(Class)	
	teacher_id = models.ForeignKey(Teacher) # field nay de cung cap permission cho giao vien de nhap diem
	
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
	
	subject_id = models.ForeignKey(Subject)
	student_id = models.ForeignKey(Pupil)		
	term_id	= models.ForeignKey(Term)
class TKMon(models.Model):	
	tb_nam = models.FloatField( null = True, blank = True, validators = [validate_mark])
	#danh dau xem mon nay co dc phep thi lai hay ko
	thi_lai = models.BooleanField(blank = True, default = False)
	diem_thi_lai=models.FloatField( null = True, blank = True, validators = [validate_mark])
	# all fields can be null
	
	subject_id = models.ForeignKey(Subject)
	student_id = models.ForeignKey(Pupil)		
	#class Admin: pass
	def __unicode__(self):
		return str(self.tb_nam)
	
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
	
	def __unicode__(self):
		return self.danh_hieu
	
class KiLuat(models.Model):
	student_id = models.ForeignKey(Pupil)
	term_id = models.ForeignKey(Term)
	time = models.DateField(blank = True)
	hinh_thuc = models.CharField(max_length = 100)
	des = models.CharField(max_length = 400, blank = True) # description
	
	def __unicode__(self):
		return self.hinh_thuc

class HanhKiem(models.Model):
	student_id = models.ForeignKey(Pupil)
	term_id = models.ForeignKey(Term)
	loai = models.CharField( max_length = 2, choices = HK_CHOICES, default = 'K')
	
	def __unicode__(self):
		return self.loai

class TBHocKy(models.Model):
	student_id = models.ForeignKey(Pupil)
	term_id = models.ForeignKey(Term)
	tb_hk=models.FloatField( validators = [validate_mark])		
	hl_hk=models.CharField( max_length = 3, choices = HL_CHOICES)
	danh_hieu_hk=models.CharField( max_length = 2, choices = DH_CHOICES)
	
	def __unicode__(self):
		return "%.2f" % self.tb_hk
		
class TBNam(models.Model):
	student_id = models.ForeignKey(Pupil)
	year_id = models.ForeignKey(Year)
	tb_nam = models.FloatField( validators = [validate_mark])
	hl_nam=models.CharField( max_length = 3, choices = HL_CHOICES)
	#hanh kiem nam
	hk_nam=models.CharField( max_length = 2, choices = HK_CHOICES)
	#ghi danh hieu ma hoc sinh dat dc trong hoc ky	
	danh_hieu_nam=models.CharField( max_length = 2, choices = DH_CHOICES)
	len_lop=models.BooleanField(choices=LENLOP_CHOICES,default=True)
	#danh dau thi lai
	
	thi_lai = models.BooleanField(blank = True, default = False)
	tb_thi_lai=models.FloatField( null = True, blank = True, validators = [validate_mark])
	hl_thi_lai=models.CharField( blank=True,max_length = 3, choices = HL_CHOICES)
	#danh dau ren luyen lai trong giai doan he
	ren_luyen_lai=models.BooleanField(blank = True, default = False)
	hk_ren_luyen_lai=models.CharField(blank=True,max_length = 2, choices = HK_CHOICES)
	#danh dau len lop hay ko
	len_lop_sau_he=models.NullBooleanField(null=True,blank = True,choices =LENLOP_CHOICES)
	
	
	def __unicode__(self):
		return ".2f" % self.tb_nam
	
class DiemDanh(models.Model):
	student_id = models.ForeignKey(Pupil)
	time = models.DateField()
	loai = models.CharField( max_length = 2, choices = DIEM_DANH_TYPE, default = 'K') 
	
	def __unicode__(self):
		return self.student_id + " " + str(self.time)
	

class TKDiemDanh(models.Model):
	student_id = models.ForeignKey(Pupil)
	tong_so = models.IntegerField()
	co_phep = models.IntegerField()
	khong_phep = models.IntegerField()
	
	def __unicode__(self):
		return self.stundent_id + " " + str(self.tong_so)
