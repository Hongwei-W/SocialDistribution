from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    # ex: /polls/
    path('newpost/', views.NewPostView.as_view(), name='newpost'),
    path('post/<uuid:pk>',views.PostDetailView.as_view(), name='postDetail'),
    path('post/edit/<uuid:pk>',views.PostEditView.as_view(), name='postEdit'),
    path('post/delete/<uuid:pk>',views.PostDeleteView.as_view(), name='postDelete'),
    path('like', views.like, name='like'),
    path('liked/<uuid:post_id>', views.liked, name='liked'),
    path('post/<uuid:pk>/share', views.SharedPostView.as_view(), name='sharePost'),
    path('post/shared/<uuid:pk>',views.ShareDetailView.as_view(), name='shareDetail'),
]