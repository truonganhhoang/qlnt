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
    #===========================================================================
    # ORGANIZATION_TYPE_CHOICES = (('T', 'Truong'),
    #                             ('P', 'Phong'),
    #                             ('S', 'So'))
    #===========================================================================
    #===========================================================================
    # def __init__(self, *args, **kwargs):
    #    super(SchoolForm, self).__init__(*args, **kwargs)
    #    self.fields['upper_organization'].choices = [(-1, '----------')] + [(i.id, i.name) for i in Organization.objects.all() \
    #                                                                        if i.organization_type == 'S' or i.organization_type == 'P']
    # 
    #===========================================================================
    name = forms.CharField(max_length=100, min_length=1)
    adress = forms.CharField(max_length=255, min_length=1)
    phone_number = forms.CharField(max_length=40, min_length=9)
    email_adress = forms.EmailField()
#    organization_type = forms.ChoiceField()
#    upper_organization = forms.
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

#===============================================================================
# class UserForm(forms.Form):
#    name = forms.CharField(max_length=100, min_length=1)
#    birthday = forms.DateField()
#    phone_number = forms.CharField(max_length=40, min_length=9)
#    fax_number = forms.CharField(max_length=50, min_length=9)
#    email = forms.EmailField()
#===============================================================================

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
    
# Student model
class Student (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

# Student form
class StudentForm (forms.ModelForm):
    class Meta:
        model = Student

# Extend student's information model
class StudentExtented (models.Model):
    student_id = models.ForeignKey(Student)
    window_code = models.CharField(max_length=30)
    birthdate = models.DateField()
    street_id = models.CharField(max_length=30)
    village_id = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    birthplace = models.CharField(max_length=255)
    ethnic = models.CharField(max_length=255)
    dien_chinh_sach = models.CharField(max_length=255) # Check
    father_name = models.CharField (max_length=50)
    father_job = models.CharField (max_length=255)
    mother_name = models.CharField(max_length=50)
    mother_job = models.CharField(max_length=255)
    phone_no1 = models.CharField (max_length=30)
    phone_no2 = models.CharField (max_length=30)
    phone_no3 = models.CharField(max_length=30)
    identity_card = models.CharField(max_length=30)
    gender = models.CharField (max_length=30)
    sick_soldier_child = models.CharField(max_length=30) # Con thuong binh
    partiotic_martyr_child = models.CharField (max_length=30) # Con liet sy
    difficult = models.CharField (max_length=255) # "hoan canh kho khan"
    certificate_type = models.CharField (max_length=30)
    email = models.EmailField ()
    graduation_province = models.CharField (max_length=255)
    capacity_last_year = models.CharField(max_length=255)
    class_last_year = models.CharField (max_length=255)
    religion_id = models.CharField(max_length=30)
    school_code = models.CharField (max_length=30)
    group = models.CharField (max_length=30) # Thuoc to
    def __unicode__(self):
        return self.name

# Extend student's information form
class StudentExtendedForm (forms.ModelForm):
    class Meta:
        model = StudentExtented
 
# Standard major model
class StandardMajor (models.Model):
    name = models.CharField (max_length=50)
    def __unicode__(self):
        return self.name

# Standard major form
class StandardMajorForm(forms.ModelForm):
    class Meta:
        model = StandardMajor
               
# Major model ("chuyen ban")
class Major(models.Model):
    name = models.CharField (max_length=50)
    standard_major = models.ForeignKey(StandardMajor)
    specialised_major = models.CharField (max_length=50)
    def __unicode__(self):
        return self.name

# Major form
class MajorForm(forms.ModelForm):
    class Meta:
        model = Major

# Grade model ("khoi")
class Grade(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

# Grade form
class GradeForm (forms.ModelForm):
    class Meta:
        model = Grade
        
# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=50)
    assessment = models.CharField (max_length=255) # Mon hoc danh gia?
    subject_choice = models.CharField (max_length=255) # Mon hoc tu chon
    order_number = models.IntegerField (max_length=10)
    invalid = models.BooleanField()
    def __unicode__(self):
        return self.name

# Subject form    
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        

#===============================================================================
# # User form
# class UserForm (forms.ModelForm):
#    class Meta:
#        model = User
#===============================================================================

# Class model
class Class (models.Model):
    name = models.CharField(max_length=50)
    school_year = models.ForeignKey(SchoolYear)
    major = models.ForeignKey(Major)
    class_teacher = models.ForeignKey(User)
    grade = models.ForeignKey(Grade)
    order_number = models.IntegerField(max_length=10)
    morning = models.CharField(max_length=50) #  purpose?
    class Meta:
        unique_together = ('school_year', 'major', 'class_teacher', 'grade')

# Class form
class ClassForm (forms.ModelForm):
    class Meta:
        model = Class
        
# Coefficent Subject model
class ConfficentSubject (models.Model):
    major = models.ForeignKey(Major)
    subject = models.ForeignKey(Subject)
    confficent = models.FloatField ()
    order_number = models.IntegerField(max_length=10)
    subject_type = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ('major', 'subject')

# Coefficent Subject form
class ConfficentSubjectForm (forms.ModelForm):
    class Meta:
        model = ConfficentSubject
    
# Student takes subject's awards 
class StudentSubject (models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    award = models.CharField(max_length=50)
    bonus_point = models.FloatField(max_length=10)
    
    class Meta:
        unique_together = ('student', 'subject')

# Student takes subject's award form
class StudentSubjectForm (forms.ModelForm):
    class Meta:
        model = StudentSubject

# Student_Class model
class StudentClass (models.Model):
    student = models.ForeignKey(Student)
    clazz = models.ForeignKey(Class)
    major = models.ForeignKey(Major)
    order_number = models.IntegerField(max_length=10)
    status = models.CharField (max_length=30)
    
    class Meta:
        unique_together = ('student', 'clazz', 'major')

# Student_Class form
class StudentClassForm (forms.ModelForm):
    class Meta:
        model = StudentClass
    
# Phase_Mark_Type models`
class PhaseMarkType (models.Model):
    name = models.CharField (max_length=50)
    def __unicode__(self):
        return self.name

# Phase_Mark_Type form
class PhaseMarkTypeForm (forms.ModelForm):
    class Meta:
        model = PhaseMarkType
    
# Phase to check mark of student
class PhaseMark (models.Model):
    name = models.CharField (max_length=50)
    phase_mark_type = models.ForeignKey(PhaseMarkType)
    school_year_id = models.ForeignKey(SchoolYear)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.IntegerField(max_length=10)
    order_number = models.IntegerField(max_length=10)
    SMS_code1 = models.CharField(max_length=30)
    SMS_code2 = models.CharField(max_length=30)
    SMS_code3 = models.CharField(max_length=30)
    SMS_code4 = models.CharField(max_length=30)
    SMS_code5 = models.CharField(max_length=30)
    SMS_code6 = models.CharField(max_length=30)
    
    class Meta:
        unique_together = ('phase_mark_type', 'school_year_id')


# Phase_Mark form
class PhaseMarkForm (forms.ModelForm):
    class Meta:
        model = PhaseMark

# Student_Class_PhaseMark models
class StudentClassPhaseMark (models.Model):
    student_class = models.ForeignKey(StudentClass)
    phase_mark = models.ForeignKey(PhaseMark)
    average = models.FloatField()
    round_average = models.FloatField()
    capacity = models.CharField(max_length=50) # Hoc luc?
    average_conduct = models.FloatField ()
    conduct = models.CharField(max_length=50)
    order = models.IntegerField(max_length=10)
    identifier = models.CharField(max_length=50)
    permit = models.IntegerField (max_length=10) # Nghi co phep??
    unpermitted = models.IntegerField (max_length=10) # Nghi ko phep??
    comment = models.CharField (max_length=1000)
    result = models.CharField(max_length=255)
   
    class Meta:
        unique_together = ('student_class', 'phase_mark')

# Student_Class_PhaseMark form
class StudentClassPhaseMarkForm (forms.ModelForm):
    class Meta:
        model = StudentClassPhaseMark

# Time table model
class TimeTable(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    apply_date = models.DateField()
    comment = models.TextField()
    locked = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        
class TeacherRules(models.Model):
    teacher = models.ForeignKey(User, unique=True)
    max_periods = models.IntegerField()
    max_wait_periods = models.IntegerField()
    only_one_moment_per_day = models.BooleanField()
    max_subject_per_moment = models.IntegerField()
    max_continuous_periods = models.IntegerField()
    other_info = models.TextField()
    priority = models.IntegerField()

class ClassTabling(models.Model):
    time_table = models.ForeignKey(TimeTable)
    clazz = models.ForeignKey(Class)
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(User)
    day = models.IntegerField()
    period = models.IntegerField()
    type = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('time_table', 'clazz', 'day', 'period')
        
class StandardPeriod(models.Model):
    grade = models.ForeignKey(Grade)
    major = models.ForeignKey(Major)
    subject = models.ForeignKey(Subject)
    curricular_periods = models.CharField(max_length=100)
    curricular_couple_periods = models.CharField(max_length=100)
    extra_curricular_periods = models.CharField(max_length=100)
    extra_curricular_couple_periods = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('grade', 'major', 'subject')

class ClassRules(models.Model):
    clazz = models.ForeignKey(Class)
    day = models.IntegerField()
    period = models.IntegerField()
    reserved = models.BooleanField()
    locked = models.BooleanField()
    # missing some fields due to incomprehension
    
    class Meta:
        unique_together = ('clazz', 'day', 'period')

class TeacherPeriodRules(models.Model):
    teacher = models.ForeignKey(User)
    day = models.IntegerField()
    period = models.IntegerField()
    rule_id = models.IntegerField()
    
    class Meta:
        unique_together = ('teacher', 'day', 'period')
    
# Exam Model
class ConcentratedExam(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateField(auto_now_add=True)
    exam_date = models.DateField()
#    mark_flow = models.ForeignKey()
    mark_column = models.CharField(max_length=20) 
    exam_type = models.CharField(max_length=20) 
    start_name_list_no = models.CharField(max_length=20)
    code_length = models.IntegerField()
    name_list_scale = models.BooleanField()
    subject_type = models.CharField(max_length=20)
class CEGroup(models.Model): #from ConcentratedExam
    name = models.CharField(max_length=100)
    concentrated_exam = models.ForeignKey(ConcentratedExam)
    group_prefix = models.CharField(max_length=10)

class CERoom (models.Model):
    CEGroup = models.ForeignKey(CEGroup)
    name = models.CharField(max_length=100)
    quanlity = models.IntegerField()

class CESubject (models.Model):
    concentrated_exam = models.ForeignKey(ConcentratedExam)
    #subject = models.ForeignKey()
    prefix = models.CharField(max_length=20)
    difference = models.CharField(max_length=50) # do lech

class CEGroupClass (models.Model):
    group = models.ForeignKey(CEGroup)
#    clazz = models.ForeignKey()

# class StudentClass(models.Model):
#    clazz = models.ForeignKey()
#    student = models.ForeignKey()
#    type = models.ForeignKey()
#    order_number = models.IntegerField()
#    status  = models.CharField(max_length=100)
    
class CERoomStudent(models.Model):
    room = models.ForeignKey(CERoom)
    student_class = models.ForeignKey(StudentClass)
    name_number = models.CharField(max_length=20)
    order_number = models.IntegerField()
    room_number = models.IntegerField()
    absent = models.BooleanField()

class CERoomStudentMark():
#    subject = models.ForeignKey()
    mark = models.IntegerField()
#    student = models.ForeignKey()
    verified_mark = models.IntegerField()
    
# quyendt2612 -- System - Data Type Models
class SystemDataType(models.Model):
    data_type_name = models.CharField(max_length=100)
    detail_assign = models.CharField(max_length=100)
    
class SystemDataTypeForm(forms.ModelForm):
    class Meta:
        model = SystemDataType

# quyendt2612 -- User Type - Data Type Model
class UserTypeDataType(models.Model):
    group_assign_id = models.CharField(max_length=10, primary_key=True)
    user_type_id = models.CharField(max_length=10)
    data_type_id = models.CharField(max_length=10)

class UserTypeDataTypeForm(forms.ModelForm):
    class Meta:
        model = UserTypeDataType

# quyendt2612 -- User Type - Data Type - Class
class UserTypeDataTypeClass(models.Model):
    user_assign_id = models.CharField(max_length=10, primary_key=True)
    group_assign_id = models.ForeignKey(UserTypeDataType)
    user_id = models.CharField(max_length=10)
    class_id = models.CharField(max_length=10)

class UserTypeDataTypeClassForm(forms.ModelForm):
    class Meta:
        model = UserTypeDataTypeClass

# quyendt2612 -- User - Data Key
class UserDataKey(models.Model):
    user_assign_id = models.ForeignKey(UserTypeDataTypeClass)
    phase_mark_id = models.ForeignKey('PhaseMark')
    all_mark = models.CharField(max_length=10)
    oral_test_1 = models.CharField(max_length=10)
    oral_test_2 = models.CharField(max_length=10)
    oral_test_3 = models.CharField(max_length=10)
    oral_test_4 = models.CharField(max_length=10)
    oral_test_5 = models.CharField(max_length=10)
    _15_test_1 = models.CharField(max_length=10)
    _15_test_2 = models.CharField(max_length=10)
    _15_test_3 = models.CharField(max_length=10)
    _15_test_4 = models.CharField(max_length=10)
    _15_test_5 = models.CharField(max_length=10)
    _45_test_1 = models.CharField(max_length=10)
    _45_test_2 = models.CharField(max_length=10)
    _45_test_3 = models.CharField(max_length=10)
    _45_test_4 = models.CharField(max_length=10)
    _45_test_5 = models.CharField(max_length=10)
    _45_test_6 = models.CharField(max_length=10)
    _45_test_7 = models.CharField(max_length=10)
    _45_test_8 = models.CharField(max_length=10)
    exam = models.CharField(max_length=10)

class UserDataKeyForm(forms.ModelForm):
    class Meta:
        unique_together = ('user_assign_id', 'phase_mark_id')

# quyendt2612 -- User Type
class UserType(models.Model):
    user_type_name = models.CharField(max_length=100)
    user_level = models.CharField(max_length=100)
    ineffective = models.BooleanField()
    
class UserTypeForm(forms.ModelForm):
    class Meta:
        model = UserType

# quyendt2612 -- Teaching Assign
class TeachingAssign(models.Model):
    subject_id = models.ForeignKey(Subject)
    class_id = models.ForeignKey(Class)
    summer_id = models.CharField(max_length=10)
    first_term = models.CharField(max_length=10)
    second_term = models.CharField(max_length=10)

class TeachingAssignForm(forms.ModelForm):
    class Meta:
        model = TeachingAssign

# Ngoc Thanh - 5/4/2011
class MarkByPeriod(models.Model):
    #studentclass = models.ForeignKey(StudentClass)# primary key
    #subject_id = models.ForeignKey(Subject)
    #markbyperiod = models.CharField(max_length=10, primary_key=True)
    k15_1 = models.IntegerField(max_length=10)
    k15_2 = models.IntegerField(max_length=10)
    k1t_1 = models.IntegerField(max_length=10)
    k1t_2 = models.IntegerField(max_length=10)
    average_mark = models.IntegerField(max_length=10)
    user_id = models.CharField(max_length=10)
    date_k15_1 = models.DateField()
    date_k15_2 = models.DateField()
    date_k1t_1 = models.DateField()
    date_k1t_2 = models.DateField()
    miss_mark_15 = models.BooleanField()
    miss_mark_1t = models.BooleanField()
    miss_mark_prac = models.BooleanField()
    speak_mark_1 = models.IntegerField(max_length=10)
    date_speak_mark_1 = models.DateField()
    speak_mark_2 = models.IntegerField(max_length=10)
    date_speak_mark_2 = models.DateField()
    
class MarkByPeriodForm(forms.ModelForm):
    class Meta:
        model = MarkByPeriod
        
class SysValueMarkType(models.Model):
    value_mark_type_id = models.CharField(max_length=10, primary_key=True)
    name_value_mark_type = models.CharField(max_length=50)
    is_disable = models.BooleanField(False)

class SysValueMarkTypeForm(forms.ModelForm):
    class Meta:
        model = SysValueMarkType

# D_Log_UserLogin -- quy
class LogUserLogin (models.Model):
    user_id = models.ForeignKey(User)
    login_time = models.DateField()
    logout_time = models.DateField()
    host_name = models.CharField(max_length=100)

#T_DM_PhanHe -- quy
class SystemPartition (models.Model):
    system_name = models.CharField(max_length=100)
    system_index = models.CharField(max_length=10)

# T_DM_Tinh - codai2810
class Province(models.Model):
    name = models.CharField(max_length=30)
    invalid = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

# T_DM_Huyen - codai2810
class District(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province)
    invalid = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

#T_DM_Xa - codai2810
class Village(models.Model):
    name = models.CharField(max_length=30)
    district = models.ForeignKey(District)
    invalid = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

# T_DM_Ap - codai2810
class Hamlet(models.Model):
    name = models.CharField(max_length=30)
    village = models.ForeignKey(Village)
    invalid = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name
    
# T_DM_NhomViPham - codai2810
class InfractionCategories(models.Model):
    name = models.CharField(max_length=250)
    invalid = models.BooleanField()
    def __unicode__(self):
        return self.name

# T_DM_ViPham - codai2810
class InfractionMenu(models.Model):
    infraction_name = models.CharField(max_length=250)
    #DiemTru -- FIXME
    #KhongCheHocKy -- FIXME
    infraction_categories = models.ForeignKey(InfractionCategories)
    times_per_day = models.IntegerField()
    invalid = models.BooleanField()
    initials = models.CharField(max_length=10)
    permitted = models.BooleanField()    # co phep
    unpermitted = models.BooleanField() # khong phep
    late = models.BooleanField()
    def __unicode__(self):
        return self.infraction_name
       
# T_ViPham - codai2810
class Infraction(models.Model):
    student_class = models.ForeignKey(StudentClass)
    infraction = models.ForeignKey(InfractionMenu)
    infraction_date = models.DateField()
    user = models.ForeignKey(User)
    section = models.IntegerField()
    subject = models.ForeignKey(Subject)

