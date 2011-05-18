# -*- coding: utf-8 -*-
import os.path
import datetime
from school.models import *
from django.contrib.auth.models import User


def to_en(string):
    result = ''
    uni_a = u'ăắẳẵặằâầấẩẫậàáảãạ'
    uni_o = u'óòỏõọơớờởỡợôốồỗộổ'
    uni_i = u'ìĩịỉí'
    uni_u = u'ủùũụúưừứựữử'
    uni_e = u'éèẽẻẹêếềễệể'
    uni_y = u'ýỳỷỹỵ'
    uni_d = u'đ'
    for char in string:
        c = char.lower()
        for cc in ['a','o','i','u','e','d','y']:
            exec("if c in uni_" + cc + ": c = " + "'" + cc + "'" )
        result += c
    return result
        
# make username: example: input: AA, Nguyen Van, 2006 => output: AAnv_2006
#                         input: AA, Nguyen Van       => output: AAnv
def make_username( first_name = None, last_name = None, full_name = None, start_year = None):
    if full_name:
        names = full_name.split(" ")
        last_name = ' '.join(names[:len(names)-1])
        first_name = names[len(names)-1]
    last_name = to_en(last_name)
    first_name = to_en(first_name)
    
    print last_name, " ", first_name
    username = first_name
    if last_name and last_name != '':
        print last_name.split(" ")
        for word in last_name.split(" "):
             if word: username += word[0]
    if start_year:
        username += '_' + str(start_year.time)
    
    i = 0
    username1 = username
    while User.objects.filter( username__exact = username1):
        i = i+1
        username1 = username + '_' + str(i)
    
    return username1
    
def make_default_password( pw):
    return pw
        
        

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
                #raise Exception("Subject does not exist")        


# This function will handle a change of students in a particular class
# where: students: is a list of dictionaries those have 'full_name','birthday','ban' keys
#                                                       'full_name':string, 'birthday': date, 'ban': string,
#                                                       'first_name', 'last_name', 'school_join_date'     
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
def add_student( student = None, start_year = None , year = None, 
                _class = None, term = None, school = None, school_join_date = None ):
        if not ( student and start_year and term and school ):
            raise Exception("Student,Start_Year,Term,School can't not be null")
        if 'full_name' in student:
            names = student['full_name'].split(" ")
            last_name = ' '.join(names[:len(names)-1])
            first_name = names[len(names)-1]
        else:
            last_name = student['last_name']
            first_name = student['first_name']
        if not school_join_date:
            school_join_date = datetime.date.today()
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
            st.school_join_date = school_join_date
            st.start_year_id = start_year
            st.class_id = _class
            st.school_id = school
            st.sex = student['sex']
            
            user = User()
            user.username = make_username( first_name = first_name, last_name = last_name, start_year = start_year)
            user.password = make_default_password( user.username )
            user.save()
            userprofile = UserProfile()
            userprofile.user = user
            userprofile.organization = school
            userprofile.position = 'HOC_SINH'
            userprofile.save() 
            st.user_id = user
            st.save()
            
            for i in range(1,3):
                term1 = year.term_set.get( number__exact = i)
                hk = HanhKiem()
                hk.student_id = st
                hk.term_id = term1
                hk.save()
               
                tb_hoc_ky = TBHocKy()
                tb_hoc_ky.student_id = st
                tb_hoc_ky.term_id = term1
                tb_hoc_ky.save()
              
                tk_diem_danh = TKDiemDanh()
                tk_diem_danh.student_id = st
                tk_diem_danh.term_id = term1
                tk_diem_danh.save()                            
                        
            tb_nam = TBNam()
            tb_nam.student_id = st
            tb_nam.year_id = year
            tb_nam.save()
                    
            subjects = _class.subject_set.all()
            for subject in subjects:
                for i in range(1,3):
                    term1 = year.term_set.get( number__exact = i)
                    the_mark = Mark()
                    the_mark.student_id = st
                    the_mark.subject_id = subject
                    the_mark.term_id = term1
                    the_mark.save()
                                   
                tkmon = TKMon()
                tkmon.student_id = st
                tkmon.subject_id = subject
                tkmon.save()
                
                
                
        #end for student in students


# student: Pupil object
def del_student( student):
    student.disable = True
    student.save()    
    
def completely_del_student( student):
    student.delete()

def add_teacher( first_name = None, last_name = None, full_name = None, school = None,
                 birthday = None, sex = 'N', birthplace = None):
    if full_name:
        names = full_name.split(" ")
        last_name = ' '.join(names[:len(names)-1])
        first_name = names[len(names)-1]
    teacher = Teacher()
    teacher.first_name = first_name
    teacher.last_name = last_name
    teacher.school_id = school
    teacher.birthday = birthday
    teacher.sex = sex
    teacher.birth_place = birthplace
    
    user = User()
    user.username = make_username( first_name = first_name, last_name = last_name )
    user.password = make_default_password( user.username)
    user.save()
    userprofile = UserProfile()
    userprofile.user = user
    userprofile.organization = school
    userprofile.position = 'GIAO_VIEN'
    userprofile.save() 
    
    teacher.user_id = user
    teacher.save()

def del_teacher( teacher):
    teacher.delete()    
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
    
        students = _class.pupil_set.all()
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
            
def get_school(request):
    if request.user.userprofile.organization.level != 'T':
        raise Exception('UserDoesNotHaveAnySchool')
    return Organization.objects.get(id=request.user.userprofile.organization.id)

def get_permission(request):
    if request.user.userprofile.organization.level != 'T':
        raise Exception('UserDoesNotHaveAnySchoolPosition')
    return request.user.userprofile.position

def get_position(request):
    if request.user.userprofile.position == 'HOC_SINH':
        return 1
    elif request.user.userprofile.position == 'GIAO_VU':
        return 2
    elif request.user.userprofile.position == 'GIAO_VIEN':
        return 3
    elif request.user.userprofile.position == 'HIEU_PHO':
        return 4
    elif request.user.userprofile.position == 'HIEU_TRUONG':
        return 4
    else:
        return 0
    
def get_current_year(request):
    school = get_school(request)
    try:
        return school.year_set.latest('time')
    except Exception( 'YearDoesNotExist'):
        return None
		
def get_current_term(request):
    school = get_school(request)
    print "ok"+str(school.status)
    try:
        return school.year_set.latest('time').term_set.get(number = school.status)
    except Exception( 'Term does not exist'):
        return None    

def in_school(request,school_id):
    try:
        school = get_school(request)
        if school == school_id:
            return True
        else:
            return False
    except Exception('UserDoesNotHaveAnySchool'):
        return False
