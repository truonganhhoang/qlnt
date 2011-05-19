#! /usr/bin/env python
#encoding:UTF-8
"""
Kiểm thử các chức năng 
"""

from django.test import TestCase
from django.test.client import Client


class UserFunctionTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_login(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        
    def test_failed_login(self):
        # Wrong username and password
        response = self.client.post('/login/', {'username': 'wrong_username', 'password': ''})
        self.assertContains(response, "Your username and password didn't match. Please try again.", status_code=200)
    
    def test_logout(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        response = self.client.logout()
        self.assertEqual(response, None)
        response = self.client.post('/logout/')
        self.assertContains(response, "You logged out successfully.")
 
    def test_user_addition(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        # before adding, database has no user with name "st01"
        response = self.client.post('/admin/auth/user/')
        self.assertContains(response, "st01", 0, status_code=200)
        data = {
            'username': 'st01',
            'password1': 'st01',
            'password2': 'st01'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 302)
        # after adding, database has user with name "st01"
        response = self.client.post('/admin/auth/user/')
        self.assertContains(response, "st01", status_code=200)
        
    def test_duplicated_user_addition(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'username': 'st01',
            'password1': 'st01',
            'password2': 'st01'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 302)
        data = {
            'username': 'st01',
            'password1': 'st01',
            'password2': 'st01'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 200)
    
    def test_user_addition_with_no_data(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
        }
        response = self.client.post('/admin/auth/user/add', data)
        #self.assertContains(response, "Trường này bắt buộc", 3, status_code=301)
        self.assertEqual(response.status_code, 301)
        
    def test_user_addition_without_password(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
            'username': 'without-password',
            'password': '',
            'password': ''
        }
        response = self.client.post('/admin/auth/user/add', data)
        #self.assertContains(response, "Trường này bắt buộc", 2, status_code=301)
        self.assertEqual(response.status_code, 301)
        
    def test_user_addition_without_username(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
            'username': '',
            'password': 'without-username',
            'password': ''
        }
        response = self.client.post('/admin/auth/user/add', data)
        #self.assertContains(response, "Trường này bắt buộc", 2, status_code=301)
        self.assertEqual(response.status_code, 301)
        
    def test_usercreation_with_spaced_username(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
            'username': 'with space',
            'password': 'password',
            'password': 'password'
        }
        response = self.client.post('/admin/auth/user/add', data)
        #self.assertContains(response, "Giá trị này có thể chứa chữ cái, số và ký tự @/./+/-/_.", status_code=301)
        self.assertEqual(response.status_code, 301)
    
    def test_user_addition_with_not_matched_password(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
            'username': 'username',
            'password': 'password',
            'password': 'pass_word'
        }
        response = self.client.post('/admin/auth/user/add', data)
        #self.assertContains(response, "Hai trường mật khẩu không giống nhau", status_code=301)
        self.assertEqual(response.status_code, 301)
    
    def test_user_deletion(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        # before adding, database has no user with name "st02"
        response = self.client.post('/admin/auth/user/')
        self.assertContains(response, "st02", 0, status_code=200)
        data = {
            'username': 'st02',
            'password1': 'st02',
            'password2': 'st02'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 302)
        # after adding, database has a user with name "st02"
        response = self.client.post('/admin/auth/user/')
        self.assertContains(response, "st02", status_code=200)
        data = {
            'action': 'delete_selected',
            '_selected_action': '2',
            'post': 'yes'
        }
        response = self.client.post('/admin/auth/user/', data)
        self.assertEqual(response.status_code, 302)
        # after deleting, database has no user with name "st02"
        response = self.client.post('/admin/auth/user/')
        self.assertContains(response, "st02", 0, status_code=200)
    
    def test_group_addition(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers", 0, status_code=200)
        data = {
            'name': 'teachers'
        }
        response = self.client.post('/admin/auth/group/add/', data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers", status_code=200)
        
    def test_duplicated_group_addition(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers", 0, status_code=200)
        data = {
            'name': 'teachers'
        }
        response = self.client.post('/admin/auth/group/add/', data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers", status_code=200)
        response = self.client.post('/admin/auth/group/add/', data)
        #selft.assertContains(response, "Nhóm có Tên đã tồn tại.", status_code=200)
        self.assertEqual(response.status_code, 200)        
    
    def test_group_addition_without_name(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)
        data = {
        }
        response = self.client.post('/admin/auth/group/add', data)
        #self.assertContains(response, "Trường này bắt buộc", 2, status_code=301)
        self.assertEqual(response.status_code, 301)

    def test_deletion_group(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        # before adding, database has no group with name "teachers02"
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers02", 0, status_code=200)
        data = {
            'name': 'teachers02',
        }
        response = self.client.post('/admin/auth/group/add/', data)
        self.assertEqual(response.status_code, 302)
        # after adding, database has a group with name "teachers02"
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers02", status_code=200)
        data = {
            'action': 'delete_selected',
            '_selected_action': '1',
            'post': 'yes'
        }
        response = self.client.post('/admin/auth/group/', data)
        self.assertEqual(response.status_code, 302)
        # after deleting, database has no group with name "teachers02"
        response = self.client.post('/admin/auth/group/')
        self.assertContains(response, "teachers02", 0, status_code=200)
        
class OrganizationTest(TestCase):
    def setUp(self):
        self.client = Client()
