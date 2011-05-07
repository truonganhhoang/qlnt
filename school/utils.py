# -*- coding: utf-8 -*-
import os.path
import datetime
from school.models import *

# student: Pupil object,
# old_class: Class object,
# new_class: Class object,
def move_student( student, old_class, new_class):
    if old_class.block.number != new_class.block.number:
        raise Exception("chuyển học sinh tới lớp không cùng khối")
    else:
        subjects = old_class.subject_set.all()
        for subject in subjects:
            subject_in_new_class = new_class.subject_set.filter( name__exact = subject.name)
            if subject_in_new_class:
                the_mark = subject.mark_set.filter( student_id__exact = student)
                the_mark.subject_id = subject_in_new_class
                the_mark.save()
                tkmon = subject.tkmon_set.filter( student_id__exact = student)
                tkmon.subject_id = subject_in_new_class
                tkmon.save()       
            else:
                print student, "moved from ", find.class_id, " to ", _class
                print "but the subject: ", subject, " doesn't exist"
                raise Exception("Subject does not exist")        


# This function will handle a change of students in a particular class
# where: students: is a list of dictionaries those have 'full_name','birthday','ban' keys
#                                                       'full_name':string, 'birthday': date, 'ban': string, 
#        start_year: StartYear object, 'term': Term object
#        year: Year object    
#        _class : is a Class object
#        school : is a School object   
# TO DO: if student exists and _class is defferent from student's class:
#              . disassociated student's marks, "TBMon", "TKMon", 
#              . change the student's class into _class
#              . transfer the associated marks to the new corresponding mark table, "TBMon", "TKMon".  
#        if student exists and _class is the same with student's class:
#              . do nothing
#        if student does not exist:
#              . add the student to db  
#              . lets student belong to _class
#              . add: marks for each subject, "khenthuong", "kiluat", "diemdanh", "TKDiemDanh", "TBMon"
#                     "HanhKiem", "TKMon", "TBHocKy", "TBNam"
def add_student( student = None, start_year = None, year = None, _class = None, term = None, school = None ):
        names = student['full_name'].split(" ")
        last_name = ' '.join(names[:len(names)-1])
        first_name = names[len(names)-1]
        birthday = student['birthday']
        ban = student['ban']
        find = start_year.pupil_set.filter( first_name__exact = first_name)\
                                   .filter(last_name__exact = last_name)\
                                   .filter(birthday__exact = birthday)
        if find: # the student exists:
            find = find[0]
            find.class_id = _class
            if _class is not find.class_id:
                move_student( find, find.class_id, _class)
            else:
                pass
        else:    # the student does not exist
            st = Pupil()
            st.first_name = first_name
            st.last_name = last_name
            st.birthday = birthday
            st.ban_dk = ban
            st.school_join_date = datetime.date.today()
            st.start_year_id = start_year
            st.class_id = _class
            st.save()
            
            subjects = _class.subject_set.all()
            for subject in subjects:
                the_mark = Mark()
                the_mark.student_id = st
                the_mark.subject_id = subject
                the_mark.term_id = term
                the_mark.save()
                
                tkmon = TKMon()
                tkmon.student_id = st
                tkmon.subject_id = subject
                tkmon.save()
                
                hk = HanhKiem()
                hk.student_id = st
                hk.term_id = term
                hk.save()
                
                tb_hoc_ky = TBHocKy()
                tb_hoc_ky.student_id = st
                tb_hoc_ky.term_id = term
                tb_hoc_ky.save()
                
                tb_nam = TBNam()
                tb_nam.student_id = st
                tb_nam.year_id = year
                tb_nam.save()
                
                tk_diem_danh = TKDiemDanh()
                tk_diem_danh.student_id = st
                tk_diem_danh.term_id = term
                tk_diem_danh.save()                            
        #end for student in students


# student: Pupil object
def del_student( student):
    student.disable = True
    student.save()    
    
def completely_del_student( student):
    student.delete()

# subject_name: string, teacher : Teacher object, _class : Class object
def add_subject( subject_name = None, hs = 1, teacher = None, _class = None, term = None):
    find = _class.subject_set.filter( name__exact = subject_name)
    if find:
        raise Exception("SubjectExist")
    else:
        subject = Subject()
        subject.name = subject_name
        subject.hs = hs
        subject.teacher_id = teacher
        subject.class_id = _class
        subject.save()
    
        students = _class.student_set.all()
        for student in students:
            mark = Mark()
            mark.student_id = student
            mark.subject_id = subject
            mark.term_id = term
            mark.save()
            
            tkmon = TKMon()
            tkmon.student_id = student
            tkmon.subject_id = subject
            tkmon.save()

def completely_del_subject( subject):
    subject.delete()                
            
