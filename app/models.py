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

class StudentClass(models.Model):
#    clazz = models.ForeignKey()
#    student = models.ForeignKey()
#    type = models.ForeignKey()
    order_number = models.IntegerField()
    status  = models.CharField(max_length = 100)
    
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
    