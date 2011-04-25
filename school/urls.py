from django.conf.urls.defaults import *


urlpatterns = patterns('',
	url(r'^$', 'school.views.school'),
	url(r'classes/add$', 'school.views.add_class'),
    url(r'teachers/add$', 'school.views.add_teacher'),
    url(r'subjects/add$', 'school.views.add_subject'),
    url(r'students/add$', 'school.views.add_pupil'),
    url(r'mark_table$','school.views.mark_table'), 

    url(r'students/import$', 'school.views.nhap_danh_sach_trung_tuyen'),
    url(r'students/import/list$', 'school.views.danh_sach_trung_tuyen'),
    #url(r'^school/test$','school.views.test'), 
                           
	
	)
