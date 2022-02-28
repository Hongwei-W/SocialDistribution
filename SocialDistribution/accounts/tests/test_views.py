from django.test import TestCase, Client
from django.urls import reverse
import json

# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.signup_url = '/accounts/signup/'
        self.login_url = '/accounts/login/'

        self.signup_correct_info = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'qwonvwet23',
            'password2': 'qwonvwet23',
        }
        self.signup_incorrect_short_password = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': '23we',
            'password2': '23we',
        }
        self.signup_incorrect_not_follow_standard_password = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'johnny123',
            'password2': 'johnny123',
        }
        self.signup_incorrect_missing_parts_form = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'qwonvwet23',
        }
        self.signup_incorrect_unmatch_password = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'qwonvwet23',
            'password2': 'qwonvwet243',
        }
        self.login_correct_info = {
            'username': 'johnny',
            'password': 'qwonvwet23',
        }
        self.login_incorrect_password ={
            'username': 'johnny',
            'password1': 'qwonvwet243'
        }
        self.login_incorrect_missing_parts_no_password = {
            'username': 'johnny',
        }
        return super().setUp()

class SignupTest(TestViews):

    def test_can_signup_view_correctly(self):
        response = self.c.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    # def test_cant_signup_fail_short_password(self):
    #     response = self.c.post(self.signup_url, self.signup_incorrect_short_password)
    #
    #     self.assertEquals(response.status_code, 400)
    #
    # def test_cant_signup_fail_not_follow_standard_password(self):
    #     response = self.c.post(self.signup_url, self.signup_incorrect_not_follow_standard_password)
    #
    #     self.assertEquals(response.status_code, 400)
    #
    # def test_cant_signup_fail_missing_parts_form(self):
    #     response = self.c.post(self.signup_url, self.signup_incorrect_missing_parts_form)
    #
    #     self.assertEquals(response.status_code, 400)
    #
    # def test_cant_signup_unmatch_password(self):
    #     response = self.c.post(self.signup_url, self.signup_incorrect_unmatch_password)
    #
    #     self.assertEquals(response.status_code, 400)
    #
    def test_can_signup_success(self):
        response = self.c.post(self.signup_url, self.signup_correct_info)

        self.assertEquals(response.status_code, 302)


class LoginTest(TestViews):

    def test_can_login_view_correctly(self):
        response = self.c.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_cant_login_incorrect_password(self):
        response = self.c.post(self.login_url, self.login_incorrect_password)

        self.assertEquals(response.status_code, 200)

    def test_cant_login_missing_parts_no_password(self):
        response = self.c.post(self.login_url, self.login_incorrect_missing_parts_no_password)

        self.assertEquals(response.status_code, 200)

    def test_can_login_success(self):
        self.c.post(self.signup_url, self.signup_correct_info)
        response = self.c.post(self.login_url, self.login_correct_info)

        self.assertEqual(response.status_code, 302)



