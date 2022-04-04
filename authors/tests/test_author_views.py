from django.test import TestCase, Client
from django.urls import reverse
from common.models import ServerSetting



class TestViews (TestCase):

    def setUp(self):
        self.c = Client()

        ServerSetting.objects.create(
            type='Social Distribution Settings',
            allow_independent_user_login= True,
        )

        self.url_feed = reverse('inboxes:postList')
        self.url_newPost = reverse('posts:newpost')
        # self.url.profile = reverse('myapp:profile')
        # self.url.follow = reverse('myapp:follow')
        self.user_info = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'qwonvwet23',
            'password2': 'qwonvwet23',
            'github': 'https://github.com/johnny123',
            'url':'https://www.imgur.com/dj2kjdf'
        }
        self.login_correct_info = {
            'username': 'johnny',
            'password': 'qwonvwet23',
        }
        
        # Signing up and logging in for self.c
        url_signup = '/accounts/signup/'
        login_url = '/accounts/login/'
        self.c.post(url_signup, self.user_info)
        self.c.post(login_url, self.login_correct_info)
        # self.c.login(username='johnny', password='qwonvwet23')


    def test_profile_GET(self):
        response = self.c.get(reverse('authors:profile', kwargs={'user_id':'johnny'}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "profile.html")
        





