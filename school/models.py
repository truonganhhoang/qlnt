# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from datetime import date

from app.models import *

LOAI_CHOICES = ((0,u'Tính cả 2 kỳ'),(1,u'Chỉ tính kì 1'),(2,u'Chỉ tính kì 2'),(3,u'Cộng vào điểm TB(NN2)'),(4,u'Không tính điểm'))
SUBJECT_TYPES = ((u'Toán',u'Toán'),
                 (u'Vật lí', u'Vật lí'), (u'Hóa học', u'Hóa học'),
                 (u'Sinh học', u'Sinh học'),(u'Ngữ văn', u'Ngữ văn'),
                 (u'Lịch sử', u'Lịch sử'), (u'Địa lí', u'Địa lí'),
                 (u'Ngoại ngữ', u'Ngoại ngữ'), (u'GDCD',u'GDCD'),
                 (u'Công nghệ', u'Công nghệ'), (u'Thể dục', u'Thể dục'),
                 (u'Âm nhạc', u'Âm nhạc'),(u'Mĩ thuật', u'Mĩ thuật'),
                 (u'NN2', u'NN2'),(u'Tin học', u'Tin học'),
                 (u'GDQP-AN', u'GDQP-AN'),('',u'Loai khac'))
GENDER_CHOICES = ((u'Nam', u'Nam'),(u'Nữ', u'Nữ'),)
TERM_CHOICES = ((1, u'1'), (2, u'2'),(3, u'3'),)
HK_CHOICES = ((u'T', u'Tốt'), (u'K', u'Khá'),(u'TB',u'Trung Bình'),(u'Y', u'Yếu'),)
HL_CHOICES = ((u'G', u'Giỏi'), (u'K', u'Khá'),(u'TB',u'Trung Bình'),(u'Y', u'Yếu'),(u'Kem', u'Kém'))
#k co nghia la khong duoc danh hieu gi
DH_CHOICES = ((u'XS', u'Học sinh xuất sắc'),(u'G', u'Hoc sinh giỏi'), (u'TT', u'Học sinh tiên tiến'),(u'K',u'Không được gì'))
KT_CHOICES = ((u'Khen trước lớp',u'Khen trước lớp'), (u'Khen trước toàn trường',u'Khen trước toàn trường'),
              (u'Được tặng danh hiệu học sinh khá',u'Được tặng danh hiệu học sinh khá'), 
              (u'Được tặng danh hiệu học sinh giỏi',u'Được tặng danh hiệu học sinh giỏi'), (u'Được ghi tên vào bảng danh dự của trường',u'Được ghi tên vào bảng danh dự của trường'), 
              (u'Được tặng danh hiệu học sinh xuất sắc',u'Được tặng danh hiệu học sinh xuất sắc'), (u'Được khen thưởng đặc biệt',u'Được khen thưởng đặc biệt'))
KL_CHOICES = ((u'Khiển trách trước lớp',u'Khiển trách trước lớp'), (u'Khiển trách trước hội đồng kỷ luật',u'Khiển trách trước hội đồng kỷ luật'), 
              (u'Cảnh cáo trước toàn trường',u'Cảnh cáo trước toàn trường'), (u'Đình chỉ học',u'Đình chỉ học'))
SCHOOL_LEVEL_CHOICE = ((1, u'1'), (2, u'2'), (3, u'3'))
DIEM_DANH_TYPE = ((u'Có phép', u'Có phép'),(u'Không phép', u'Không phép'),(u'k','Đi học'))
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
            (63,u'Sơ rá'),(64,u'Jẻ'),(65,u'Mơ nâm'),(66,u'Hơ lăng'),(67,u'Hoa (Hán)'),(68,u'Sán chay'),
            (69,u'CaDong'),(70,u'Chơ ro'))
LENLOP_CHOICES=((True,u'Được lên lớp'),(False,u'Không được lên lớp'))
SCHOOL_ACTION_STATUS=((0, u'Trường mới'),(1, u'Đang học kì 1'), (2, u'Đang học kì 2'), (3, u'Đang nghỉ hè'))
CLASS_ACTION_STATUS=((1, u'Đang học kì 1'), (2, u'Đang học kì 2'), (3, u'Đang nghỉ hè'))
ACTIVE_CHOICES=((True,u'Đang diễn ra'),(False,u'Đã kết thúc'))

def this_year():
    return int(date.today().year)

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

def validate_dd_date(value):
    if value > date.today():
        raise ValidationError(u'Ngày nẳm ngoài khoảng cho phép')
#validate he so diem cua mon    
def validate_hs(value):
    #he so bang 0 la cho nhung mon cham diem bang nhan xet
    if value < 0:
        raise ValidationError(u'hs must be larger than 0')        

class DanhSachLoaiLop(models.Model):
    loai = models.CharField("Loại", max_length = 15)
    school_id = models.ForeignKey(Organization,verbose_name = "Trường")
    
    class Meta:
        verbose_name = "Danh sách loại lớp"
        verbose_name_plural = "Danh sách loại lớp"
        
    def __unicode__(self):
        return self.loai

    #cac khoi trong 1 truong    
class Block(models.Model):
    number = models.SmallIntegerField("Khối(*)", max_length = 2, choices=KHOI_CHOICE)
    school_id = models.ForeignKey(Organization, verbose_name = "Trường(*)")
    
    class Meta:
        verbose_name = "Khối"
        verbose_name_plural = "Khối"

    def __unicode__(self):
        return str(self.number)

class Team(models.Model):
    name = models.CharField("Tổ", max_length= 30)
    school_id = models.ForeignKey(Organization, verbose_name="Trường(*)")

    class Meta:
        verbose_name = "Tổ"
        verbose_name_plural = "Tổ"

    def __unicode__(self):
        return unicode(self.name)

class Group(models.Model):
    name = models.CharField("Nhóm", max_length= 30)
    team_id = models.ForeignKey(Team, verbose_name="Tổ(*)")

    class Meta:
        verbose_name = "Nhóm"
        verbose_name_plural = "Nhóm"

    def __unicode__(self):
        return unicode(self.name)

class BasicPersonInfo(models.Model):
    last_name = models.CharField("Họ", max_length = 45, blank = True) # tach ra first_name and last_name de sort va import from excel file
    first_name = models.CharField("Tên(*)", max_length = 90)#vi phan nhap bang tay, ho ten se dc luu vao first_name nen max_length phai dc tang len gap doi
    birthday = models.DateField("Ngày sinh(*)", null = True, validators = [validate_birthday])
    birth_place = models.CharField("Nơi sinh", max_length = 200, blank = True)
    dan_toc = models.CharField("Dân tộc", max_length = 15, blank = True, default = 'Kinh')
    ton_giao = models.CharField("Tôn giáo", max_length = 20, blank = True)
    quoc_tich = models.CharField("Quốc tịch", max_length = 20, blank = True, default = 'Việt Nam')
    home_town = models.CharField("Quê quán", max_length = 100, blank = True) #nguyen quan
    sex = models.CharField("Giới tính(*)", max_length = 3, choices = GENDER_CHOICES, default = 'Nam')
    phone = models.CharField("Điện thoại", max_length = 15, blank = True, validators = [validate_phone])
    sms_phone = models.CharField("Điện thoại nhận tin nhắn", max_length = 15, blank = True, validators = [validate_phone])
    current_address = models.CharField("Địa chỉ", max_length = 200, blank = True)
    email = models.EmailField("Email", null = True, blank = True)
    index = models.IntegerField("Số thứ tự(*)", default=0)
    class Meta:
        abstract = True
    
    def full_name(self):
        return ' '.join([self.last_name, self.first_name])
    
    def __unicode__(self):
        return self.last_name + " " + self.first_name
        
    #class Admin: pass

class Teacher(BasicPersonInfo):
    major = models.CharField("Chuyên môn(*)", max_length=45, default='', blank= True, choices=SUBJECT_TYPES)
    user_id = models.OneToOneField(User, verbose_name = "Tài khoản")
    school_id = models.ForeignKey(Organization, verbose_name = "Trường")
    group_id = models.ForeignKey(Group, null=True, blank=True, verbose_name="Nhóm", on_delete = models.SET_NULL)
    team_id = models.ForeignKey(Team, null=True, blank=True, verbose_name="Tổ", on_delete = models.SET_NULL)

    class Meta:
        verbose_name = "Giáo viên"
        verbose_name_plural = "Giáo viên"
        unique_together = ("school_id", "first_name", "last_name", "birthday",)

class Year(models.Model):
    time = models.IntegerField("Năm", max_length = 4, validators = [validate_year]) # date field but just use Year
    school_id = models.ForeignKey(Organization, verbose_name = "Trường")
    
    class Meta:
        verbose_name = "Năm học"
        verbose_name_plural = "Năm học"
    
    def __unicode__(self):
        return str(self.time) + "-" + str(self.time+1)
        
class StartYear(models.Model):
    time = models.IntegerField("Năm", max_length = 4, validators = [validate_year]) # date field but just use Year
    school_id = models.ForeignKey(Organization)
    
    
    class Meta:
        verbose_name = "Khóa"
        verbose_name_plural = "Khóa"
        
    def __unicode__(self):
        return str(self.time)
    
class Term(models.Model):
    number = models.IntegerField("Kì", max_length=1, choices = TERM_CHOICES)
    # neu active =false thi khong cho phep sua diem nua
    year_id = models.ForeignKey(Year, verbose_name = "Năm học")
    
    class Meta:
        verbose_name = "Kì"
        verbose_name_plural = "Kì"
        
    def __unicode__(self):
        return str(self.number) + " " + str(self.year_id)         
    #class Admin: pass

class Class(models.Model):    
    #cai nay sau cung bo di    
    #class_code = models.CharField(max_length = 20, unique = True)    
    name = models.CharField("Tên lớp(*)", max_length = 20)
    index = models.IntegerField("Số thứ tự", default=0)
    status = models.SmallIntegerField("Tình trạng", max_length = 3, null = True, blank= True, choices = CLASS_ACTION_STATUS)


    year_id = models.ForeignKey(Year, verbose_name = "Năm học(*)")
    #lop nay thuoc khoi nao
    block_id = models.ForeignKey(Block, verbose_name = "Khối(*)")
    teacher_id = models.OneToOneField(Teacher, verbose_name = "Giáo viên chủ nhiệm", null = True, blank = True) #field nay chi dung de phan quyen, vi vay chi gan 1 gia tri nhan dang
    
    
    def __unicode__(self):
        return self.name

    def number_of_pupils(self):
        try:
            return self.pupil_set.count()
        except Exception :
            return 0

    class Meta:
        verbose_name = "Lớp"
        verbose_name_plural = "Lớp"
        unique_together = ("year_id", "name")
    #class Admin: pass
        
class Pupil(BasicPersonInfo):
    year = models.IntegerField("Năm học lớp 1", validators = [validate_year], blank = True, null = True) #year that pupil go to class 1

    school_join_date = models.DateField("Ngày nhập trường(*)", default = date.today(),validators=[validate_join_date])
    ban_dk = models.CharField("Ban đăng kí(*)", max_length = 5, choices = BAN_CHOICE, default = u'CB')
    school_join_mark = models.IntegerField("Điểm tuyển sinh", null = True, blank = True)
    #thong tin ca nhan
    khu_vuc = models.CharField("Khu vực", max_length = 3, choices = KV_CHOICE, blank = True)
    doi = models.BooleanField("Là đội viên", blank = True, default = False)
    ngay_vao_doi = models.DateField("Ngày vào đội", blank = True, null = True, validators=[validate_dd_date])
    doan = models.BooleanField("Là đoàn viên", blank = True, default = False)
    ngay_vao_doan = models.DateField("Ngày vào đoàn", blank = True, null = True, validators=[validate_dd_date])
    dang = models.BooleanField("Là đảng viên", blank = True, default = False)
    ngay_vao_dang = models.DateField("Ngày vào đảng", blank = True, null = True, validators=[validate_dd_date])
    uu_tien = models.CharField("Ưu tiên", blank = True, max_length = 100)
    
    #thong tin gia dinh
    father_name = models.CharField("Họ và tên bố", max_length = 45, blank = True)
    father_birthday = models.DateField("Ngày sinh của bố", null = True, blank = True)
    father_phone = models.CharField("Điện thoại của bố", max_length = 15, null = True, blank = True, validators = [validate_phone])
    father_job = models.CharField("Nghê nghiệp của bố", max_length = 100, blank = True)
    mother_name = models.CharField("Họ và tên mẹ", max_length = 45, blank = True)
    mother_birthday = models.DateField("Ngày sinh của mẹ", null = True, blank = True)
    mother_job = models.CharField("Nghê nghiệp của mẹ", max_length = 100, blank = True)    
    mother_phone = models.CharField("Điện thoại của mẹ", max_length = 15, null = True, blank = True, validators = [validate_phone])
    
    current_status = models.CharField("Tình trạng", max_length = 200, blank = True, null = True, default = 'OK')
    disable = models.BooleanField("Không còn trong trường", default = False)
    
    user_id = models.OneToOneField(User, verbose_name = "tài khoản", null = True, blank = True) # nullable is temporary 
    start_year_id = models.ForeignKey(StartYear, verbose_name = "khóa")
    class_id = models.ForeignKey(Class, verbose_name = "lớp", null = True, blank = True)
    school_id = models.ForeignKey(Organization, verbose_name = "trường", null = True, blank = True)
    
    class Meta:
        verbose_name = "Học sinh"
        verbose_name_plural = "Học sinh"
        unique_together = ("class_id", "first_name", "last_name", "birthday",)

class Subject(models.Model):    
    name = models.CharField("Tên môn học(*)", max_length = 45) # can't be null
    type = models.CharField("Môn(*)", max_length=45, default='', blank=True, choices= SUBJECT_TYPES)
    hs = models.FloatField("Hệ số(*)", validators = [validate_hs])

    primary = models.SmallIntegerField("Tính điểm(*)", default = 0, choices = LOAI_CHOICES)
    index = models.IntegerField("Số thứ tự(*)", default=0)

    class_id = models.ForeignKey(Class, verbose_name = "Lớp(*)")    
    teacher_id = models.ForeignKey(Teacher, verbose_name = "Giáo viên", null= True ) # field nay de cung cap permission cho giao vien de nhap diem
    
    class Meta:
        verbose_name = "Môn"
        verbose_name_plural = "Môn"
        unique_together = ("name", "class_id")
    
    def __unicode__(self):
        return self.name
    
    #class Admin: pass

class Mark(models.Model):
    
    mieng_1 = models.FloatField("Điểm miệng 1", null = True, blank = True, validators = [validate_mark])
    mieng_2 = models.FloatField("Điểm miệng 2", null = True, blank = True, validators = [validate_mark])
    mieng_3 = models.FloatField("Điểm miệng 3", null = True, blank = True, validators = [validate_mark])
    mieng_4 = models.FloatField("Điểm miệng 4", null = True, blank = True, validators = [validate_mark])
    mieng_5 = models.FloatField("Điểm miệng 5", null = True, blank = True, validators = [validate_mark])
    mlam_1 = models.FloatField("Điểm 15' 1", null = True, blank = True, validators = [validate_mark])
    mlam_2 = models.FloatField("Điểm 15' 2", null = True, blank = True, validators = [validate_mark])
    mlam_3 = models.FloatField("Điểm 15' 3", null = True, blank = True, validators = [validate_mark])
    mlam_4 = models.FloatField("Điểm 15' 4", null = True, blank = True, validators = [validate_mark])
    mlam_5 = models.FloatField("Điểm 15' 5", null = True, blank = True, validators = [validate_mark])
    mot_tiet_1 = models.FloatField("Điểm 1 tiết 1", null = True, blank = True, validators = [validate_mark])
    mot_tiet_2 = models.FloatField("Điểm 1 tiết 2", null = True, blank = True, validators = [validate_mark])
    mot_tiet_3 = models.FloatField("Điểm 1 tiết 3", null = True, blank = True, validators = [validate_mark])
    mot_tiet_4 = models.FloatField("Điểm 1 tiết 4", null = True, blank = True, validators = [validate_mark])
    mot_tiet_5 = models.FloatField("Điểm 1 tiết 5", null = True, blank = True, validators = [validate_mark])
    ck = models.FloatField("Điểm thi cuối kì", null = True, blank = True, validators = [validate_mark])
    tb = models.FloatField("Điểm trung bình", null = True, blank = True, validators = [validate_mark])
    
    sent_mark=models.CharField("đánh dấu đã gửi tin nhắn",max_length=19,default="0000000000000000000")
    
    subject_id = models.ForeignKey(Subject, verbose_name = "Môn")
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh", null = True, blank = True)        
    term_id    = models.ForeignKey(Term, verbose_name = "Kì")
    
    class Meta:
        verbose_name = "Bảng điểm"
        verbose_name_plural = "Bảng điểm"

    #noinspection PyMethodOverridi
    def save(self):
        new = self.id is None
        super(Mark, self).save()
        if new:
            MarkTime.objects.create( mark_id = self)
            #SentMark.objects.create( mark_id = self)    
     

    def __unicode__(self):
        return self.subject_id.name + " " + str(self.term_id.number) + self.student_id.first_name

class MarkTime(models.Model):
    
    mieng_1 = models.DateTimeField("Thời gian cập nhật điểm miệng 1", null = True, blank = True)
    mieng_2 = models.DateTimeField("Thời gian cập nhật điểm miệng 2", null = True, blank = True)
    mieng_3 = models.DateTimeField("Thời gian cập nhật điểm miệng 3", null = True, blank = True)

    mieng_4 = models.DateTimeField("Thời gian cập nhật điểm miệng 4", null = True, blank = True)
    mieng_5 = models.DateTimeField("Thời gian cập nhật điểm miệng 5", null = True, blank = True)
    mlam_1 = models.DateTimeField("Thời gian cập nhật điểm 15' 1", null = True, blank = True)
    mlam_2 = models.DateTimeField("Thời gian cập nhật điểm 15' 2", null = True, blank = True)
    mlam_3 = models.DateTimeField("Thời gian cập nhật điểm 15' 3", null = True, blank = True)
    mlam_4 = models.DateTimeField("Thời gian cập nhật điểm 15' 4", null = True, blank = True)
    mlam_5 = models.DateTimeField("Thời gian cập nhật điểm 15' 5", null = True, blank = True)
    
    mot_tiet_1 = models.DateTimeField("Thời gian cập nhật điểm 1 tiết 1", null = True, blank = True)
    mot_tiet_2 = models.DateTimeField("Thời gian cập nhật điểm 1 tiết 2", null = True, blank = True)
    mot_tiet_3 = models.DateTimeField("Thời gian cập nhật điểm 1 tiết 3", null = True, blank = True)
    mot_tiet_4 = models.DateTimeField("Thời gian cập nhật điểm 1 tiết 4", null = True, blank = True)
    mot_tiet_5 = models.DateTimeField("Thời gian cập nhật điểm 1 tiết 5", null = True, blank = True)
    
    ck = models.DateTimeField("Thời gian cập nhật điểm thi cuối kì", null = True, blank = True)
    tb = models.DateTimeField("Thời gian cập nhật điểm trung bình", null = True, blank = True)
    
    mark_id = models.OneToOneField(Mark, verbose_name = "Điểm")
    
    class Meta:
        verbose_name = "Bảng thời gian cập nhật điểm"
        verbose_name_plural = "Bảng thời gian cập nhật điểm"

    def __unicode__(self):
        return self.mark_id.__unicode__() 
class TKMon(models.Model):    
    tb_nam = models.FloatField("Trung bình năm", null = True, blank = True, validators = [validate_mark])
    #danh dau xem mon nay co dc phep thi lai hay ko
    thi_lai = models.BooleanField("Có thi lại", blank = True, default = False)
    diem_thi_lai=models.FloatField("Điểm thi lại", null = True, blank = True, validators = [validate_mark])
    # all fields can be null
    
    subject_id = models.ForeignKey(Subject, verbose_name = "Môn")
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    
    class Meta:
        verbose_name = "Trung bình môn"
        verbose_name_plural = "Trung bình môn"        
    #class Admin: pass
    def __unicode__(self):
        return self.subject_id.name + " " + self.student_id.first_name
        
class KhenThuong(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh", null = True)
    term_id = models.ForeignKey(Term, verbose_name = "Kì", null = True)
    
    time = models.DateField("Thời gian(*)", blank = True)
    hinh_thuc = models.CharField("Hình thức(*)", max_length = 100, choices = KT_CHOICES)
    dia_diem= models.CharField("Địa điểm", max_length = 100, blank = True, null = True)
    noi_dung = models.CharField("Nội dung", max_length = 400, blank = True, null = True) # description
    luu_hoc_ba = models.BooleanField("Lưu học bạ", blank = True, default = False)
    
    class Meta:
        verbose_name = "Khen thưởng"
        verbose_name_plural = "Khen thưởng"
        
    def __unicode__(self):
        return self.hinh_thuc

class KiLuat(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    term_id = models.ForeignKey(Term, verbose_name = "Kì")
    
    time = models.DateField("Thời gian(*)", blank = True)
    hinh_thuc = models.CharField("Hình thức(*)", max_length = 35, choices = KL_CHOICES)
    dia_diem= models.CharField("Địa điểm", max_length = 100, blank = True, null = True)
    noi_dung = models.CharField("Nội dung", max_length = 400, blank = True, null = True) # description
    luu_hoc_ba = models.BooleanField("Lưu học bạ", blank = True, default = False)
    
    class Meta:
        verbose_name = "Kỉ luật"
        verbose_name_plural = "Kỉ luật"
        
    def __unicode__(self):
        return self.hinh_thuc
        
class HanhKiem(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    year_id = models.ForeignKey(Year, verbose_name = "Năm học")    
    term1 = models.CharField("Kì 1",max_length = 2, choices = HK_CHOICES, null=True,blank=True)
    term2 = models.CharField("Kì 2",max_length = 2, choices = HK_CHOICES, null=True,blank=True)
    year = models.CharField("Cả năm",max_length = 2, choices = HK_CHOICES, null=True,blank=True)
    #danh dau ren luyen lai trong giai doan he
    ren_luyen_lai=models.NullBooleanField("Rèn luyện lại", blank = True, null = True)
    hk_ren_luyen_lai=models.CharField("Hạnh kiểm rèn luyện lại", null=True, blank=True, max_length = 2, choices = HK_CHOICES)
    class Meta:
        verbose_name = "Hạnh kiểm"
        verbose_name_plural = "Hạnh kiểm"
    
    def __unicode__(self):
        return unicode(self.student_id) + '-' + unicode(self.year_id)
        
class TBHocKy(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    term_id = models.ForeignKey(Term, verbose_name = "Kì")

    number_subject=models.SmallIntegerField("số lượng môn",null=True,blank=True, default=0)
    number_finish =models.SmallIntegerField("số lượng môn đã tổng kết xong", default=0)
    
    
    tb_hk = models.FloatField("Trung bình học kì", validators = [validate_mark], null = True, blank = True)        
    hl_hk = models.CharField("Học lực", max_length = 3, choices = HL_CHOICES, null = True, blank = True)
    danh_hieu_hk = models.CharField("Danh hiệu", max_length = 2, choices = DH_CHOICES, null = True, blank = True)
    
    class Meta:
        verbose_name = "Trung bình học kì"
        verbose_name_plural = "Trung bình học kì"
    
    def __unicode__(self):
        return  str(self.tb_hk) + " " + self.term_id.__unicode__() + self.student_id.__unicode__()
        
class TBNam(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    year_id = models.ForeignKey(Year, verbose_name = "Năm học")
    
    number_subject=models.SmallIntegerField("số lượng môn",null=True,blank=True, default=0)
    number_finish =models.SmallIntegerField("số lượng môn chưa tổng kết xong", default=0)
    
    tb_nam = models.FloatField("Trung bình năm", validators = [validate_mark], null = True, blank = True)
    hl_nam=models.CharField("Học lực", max_length = 3, choices = HL_CHOICES, null = True, blank = True)
    #hanh kiem nam
    #hk_nam=models.CharField("Hạnh kiểm",max_length = 2, choices = HK_CHOICES, null = True, blank = True)
    tong_so_ngay_nghi=models.SmallIntegerField("Số ngày nghỉ", null = True, blank = True)
    #ghi danh hieu ma hoc sinh dat dc trong hoc ky    
    danh_hieu_nam=models.CharField("Danh hiệu", max_length = 2, choices = DH_CHOICES,null=True,blank=True)
    len_lop=models.NullBooleanField("Lên lớp", choices = LENLOP_CHOICES, null = True, blank = True)
    #danh dau thi lai
    
    thi_lai = models.NullBooleanField("Thi lại", null=True,blank=True)
    tb_thi_lai=models.FloatField("Trung bình thi lại", null = True, blank = True, validators = [validate_mark])
    hl_thi_lai=models.CharField("Học lực thi lại", null = True, blank=True, max_length = 3, choices = HL_CHOICES)
    
    #len_lop_sau_he=models.NullBooleanField(null=True,blank = True,choices =LENLOP_CHOICES)

    
    class Meta:
        verbose_name = "Trung bình năm"
        verbose_name_plural = "Trung bình năm"
    def __unicode__(self):
        return self.student_id.__unicode__() + " " + str(self.year_id.__unicode__()) + " " + str(self.tb_nam) 

class DiemDanh(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    term_id = models.ForeignKey(Term, verbose_name = "Kì")
    
    time = models.DateField("Ngày")
    loai = models.CharField("Tình trạng", max_length = 10, choices = DIEM_DANH_TYPE, default = 'k') 
    
    class Meta:
        verbose_name = "Điểm danh"
        verbose_name_plural = "Điểm danh"
        unique_together = ("student_id", "time", "term_id")
        
    def __unicode__(self):
        return self.student_id.__unicode__() + " " + str(self.time)
        
class TKDiemDanh(models.Model):
    student_id = models.ForeignKey(Pupil, verbose_name = "Học sinh")
    term_id = models.ForeignKey(Term, verbose_name = "Kì")
    
    tong_so = models.IntegerField("Số buổi nghỉ", blank = True, null = True)
    co_phep = models.IntegerField("Số buổi có phép", blank = True, null = True)
    khong_phep = models.IntegerField("Số buổi không phép", blank = True, null = True)
    
    class Meta:
        verbose_name = "Tổng kết điểm danh"
        verbose_name_plural = "Tổng kết điểm danh"
    
    def __unicode__(self):
        return self.student_id.__unicode__()
        
