
from django.conf.urls.defaults import patterns, url 


urlpatterns = patterns('',
    url(r'^$', 'school.views.school_index', name = "school_index"),

    
    # author: luulethe@gmail.com (cac ham den cho gach)
    
    #-----------------------------------------------------------------------
    # 2 ham nay dung de test, tao tat ca cac thong tin con thieu cho sinh vien
    # sau nay hoan thien, co the bo di    
    url(r'createTbNam/(?P<year_id>\w+)','school.viewMark.createTbNam'),
    url(r'createAllInfoInTerm/(?P<term_id>\w+)','school.viewMark.createAllInfoInTerm'),
    url(r'markTable/(?P<class_id>\w+)','school.viewMark.markTable'),
    url(r'markForAStudent/(?P<class_id>\w+)/(?P<student_id>\w+)','school.viewMark.markForAStudent'),
    url(r'markForASubject/(?P<subject_id>\w+)','school.viewMark.markForASubject'),
	# xep loai hoc luc theo lop, gom co xep loai k1, k2 va ca nam
    url(r'xepLoaiHlTheoLop/(?P<class_id>\w+)','school.viewFinish.xepLoaiHlTheoLop'),	
    url(r'xlCaNamTheoLop/(?P<class_id>\w+)','school.viewFinish.xlCaNamTheoLop'),		
	# tinh diem tong ket hoc luc toan truong	
	# tong ket hoc ky, tinh toan bo hoc luc cua hoc sinh trong toan truong
	# xem xet lop nao da tinh xong, lop nao chua xong de hieu truong co the chi dao
	# co chuc nang ket thuc hoc ky	
    url(r'finishYear/(?P<year_id>\w+)','school.viewFinish.finishYear'),
    url(r'finishTerm/(?P<term_id>\w+)','school.viewFinish.finishTerm'),    
    url(r'finish$','school.viewFinish.finish'),    
    #thong ke toan truong
    #url(r'countInSchool/(?P<year_id>\w+)' , 'school.viewCount.countInSchool'),
    url(r'countInSchool$' , 'school.viewCount.countInSchool'), 
    url(r'countPractisingInTerm/(?P<term_id>\w+)','school.viewCount.countPractisingInTerm'),
    url(r'countPractisingInYear/(?P<year_id>\w+)','school.viewCount.countPractisingInYear'),
    url(r'countLearningInTerm/(?P<term_id>\w+)','school.viewCount.countLearningInTerm'),
    url(r'countLearningInYear/(?P<year_id>\w+)','school.viewCount.countLearningInYear'),
    url(r'countAllInTerm/(?P<term_id>\w+)','school.viewCount.countAllInTerm'),
    url(r'countAllInYear/(?P<year_id>\w+)','school.viewCount.countAllInYear'),

    #------------------------------------------------------------------

    url(r'classes/(?P<sort_type>\w+)/(?P<sort_status>\w+)/(?P<page>\w+)$', 'school.views.classes'),
    url(r'classes$', 'school.views.classes', name = "classes"),
    url(r'addclass$', 'school.views.addClass'),
    url(r'hanhkiem/(?P<class_id>\w+)/(?P<term_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)$', 'school.views.hanh_kiem'),
    url(r'hanhkiem/(?P<class_id>\w+)/(?P<term_id>\w+)', 'school.views.hanh_kiem'),
    url(r'hanhkiem/(?P<class_id>\w+)', 'school.views.hanh_kiem'),
    url(r'teachers/(?P<sort_type>\w+)/(?P<sort_status>\w+)/(?P<page>\w+)$', 'school.views.teachers'),
    url(r'teachers$', 'school.views.teachers'),
    url(r'students/(?P<sort_type>\w+)/(?P<sort_status>\w+)/(?P<page>\w+)$', 'school.views.students'),
    url(r'students$', 'school.views.students'),
    url(r'viewClassDetail/(?P<class_id>\w+)', 'school.views.viewClassDetail'),
    url(r'viewTeacherDetail/(?P<teacher_id>\w+)$', 'school.views.viewTeacherDetail'),
    url(r'viewStudentDetail/(?P<student_id>\w+)', 'school.views.viewStudentDetail'),
    url(r'studentPerClass/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)/(?P<page>\w+)', 'school.views.studentPerClass'),
    url(r'studentPerClass/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)', 'school.views.studentPerClass'),
    url(r'studentPerClass/(?P<class_id>\w+)', 'school.views.studentPerClass'),
    url(r'subjectPerClass/(?P<class_id>\w+)/(?P<sort_type>\w+)/(?P<sort_status>\w+)', 'school.views.subjectPerClass'),
    url(r'subjectPerClass/(?P<class_id>\w+)', 'school.views.subjectPerClass'),
	#url(r'viewSubjectDetail/(?P<subject_id>\w+)', 'school.views.viewSubjectDetail'),
    url(r'start_year$','school.views.b1', name = "start_year"),
    url(r'khenthuong/(?P<student_id>\w+)/add', 'school.views.add_khen_thuong'),
    url(r'khenthuong/(?P<kt_id>\w+)/delete', 'school.views.delete_khen_thuong'),    
    url(r'khenthuong/(?P<kt_id>\w+)/edit', 'school.views.edit_khen_thuong'),    
    url(r'khenthuong/(?P<student_id>\w+)', 'school.views.khen_thuong'),
    url(r'kiluat/(?P<student_id>\w+)/add', 'school.views.add_ki_luat'),
    url(r'kiluat/(?P<kt_id>\w+)/edit', 'school.views.edit_ki_luat'),
    url(r'kiluat/(?P<kt_id>\w+)/delete', 'school.views.delete_ki_luat'),    
    url(r'kiluat/(?P<student_id>\w+)', 'school.views.ki_luat'),
    url(r'diemdanh/(?P<class_id>\w+)/(?P<day>\w+)/(?P<month>\w+)/(?P<year>\w+)', 'school.views.diem_danh'),
    url(r'diemdanh/(?P<class_id>\w+)', 'school.views.time_select'),
    url(r'diemdanhhs/(?P<student_id>\w+)', 'school.views.diem_danh_hs'),    
    url(r'start_year/import$', 'school.views.nhap_danh_sach_trung_tuyen'),
    url(r'start_year/import/list$', 'school.views.danh_sach_trung_tuyen', name = "imported_list"),
    url(r'start_year/manual$', 'school.views.manual_adding', name = "manual_adding"),
    url(r'deleteTeacher/(?P<teacher_id>\w+)', 'school.views.deleteTeacher'),
    url(r'deleteSubject/(?P<subject_id>\w+)', 'school.views.deleteSubject'),
    url(r'deleteStudentInSchool/(?P<student_id>\w+)', 'school.views.deleteStudentInSchool'),
    url(r'deleteStudentInClass/(?P<student_id>\w+)', 'school.views.deleteStudentInClass'),
    url(r'deleteClass/(?P<class_id>\w+)', 'school.views.deleteClass'),
    
    #top menu
    url(r'years/$', 'school.views.years', name = "years"),
    #side menu
    url(r'classlabels/$', 'school.views.class_label', name = "class_label")
    #url(r'^school/test$','school.views.test'), 
    
	)
