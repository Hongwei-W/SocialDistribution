from django.test import TestCase, Client
from django.urls import reverse
import json
from posts.models import Post, Comment
from authors.models import Author, FollowerCount

from django.contrib.auth.models import User


class TestViews (TestCase):

    def setUp(self):
        self.c = Client()

        self.url_feed = reverse('myapp:postList')
        self.url_newPost = reverse('myapp:newpost')
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
        

        url_signup = '/accounts/signup/'
        self.c.post(url_signup, self.user_info)
        logged_in = self.c.login(username='johnny', password='qwonvwet23')

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
            'contentType':"md", 
            'categories':"test", 
            'visibility': "PUBLIC",
            'postImage':'',
        })

        self.assertEquals(response.status_code, 302)
        author = Author.objects.get(id='johnny')
        newPost = Post.objects.get(title='testpost')
        self.assertEquals(newPost.description, "This is a new post")
    
    def test_post_detail_GET(self):
        author = Author.objects.get(id='johnny')
        newPost = Post(title='testpost', description="This is a new post", contentType="text", categories="test", author=author)
        newPost.save()
        response = self.c.get(reverse('myapp:postDetail', kwargs={'pk':newPost.id}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "postDetail.html")
    
    def test_post_detail_POST(self):
        author = Author.objects.get(id='johnny')
        newPost = Post(title='testpost', description="This is a new post", contentType="text", categories="test", author=author)
        newPost.save()

        # Posting a comment
        response = self.c.post(reverse('myapp:postDetail', kwargs={'pk':newPost.id}),{
            'comment': 'Test comment'
        })

        # author = Author.objects.get(id='johnny')
        newComment = Comment.objects.get(author__id='johnny')
        self.assertEquals(newComment.comment, "Test comment")
    
    def test_post_edit(self):
        author = Author.objects.get(id='johnny')
        newPost = Post(title='testpost', description="description", contentType="text", categories="test", author=author)
        newPost.save()
        
        response = self.c.post(reverse('myapp:postEdit', kwargs={'pk':newPost.id}),{
            'title': 'title edited',
            'description':'description edited',
            'visibility': "PUBLIC",
        })

        editPost = Post.objects.get(author__id='johnny')
        self.assertEquals(editPost.title, "title edited")
        self.assertEquals(editPost.description, "description edited")
    
    def test_post_delete(self):
        author = Author.objects.get(id='johnny')
        newPost = Post(title='testpost', description="description", contentType="text", categories="test", author=author)
        newPost.save()
        
        response = self.c.post(reverse('myapp:postDelete', kwargs={'pk':newPost.id}),{
        })

        deletedPost = Post.objects.filter(author__id='johnny')
        self.assertEquals(deletedPost.count(), 0)

    def test_profile_GET(self):
        response = self.c.get(reverse('myapp:profile', kwargs={'user_id':'johnny'}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "profile.html")
        





