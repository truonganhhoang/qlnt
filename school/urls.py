from school import views, helptools
from django.conf.urls.defaults import patterns, url 


urlpatterns = patterns('',
    url(r'^$', 'school.views.school_index', name = "school_index"),
    

    # author: luulethe@gmail.com (cac ham den cho gach)
    
    #-----------------------------------------------------------------------
    # 2 ham nay dung de test, tao tat ca cac thong tin con thieu cho sinh vien
    # sau nay hoan thien, co the bo di    
    url(r'thu$','school.makeTest.thu'),
    url(r'markTable$','school.viewMark.markTable'),
    url(r'markTable/(?P<term_id>\w+)$','school.viewMark.markTable'),
    url(r'markTable/(?P<term_id>\w+)/(?P<class_id>\w+)$','school.viewMark.markTable'),
    url(r'markTable/(?P<term_id>\w+)/(?P<class_id>\w+)/(?P<subject_id>\w+)$','school.viewMark.markTable'),
    url(r'markTable/(?P<term_id>\w+)/(?P<class_id>\w+)/(?P<subject_id>\w+)/(?P<move>\w+)$','school.viewMark.markTable'),
    
    url(r'markForTeacher$','school.viewMark.markForTeacher'),
    url(r'markForTeacher/(?P<type>\w+)$','school.viewMark.markForTeacher'),
    url(r'markForTeacher/(?P<type>\w+)/(?P<term_id>\w+)$','school.viewMark.markForTeacher'),
    url(r'markForTeacher/(?P<type>\w+)/(?P<term_id>\w+)/(?P<subject_id>\w+)$','school.viewMark.markForTeacher'),
    url(r'markForTeacher/(?P<type>\w+)/(?P<term_id>\w+)/(?P<subject_id>\w+)/(?P<move>\w+)$','school.viewMark.markForTeacher'),
    
    url(r'markForAStudent/(?P<class_id>\w+)/(?P<student_id>\w+)$','school.viewMark.markForAStudent'),
    #url(r'markForASubject/(?P<subject_id>\w+)','school.viewMark.markForASubject'),
    
    url(r'saveMark$','school.viewMark.saveMark'),
    url(r'sendSMSMark$','school.viewMark.sendSMSMark'),
    url(r'sendSMSResult/(?P<class_id>\w+)/(?P<termNumber>\w+)$','school.viewFinish.sendSMSResult'),
    url(r'sendSMSResult/(?P<class_id>\w+)$','school.viewFinish.sendSMSResult'),
    
    url(r'saveHocLai$','school.viewFinish.saveHocLai'),
    url(r'saveRenLuyenThem$','school.viewFinish.saveRenLuyenThem'),
    
	# xep loai hoc luc theo lop, gom co xep loai k1, k2 va ca nam
    url(r'xepLoaiHlTheoLop/(?P<class_id>\w+)/(?P<termNumber>\w+)$','school.viewFinish.xepLoaiHlTheoLop'),    
    url(r'xlCaNamTheoLop/(?P<class_id>\w+)/(?P<type>\w+)$','school.viewFinish.xlCaNamTheoLop'),
    url(r'thilai/(?P<class_id>\w+)$','school.viewFinish.thilai'),
    url(r'renluyenthem/(?P<class_id>\w+)$','school.viewFinish.renluyenthem'),
    url(r'capNhapMienGiam/(?P<class_id>\w+)/(?P<student_id>\w+)$','school.viewMark.capNhapMienGiam'),
    		
	# tinh diem tong ket hoc luc toan truong	
	# tong ket hoc ky, tinh toan bo hoc luc cua hoc sinh trong toan truong
	# xem xet lop nao da tinh xong, lop nao chua xong de hieu truong co the chi dao
	# co chuc nang ket thuc hoc ky	
    url(r'finishYear/(?P<year_id>\w+)$','school.viewFinish.finishYear'),
    url(r'finishTerm/(?P<term_id>\w+)$','school.viewFinish.finishTerm'),    
    url(r'finish$','school.viewFinish.finish'),    
    #thong ke toan truong
    #url(r'countInSchool/(?P<year_id>\w+)' , 'school.viewCount.countInSchool'),
    url(r'report$' , 'school.writeExcel.report'), 
    
    url(r'countInSchool$' , 'school.viewCount.countInSchool'), 
    url(r'countPractisingInTerm/(?P<term_id>\w+)$','school.viewCount.countPractisingInTerm'),
    url(r'countPractisingInYear/(?P<year_id>\w+)$','school.viewCount.countPractisingInYear'),
    url(r'countLearningInTerm/(?P<term_id>\w+)$','school.viewCount.countLearningInTerm'),
    url(r'countLearningInYear/(?P<year_id>\w+)$','school.viewCount.countLearningInYear'),
    url(r'countAllInTerm/(?P<term_id>\w+)$','school.viewCount.countAllInTerm'),
    url(r'countAllInYear/(?P<year_id>\w+)$','school.viewCount.countAllInYear'),
    #thong ke hoc luc, hanh kiem, danh hieu
    url(r'count1/(?P<year_id>\w+)/(?P<number>\w+)/(?P<type>\w+)$','school.viewCount.count1'),
    url(r'count1/(?P<year_id>\w+)/(?P<number>\w+)$','school.viewCount.count1'),
    url(r'count1$','school.viewCount.count1'),
    url(r'count2/(?P<type>\w+)/(?P<modeView>\w+)$','school.viewCount.count2'),
    url(r'count2/(?P<type>\w+)/(?P<modeView>\w+)/(?P<year_id>\w+)/(?P<number>\w+)/(?P<index>\w+)$','school.viewCount.count2'),
    url(r'count2/(?P<type>\w+)/(?P<modeView>\w+)/(?P<year_id>\w+)/(?P<number>\w+)/(?P<index>\w+)/(?P<isExcel>\w+)$','school.viewCount.count2'),
    
    url(r'printMarkBook$' , 'school.writeExcel.printMarkBook'), 
    url(r'printMarkBook/(?P<termNumber>\w+)/(?P<class_id>([0-9-])*)$' , 'school.writeExcel.printMarkBook'), 
    url(r'markExcel/(?P<term_id>\w+)/(?P<subject_id>\w+)$' , 'school.writeExcel.markExcel'), 
    url(r'importMark/(?P<term_id>\w+)/(?P<subject_id>\w+)$' , 'school.importMark.importMark'), 
    url(r'importMark/(?P<term_id>\w+)/(?P<subject_id>\w+)$' , 'school.importMark.importMark'), 

    url(r'printMarkForClass$' , 'school.writeExcel.printMarkForClass'), 
    url(r'printMarkForClass/(?P<termNumber>\w+)/(?P<class_id>\w+)$' , 'school.writeExcel.printMarkForClass'), 
    
    
    #------------------------------------------------------------------

    url(r'classes$', 'school.views.classes', name = "classes"),
    url(r'classtab/(?P<block_id>\w+)$', 'school.views.classtab'),
    url(r'classtab$', 'school.views.classtab'),
    url(r'addclass$', 'school.views.addClass'),
    url(r'hanhkiem/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)$', 'school.views.hanh_kiem'),
    url(r'hanhkiem/(?P<class_id>\w+)$', 'school.views.hanh_kiem'),
    url(r'hanhkiem$', 'school.views.hanh_kiem'),
    url(r'teachers_tab/(?P<sort_type>\w+)/(?P<sort_status>\w+)$', 'school.views.teachers_tab'),
    url(r'teachers_tab$', 'school.views.teachers_tab'),
    url(r'teachers_in_team/(?P<team_id>\w+)$', 'school.views.teachers_in_team'),
    url(r'teachers/(?P<sort_type>\w+)/(?P<sort_status>\w+)$', 'school.views.teachers'),
    url(r'teachers$', 'school.views.teachers'),
    url(r'team/(?P<team_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)$', 'school.views.team'),
    url(r'team/(?P<team_id>\w+)$', 'school.views.team'),
    url(r'teachers_in_group/(?P<group_id>\w+)$', 'school.views.teachers_in_group'),
    url(r'students/organize/(?P<class_id>\w+)/(?P<type>\w+)$', 'school.views.organize_students'),
    url(r'viewTeacherDetail/(?P<teacher_id>\w+)$', 'school.views.viewTeacherDetail'),
    url(r'viewStudentDetail/(?P<student_id>\w+)', 'school.views.viewStudentDetail', name ='student_detail'),
    url(r'getStudent/(?P<student_id>\w+)', 'school.views.student'),
    url(r'viewClassDetail/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)', 'school.views.viewClassDetail'),
    url(r'viewClassDetail/(?P<class_id>\w+)', 'school.views.viewClassDetail'),
    url(r'subjectPerClass/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)', 'school.views.subjectPerClass'),
    url(r'subjectPerClass/(?P<class_id>\w+)', 'school.views.subjectPerClass'),
    url(r'viewSubjectDetail/(?P<subject_id>\w+)', 'school.views.viewSubjectDetail'),
    url(r'start_year$','school.views.b1', name = "start_year"),

   
    url(r'khenthuong/(?P<student_id>\w+)/add$', 'school.views.add_khen_thuong'),
    url(r'khenthuong/(?P<kt_id>\w+)/delete$', 'school.views.delete_khen_thuong'),    
    url(r'khenthuong/(?P<kt_id>\w+)/edit$', 'school.views.edit_khen_thuong'),    
    url(r'khenthuong/(?P<student_id>\w+)$', 'school.views.khen_thuong'),

    
    url(r'kiluat/(?P<student_id>\w+)/add$', 'school.views.add_ki_luat'),
    url(r'kiluat/(?P<kt_id>\w+)/edit$', 'school.views.edit_ki_luat'),
    url(r'kiluat/(?P<kt_id>\w+)/delete$', 'school.views.delete_ki_luat'),    
    url(r'kiluat/(?P<student_id>\w+)$', 'school.views.ki_luat'),
    url(r'diemdanhhs/(?P<student_id>\w+)/(?P<view_type>\w+)$', 'school.views.diem_danh_hs'),
    url(r'diemdanhhs/(?P<student_id>\w+)$', 'school.views.diem_danh_hs'),
    url(r'dsnghi/(?P<class_id>\w+)/(?P<day>\w+)/(?P<month>\w+)/(?P<year>\w+)$', 'school.views.ds_nghi'),
    url(r'diemdanh/(?P<class_id>\w+)/(?P<day>\w+)/(?P<month>\w+)/(?P<year>\w+)$', 'school.views.diem_danh'),
    url(r'diemdanh/(?P<class_id>\w+)$', 'school.views.time_select'),
    url(r'diemdanh', 'school.views.tnc_select'),
    url(r'change_index/(?P<target>\w+)/(?P<class_id>\w+)$', 'school.views.change_index'),
    url(r'password_change$', 'school.views.password_change'),
    url(r'username_change$', 'school.views.username_change'),
    url(r'student/account/(?P<student_id>\w+)$','school.views.student_account'),
    url(r'teacher/account/(?P<teacher_id>\w+)$','school.views.teacher_account'),
    url(r'movestudent/(?P<student_id>\w+)$','school.views.move_one_student'),
    url(r'movestudents$','school.views.move_students'),

    url(r'generate/(?P<class_id>\w+)/(?P<object>\w+)/$','school.views.class_generate', name = 'class_generate'),
    url(r'generate_teacher/(?P<type>\w+)/$','school.views.teacher_generate', name = 'teacher_generate'),

    url(r'start_year/import/student/(?P<class_id>\w+)/(?P<request_type>\w+)$', 'school.views.student_import'),
    url(r'start_year/import$', 'school.views.nhap_danh_sach_trung_tuyen'),
    url(r'start_year/import/list$', 'school.views.danh_sach_trung_tuyen', name = "imported_list"),
    url(r'start_year/manual$', 'school.views.manual_adding', name = "manual_adding"),
    url(r'import/teacher/(?P<request_type>\w+)$', 'school.views.teacher_import', name = "teacher_import"),

    url(r'deleteTeacher/(?P<teacher_id>\w+)/(?P<team_id>\w+)$', 'school.views.deleteTeacher'),
    url(r'deleteSubject/(?P<subject_id>\w+)', 'school.views.deleteSubject'),
    url(r'deleteStudentInSchool/(?P<student_id>\w+)', 'school.views.deleteStudentInSchool'),
    url(r'deleteStudentInClass/(?P<student_id>\w+)', 'school.views.deleteStudentInClass'),
    url(r'deleteClass/(?P<class_id>\w+)/(?P<block_id>\w+)$', 'school.views.deleteClass'),
    url(r'deleteAllStudentsInClass/(?P<class_id>\w+)$','school.views.deleteAllStudentsInClass'),


    #top menu
    url(r'years/$', 'school.views.years', name = "years"),
    url(r'sms/$', 'school.sms_views.manual_sms', name = "manual_sms"),
    url(r'sms/excel/$', 'school.sms_views.excel_sms', name = "excel_sms"),
    url(r'sms/sent/$', 'school.sms_views.sent_sms', name = "sent_sms"),
    url(r'sms/failed/$', 'school.sms_views.failed_sms', name = 'failed_sms'),
    url(r'setup/$', 'school.views.setup', name = 'setup'),
    #side menu
    url(r'classlabels/$', 'school.views.class_label', name = "class_label"),
    url(r'info/$', 'school.views.info', name = "info"),
    url(r'classify/$', 'school.views.classify', name = "classify"),
    #url(r'^school/test$','school.views.test'), 
    
    #help
    #url(r'recover/$', 'school.helptools.recover_marktime', name = "recover_marktime"),
    url(r'sync_index/$', 'school.helptools.sync_index', name = "sync_index"),
    #url(r'sync_subject/$', 'school.helptools.sync_subject', name='sync_subject'),
    url(r'check_logic/$', 'school.helptools.check_logic', name='check_logic'),
    #url(r'sync_subject_type/$', 'school.helptools.sync_subject_type', name='sync_subject_type'),
    #url(r'sync_subject_primary/$', 'school.helptools.sync_subject_primary', name='sync_subject_primary'),
    #url(r'test_table/$', 'school.helptools.test_table'),
    url(r'copy_hanh_kiem_data/$','school.helptools.copy_hanh_kiem_data'),
    url(r'make_setting/$','school.helptools.make_setting'),
    url(r'convert_1n_mn/$', 'school.helptools.convert_data_1n_mn'),
	)
