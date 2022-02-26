from django import forms
from .models import Post, Comment, Author

# Reference: https://www.youtube.com/watch?v=USVjTtApVDM&list=PLPSM8rIid1a3TkwEmHyDALNuHhqiUiU5A&index=2
class PostForm(forms.ModelForm):
    title = forms.CharField(label='title', 
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your title here...',
            'rows':1,
            'style': 'width: 85%;'
        })
    )
    description = forms.CharField(label='description', 
        widget=forms.Textarea(attrs={
            'placeholder': 'Type something...',
            # 'rows':5,
            # 'columns':50,
            'style': 'height: 30%; width: 85%;'
        })
    )

    class Meta:
        model = Post
        fields = ['title','description','visibility']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='comment', 
        widget=forms.Textarea(attrs={
            'placeholder': 'Type in your comment here...',
            # 'rows':5,
            # 'columns':50,
            'rows':1,
            'style': 'width: 85%;'
        })
    )

    class Meta:
        model = Comment
        fields = ['comment']

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         field = ('id', 'host', 'displayname', 'github', 'profileImage')