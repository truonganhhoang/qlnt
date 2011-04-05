from django.db import models
from django.forms import ModelForm

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
        
# School year model
class SchoolYear (models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField ()
    end_date = models.DateField ()
    
    def __unicode__(self):
        return self.name
# School year form
class SchoolYearForm(ModelForm):
    class Meta:
        mode = SchoolYear

# Student model
class Student (models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.name
# Student form
class StudentForm (ModelForm):
    class Meta:
        model = Student

# Extend student's information model
class StudentExtented (models.Model):
    student_id = models.ForeignKey(Student)
    student_code = models.IntegerField(max_length = 8)
    birthdate = models.DateField()
    street_id = models.CharField(max_length = 30)
    village_id = models.CharField(max_length = 30)
    address = models.CharField(max_length = 255)
    birthplace = models.CharField(max_length = 255)
    ethnic = models.CharField(max_length = 255)
    dien_chinh_sach = models.CharField(max_length = 255) # Check
    father_name = models.CharField (max_length = 50)
    father_job = models.CharField (max_length = 255)
    mother_name = models.CharField(max_length = 50)
    mother_job = models.CharField(max_length = 255)
    phone_no1 = models.CharField (max_length = 30)
    phone_no2 = models.CharField (max_length = 30)
    phone_no3 = models.CharField(max_length = 30)
    identity_card = models.CharField(max_length = 30)
    gender = models.CharField (max_length = 30)
    sick_soldier_child = models.CharField(max_length = 30) # Con thuong binh
    partiotic_martyr_child  = models.CharField (max_length = 30) # Con liet sy
    difficult = models.CharField (max_length = 255) # "hoan canh kho khan"
    certificate_type = models.CharField (max_length = 30)
    email = models.EmailField ()
    graduation_province = models.CharField (max_length = 255)
    capacity_last_year = models.CharField(max_length = 255)
    class_last_year = models.CharField (max_length = 255)
    religion_id = models.CharField(max_length = 30)
    school_code = models.CharField (max_length = 30)
    group = models.CharField (max_length = 30) # Thuoc to
    def __unicode__(self):
        return self.name
# Extend student's information form
class StudentExtendedForm (ModelForm):
    class Meta:
        model = StudentExtented
 
# Standard major model
class StandardMajor (models.Model):
    name = models.CharField (max_length = 50)
    def __unicode__(self):
        return self.name
# Standard major form
class StandardMajorForm (ModelForm):
    class Meta:
        model = StandardMajor
               
# Major model ("chuyen ban")
class Major (models.Model):
    name = models.CharField (max_length = 50)
    standard_major_id = models.ForeignKey(StandardMajor)
    specialised_major = models.CharField (max_length = 50)
    def __unicode__(self):
        return self.name
# Major form
class MajorForm (ModelForm):
    class Meta:
        model = Major

# Grade model ("khoi")
class Grade (models.Model):
    name = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.name
# Grade form
class GradeForm (ModelForm):
    class Meta:
        model = Grade
        
# Subject model
class Subject (models.Model):
    name = models.CharField(max_length = 50)
    assessment = models.CharField (max_length = 255) # Mon hoc danh gia?
    subject_choice = models.CharField (max_length = 255) # Mon hoc tu chon
    order_number = models.IntegerField (max_length = 10)
    invalid = models.BooleanField()
    def __unicode__(self):
        return self.name
# Subject form    
class SubjectForm (ModelForm):
    class Meta:
        model = Subject
        
# User model
class User (models.Model):
    name = models.CharField(max_length = 50)
    name_tat = models.CharField(max_length = 50) # "tat"?
    type_id = models.CharField(max_length = 30)
    password = models.CharField(max_length = 50)
    email = models.EmailField()
    invalid = models.BooleanField()
    subject1 = models.ForeignKey(Subject) 
   # subject2 = models.ForeignKey(Subject)
   # subject3 = models.ForeignKey(Subject)
    captain = models.CharField(max_length = 50)
    deputy_captain = models.CharField(max_length = 50)
    phone_no1 = models.CharField(max_length = 30)
    phone_no2 = models.CharField(max_length = 30)
    def __unicode__(self):
        return self.name
# User form
class UserForm (ModelForm):
    class Meta:
        model = User

# Class model
class Class (models.Model):
    name = models.CharField(max_length = 50)
    school_year_id = models.ForeignKey(SchoolYear)
    major_id = models.ForeignKey(Major)
    class_teacher_id = models.ForeignKey(User)
    grade_id = models.ForeignKey(Grade)
    order_number = models.IntegerField(max_length = 10)
    morning = models.CharField(max_length = 50) #  purpose?
    def __unicode__(self):
        return self.name
# Class form
class ClassForm (ModelForm):
    class Meta:
        model = Class
        
# Coefficent Subject model
class ConfficentSubject (models.Model):
    major_id = models.ForeignKey(Major)
    subject_id = models.ForeignKey(Subject)
    confficent = models.FloatField ()
    order_number = models.IntegerField(max_length = 10)
    subject_type = models.CharField(max_length = 20)
    def __unicode__(self):
        return self.name
# Coefficent Subject form
class ConfficentSubjectForm (ModelForm):
    class Meta:
        model = ConfficentSubject
    
# Student takes subject's awards 
class StudentSubject (models.Model):
    student_id = models.ForeignKey(Student)
    subject_id = models.ForeignKey(Subject)
    award = models.CharField(max_length = 50)
    bonus_point = models.FloatField(max_length = 10)
    def __unicode__(self):
        return self.name
# Student takes subject's award form
class StudentSubjectForm (ModelForm):
    class Meta:
        model = StudentSubject

# Student_Class model
class StudentClass (models.Model):
    student_id = models.ForeignKey(Student)
    class_id = models.ForeignKey(Class)
    major_id = models.ForeignKey(Major)
    order_number = models.IntegerField(max_length = 10)
    status = models.CharField (max_length = 30)
    def __unicode__(self):
        return self.name
# Student_Class form
class StudentClassForm (ModelForm):
    class Meta:
        model = StudentClass
    
# Phase_Mark_Type models
class PhaseMarkType (models.Model):
    name = models.CharField (max_length = 50)
    def __unicode__(self):
        return self.name
# Phase_Mark_Type form
class PhaseMarkTypeForm (ModelForm):
    class Meta:
        model = PhaseMarkType
    
# Phase to check mark of student
class PhaseMark (models.Model):
    name = models.CharField (max_length = 50)
    phase_mark_type  = models.ForeignKey(PhaseMarkType)
    school_year_id = models.ForeignKey(SchoolYear)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.IntegerField(max_length = 10)
    order_number = models.IntegerField(max_length = 10)
    SMS_code1 = models.CharField(max_length = 30)
    SMS_code2 = models.CharField(max_length = 30)
    SMS_code3 = models.CharField(max_length = 30)
    SMS_code4 = models.CharField(max_length = 30)
    SMS_code5 = models.CharField(max_length = 30)
    SMS_code6 = models.CharField(max_length = 30)
    def __unicode__(self):
        return self.name
# Phase_Mark form
class PhaseMarkForm (ModelForm):
    class Meta:
        model = PhaseMark

# Student_Class_PhaseMark models
class StudentClassPhaseMark (models.Model):
    student_class_id = models.ForeignKey(StudentClass)
    phase_mark_id = models.ForeignKey(PhaseMark)
    average = models.FloatField()
    round_average = models.FloatField()
    capacity = models.CharField(max_length = 50) # Hoc luc?
    average_conduct = models.FloatField ()
    conduct = models.CharField(max_length = 50)
    order = models.IntegerField(max_length = 10)
    identifier = models.CharField(max_length = 50)
    permit = models.IntegerField (max_length = 10) # Nghi co phep??
    unpermitted = models.IntegerField (max_length = 10) # Nghi ko phep??
    comment = models.CharField (max_length = 1000)
    result = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.name
# Student_Class_PhaseMark form
class StudentClassPhaseMarkForm (ModelForm):
    class Meta:
        model = StudentClassPhaseMark
        


# Exam Model
class ConcentratedExam(models.Model):
    name = models.CharField(max_length = 100)
    create_date = models.DateField(auto_now_add = True)
    exam_date = models.DateField()
#    mark_flow = models.ForeignKey()
    mark_column = models.CharField(max_length = 20) 
    exam_type = models.CharField(max_length = 20) 
    start_name_list_no = models.CharField(max_length = 20)
    code_length = models.IntegerField()
    name_list_scale = models.BooleanField()
    subject_type = models.CharField(max_length = 20)
class CEGroup(models.Model): #from ConcentratedExam
    name = models.CharField(max_length=100)
    concentrated_exam = models.ForeignKey(ConcentratedExam)
    group_prefix = models.CharField(max_length = 10)
class CERoom (models.Model):
    CEGroup = models.ForeignKey(CEGroup)
    name = models.CharField(max_length = 100)
    quanlity = models.IntegerField()
class CESubject (models.Model):
    concentrated_exam = models.ForeignKey(ConcentratedExam)
    #subject = models.ForeignKey()
    prefix = models.CharField(max_length = 20)
    difference = models.CharField(max_length = 50) # do lech
class CEGroupClass (models.Model):
    group = models.ForeignKey(CEGroup)
#    clazz = models.ForeignKey()

# class StudentClass(models.Model):
#    clazz = models.ForeignKey()
#    student = models.ForeignKey()
#    type = models.ForeignKey()
 #   order_number = models.IntegerField()
 #   status  = models.CharField(max_length = 100)
    
class CERoomStudent(models.Model):
    room = models.ForeignKey(CERoom)
    student_class = models.ForeignKey(StudentClass)
    name_number = models.CharField(max_length = 20)
    order_number = models.IntegerField()
    room_number = models.IntegerField()
    absent = models.BooleanField()

class CERoomStudentMark():
#    subject = models.ForeignKey()
    mark = models.IntegerField()
#    student = models.ForeignKey()
    verified_mark = models.IntegerField()
