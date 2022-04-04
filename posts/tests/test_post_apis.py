from django.test import Client, TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from authors.models import Author
from authors.serializers import *
from posts.models import *
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

    def test_PostsAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        response = self.client.get(reverse('service-posts', kwargs={'author':author.uuid}))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.data['items'], list)
        self.assertEqual(response.data['items'][0]['title'], sample_post.title)
    
    def test_PostAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        # sample_post = {'title': 'test_post', 'content': 'test_content', 'description': 'test_description', 'content_type': 'text/plain', 'author': 'johnny'}
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        response = self.client.get(reverse('service-post', kwargs={'pk':sample_post.uuid, 'author':author.uuid}), auth=HTTPBasicAuth("admin", "admin"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['title'], sample_post.title)
    
    def test_CommentsAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        # sample_post = {'title': 'test_post', 'content': 'test_content', 'description': 'test_description', 'content_type': 'text/plain', 'author': 'johnny'}
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        sample_comment = Comment(comment="This is a new comment", contentType="text/plain", author=author, post=sample_post)
        sample_comment.id = f"{author.host}authors/{str(sample_comment.author.uuid)}/posts/{str(sample_comment.post.uuid)}/comments/{str(sample_comment.uuid)}"
        sample_comment.save()
        response = self.client.get(reverse('service-comments', kwargs={'post':sample_post.uuid, 'author':author.uuid}), auth=HTTPBasicAuth("admin", "admin"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['items'][0]['comment'], sample_comment.comment)
    
    def test_CommentsAPIView_POST(self):
        author = Author.objects.get(username='johnny')
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        # sample_post = {'title': 'test_post', 'content': 'test_content', 'description': 'test_description', 'content_type': 'text/plain', 'author': 'johnny'}
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        response = self.client.post(reverse('service-comments', kwargs={'post':sample_post.uuid, 'author':author.uuid}), auth=HTTPBasicAuth("admin", "admin"), data={"comment":"This is a new comment", "contentType":"text/plain", "author":author.uuid, "object":sample_post.id})
        self.assertEqual(response.status_code,200)