from django.test import Client, TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from authors.models import Author
from authors.serializers import *
from posts.serializers import *
import json
from SocialDistribution import urls
from requests.auth import HTTPBasicAuth


class TestPostsAPIViews(APITestCase):

    def setUp(self):
        self.c = Client()
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

    def test_AuthorsAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        print("author found " + author.username)
        response = self.client.get(reverse('service-authors'), auth=HTTPBasicAuth("admin", "admin"))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.data['items'], list)
    
    def test_AuthorAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        print("author found " + author.username)
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        # sample_post = {'title': 'test_post', 'content': 'test_content', 'description': 'test_description', 'content_type': 'text/plain', 'author': 'johnny'}
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        # serializer = PostSerializer(sample_post)
        # headerInfo = {'Content-Type': 'application/json' }
        # print(serializer.data)
        # response = self.client.post(reverse('service-posts', kwargs={'author':author.uuid}), headers=headerInfo, auth=HTTPBasicAuth("admin", "admin"), data=serializer.data, format='json')
        response = self.client.get(reverse('service-post', kwargs={'pk':sample_post.uuid, 'author':author.uuid}))
        print(response.data)
        # print(response.status_code)
        # print(list(response.data['items'][0].items())[1][1])
        self.assertEqual(response.status_code,200)
        # self.assertIsInstance(response.data['items'], list)
        # self.assertEqual(response.data['items'][0]['title'], sample_post.title)