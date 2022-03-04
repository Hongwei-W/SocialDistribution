from django.test import TestCase, Client
from django.urls import reverse


class TestViews (TestCase):

    def setUp(self):
        self.c = Client()

        self.url_feed = reverse('postList')
        self.url_post = reverse('postDetail')
        self.url_newPost = reverse('newpost')
        self.url.profile = reverse('profile')
        self.url.follow = reverse('follow')
        self.user_info = {
            'username': 'johnny',
            'email': 'johnny@123.com',
            'password1': 'qwonvwet23',
            'password2': 'qwonvwet23',
        }

        url_signup = reverse('accounts:signup')
        self.c.post(url_signup, self.user_info)

    def test_can_feed_GET(self):

        response = self.c.get(self.url_feed)

        self.assertEquals(response.status_code, 200)





