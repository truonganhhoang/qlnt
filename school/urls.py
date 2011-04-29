from django.conf.urls.defaults import patterns, url 


urlpatterns = patterns('',
	url(r'^$', 'school.views.school_index'),
	url(r'mark_table/(?P<class_id>\w+)','school.views.mark_table'),
	url(r'markForAStudent/(?P<class_id>\w+)/(?P<student_id>\w+)','school.views.markForAStudent'),

	url(r'xepLoaiHkTheoLop/(?P<class_id>\w+)','school.views.xepLoaiHkTheoLop'),

    url(r'classes$', 'school.views.classes'),
    url(r'teachers$', 'school.views.teachers'),
    url(r'students$', 'school.views.students'),
    url(r'viewClassDetail/(?P<class_id>\w+)', 'school.views.viewClassDetail'),
    url(r'viewTeacherDetail/(?P<teacher_id>\w+)', 'school.views.viewTeacherDetail'),
    url(r'viewStudentDetail/(?P<student_id>\w+)', 'school.views.viewStudentDetail'),
    url(r'studentPerClass/(?P<class_id>\w+)', 'school.views.studentPerClass'),
    url(r'subjectPerClass/(?P<class_id>\w+)', 'school.views.subjectPerClass'),
    url(r'start_year$','school.views.b1', name = "start_year"),
    
    url(r'start_year/import$', 'school.views.nhap_danh_sach_trung_tuyen'),
    url(r'start_year/import/list$', 'school.views.danh_sach_trung_tuyen', name = "imported_list"),
    #url(r'^school/test$','school.views.test'), 
                           
	
	)
