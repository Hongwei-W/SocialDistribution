from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from .forms import PostForm

# Create your views here.
def login(request):
    return HttpResponse("You're looking at login page.")
    # render(request, 'myapp/login.html')
def signup(request):
    return HttpResponse("You're looking at signup page.")
    # render(request, 'myapp/signup.html')
# def feed(request):
#     # return HttpResponse("You're looking at feed page.")
#     return render(request, 'myapp/feed.html')

# def newpost(request):
#     return render(request, 'myapp/newpost.html')

class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        # form = PostForm()
        context = {
            'postList': posts,
            # 'form': form,
        }
        return render(request,'myapp/feed.html', context)

class NewPostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request,'myapp/newpost.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm(request.POST)

        if form.is_valid():
            newPost = form.save(commit=False)
            # newPost.author = request.user.username
            newPost.save()
        
        # posts = Post.objects.all()
        # context = {
        #     'postList': posts,
        #     # 'form': form,
        # }
        # return render(request,'myapp/newpost.html', context)
        return redirect('myapp:postList')
