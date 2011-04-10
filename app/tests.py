"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from django.test.client import Client


class UserFunctionTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_login(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        
    
    def test_logout(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        '''
        NEED MORE HELP!
        '''
        #response = self.client.post('/logout/')
        #self.assertEqual(response.status_code, 301)
        
    def test_user_creation(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'username': 'st01',
            'password1': 'st01',
            'password2': 'st01'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 302)
    
    def test_user_deletion(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'username': 'st02',
            'password1': 'st02',
            'password2': 'st02'
        }
        response = self.client.post('/admin/auth/user/add/', data)
        self.assertEqual(response.status_code, 302)
        '''NEED HELP!
        which data will be sent when deleting action executed
        '''
        #data = {
        #    'action': 'delete_selected',
        #    '_selected_action': '2'
        #}
        #response = self.client.post('/admin/auth/user/', )
        #self.assertEqual(response.status_code, 302)
    
    def test_group_creation(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        data = {
            'name': 'teachers'
        }
        response = self.client.post('/admin/auth/group/add/', data)
        self.assertEqual(response.status_code, 302)
        