from django.test import Client, TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from authors.models import Author
from inboxes.models import Inbox, InboxItem
from posts.models import *
from authors.serializers import *
from posts.serializers import *
import json
from SocialDistribution import urls
from requests.auth import HTTPBasicAuth


class TestInboxAPIViews(APITestCase):

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

    def test_InboxAPIView_GET(self):
        author = Author.objects.get(username='johnny')
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        InboxItem.objects.create(
            inbox=Inbox.objects.filter(
                author__username=author.username).first(),
            inbox_item_type='post',
            item=sample_post,
        )
        
        response = self.client.get(reverse('service-Inbox', kwargs={'author':author.uuid}))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.data['items'], list)
        self.assertEqual(response.data['items'][0]['title'], sample_post.title)
    
    def test_InboxAPIView_POST(self):
        author = Author.objects.get(username='johnny')
        # Test posting a post
        sample_post = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        sample_post.id = f"{author.host}authors/{str(sample_post.author.uuid)}/posts/{str(sample_post.uuid)}"
        sample_post.save()
        serializer = PostSerializer(sample_post)
        headerInfo = {'Content-Type': 'application/json' }
        response = self.client.post(reverse('service-Inbox', kwargs={'author':author.uuid}), headers=headerInfo, auth=HTTPBasicAuth("admin", "admin"), data=serializer.data, format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['title'], sample_post.title)

        # Test posting a comment
        sample_comment = Comment(comment="This is a new comment", contentType="text/plain", author=author, post=sample_post)
        sample_comment.id = f"{author.host}authors/{str(sample_comment.author.uuid)}/posts/{str(sample_comment.post.uuid)}/comments/{str(sample_comment.uuid)}"
        sample_comment.save()
        serializer = CommentsSerializer(sample_comment)
        headerInfo = {'Content-Type': 'application/json' }
        response = self.client.post(reverse('service-Inbox', kwargs={'author':author.uuid}), headers=headerInfo, auth=HTTPBasicAuth("admin", "admin"), data=serializer.data, format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['comment'], sample_comment.comment)

        # # Test posting a like
        # sample_like = Like(author=author, object=sample_post.id)
        # sample_like.save()
        # serializer = LikesSerializer(sample_like)
        # headerInfo = {'Content-Type': 'application/json' }
        # response = self.client.post(reverse('service-Inbox', kwargs={'author':author.uuid}), headers=headerInfo, auth=HTTPBasicAuth("admin", "admin"), data=serializer.data, format='json')
        # # print("response data: ", response.data)
        # self.assertEqual(response.status_code,200)
