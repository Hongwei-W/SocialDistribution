from django.test import TestCase, Client
from django.urls import reverse
import json
from posts.models import Post, Comment
from authors.models import Author, FollowerCount

from django.contrib.auth.models import User
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

    def test_post_list_GET(self):

        response = self.c.get(self.url_feed)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "feed.html")

    def test_new_post_GET(self):

        response = self.c.get(self.url_newPost)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "newpost.html")
    
    def test_new_post_POST(self):
        # currAuthor = Author.objects.filter(id="johnny")[0]
        # newPost = Post(title='testpost', description="This is a new post", contentType="text", author=currAuthor, categories="test")

        response = self.c.post(self.url_newPost,{
            'title':'testpost', 
            'description':"This is a new post", 
            'contentType':"text/plain",
            'content':"testpost", 
            'unparsedCategories':"test", 
            'visibility': "PUBLIC",
            'unlisted': False,
            'postImage':'',
        })

        self.assertEquals(response.status_code, 302)
        author = Author.objects.get(username='johnny')
        newPost = Post.objects.get(author=author)
        self.assertEquals(newPost.description, "This is a new post")
        self.assertEquals(newPost.title, "testpost")
    
    def test_post_detail_GET(self):
        author = Author.objects.get(username='johnny')
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        newPost.id = f"{author.host}authors/{str(newPost.author.uuid)}/posts/{str(newPost.uuid)}"
        newPost.save()
        response = self.c.get(reverse('posts:postDetail', kwargs={'pk':newPost.uuid}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "postDetail.html")
    
    def test_post_detail_POST(self):
        author = Author.objects.get(username='johnny')
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        newPost.id = f"{author.host}authors/{str(newPost.author.uuid)}/posts/{str(newPost.uuid)}"
        newPost.save()

        # Posting a comment
        response = self.c.post(reverse('posts:postDetail', kwargs={'pk':newPost.uuid}),{
            'comment': 'Test comment',
            'contentType': 'text/plain',
        })
        self.assertEquals(response.status_code, 200)
        author = Author.objects.get(username='johnny')
        newComment = Comment.objects.get(author=author)
        self.assertEquals(newComment.comment, "Test comment")
    
    def test_post_edit(self):
        author = Author.objects.get(username='johnny')
        newPost = Post(title='testpost', description="description", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        newPost.id = f"{author.host}authors/{str(newPost.author.uuid)}/posts/{str(newPost.uuid)}"
        newPost.save()
        
        response = self.c.post(reverse('posts:postEdit', kwargs={'pk':newPost.uuid}),{
            'title': 'title edited',
            'content':'content edited',
            'contentType':'text/markdown',
        })

        editPost = Post.objects.get(author__username='johnny')
        self.assertEquals(editPost.title, "title edited")
        self.assertEquals(editPost.content, "content edited")
    
    def test_post_delete(self):
        author = Author.objects.get(username='johnny')
        newPost = Post(title='testpost', description="description", content="testpost", contentType="text/plain", unparsedCategories="test", author=author)
        newPost.id = f"{author.host}authors/{str(newPost.author.uuid)}/posts/{str(newPost.uuid)}"
        newPost.save()
        
        response = self.c.post(reverse('posts:postDelete', kwargs={'pk':newPost.uuid}),{
        })

        deletedPost = Post.objects.filter(author__username='johnny')
        self.assertEquals(deletedPost.count(), 0)






