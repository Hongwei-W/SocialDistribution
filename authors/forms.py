from django import forms

from authors.models import Author
class UpdateProfileForm(forms.ModelForm):
    github = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    profileImage = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))

    class Meta:
        model = Author
        fields = ['github', 'profileImage']