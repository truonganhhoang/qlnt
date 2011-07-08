
from django.test import TestCase

class ShoolTest(TestCase):
    def test_school_add(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'school_code': '123',    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '012322125',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/school/school/')
        self.assertContains(response, "THPT ABC XYZ", status_code=200)

    def test_school_duplicated_addition(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'school_code': '123',    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '012322125',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        data = {
            'school_code': '123',    
            'name': 'THPT ABC XYZ',
            'address': '123 fsafasfas akhjkas',
            'phone': '523523623',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 200)
    def test_school_add_miss_field(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '012322125',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/admin/school/school/')
        self.assertNotContains(response, "THPT ABC XYZ", 200)
        
    def test_school_add_not_validate_field(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '0123basg125',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/admin/school/school/')
        self.assertNotContains(response, "THPT ABC XYZ", 200)
        data = {    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '01234325125',
            'web_site': 'abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/admin/school/school/')
        self.assertNotContains(response, "THPT ABC XYZ", 200)
        
    def test_delete_school(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'school_code': '123',    
            'name': 'THPT ABC XYZ',
            'address': '123 kasfhjkasfhk akhjkas',
            'phone': '012322125',
            'web_site': 'http://abc-xyz.com'
        }
        response = self.client.post('/admin/school/school/add/', data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/school/school/')
        self.assertContains(response, "THPT ABC XYZ", status_code=200)
        data = {
            'action': 'delete_selected',
            '_selected_action': '1',
            'post': 'yes'
        }
        response = self.client.post('/admin/school/school/',data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/school/school/')
        self.assertNotContains(response, "THPT ABC XYZ", 200)
        
class TeacherTest(TestCase):
    def test_teacher_add_without_required_field(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'first_name': 'Anh',    
            'last_name': 'Nguyen Tuan',
            'birth_place': 'Ha Noi',
            'phone':'083593503',
            'current_address':'Cau Giay, Ha Noi',
            'email':'anh_nt@vnu.edu.vn'
        }
        response = self.client.post('/admin/school/teacher/add/', data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/admin/school/teacher/')
        self.assertNotContains(response, "Anh Nguyen Tuan", 200)
        
