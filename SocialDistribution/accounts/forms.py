from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': 'Cuddles',
            'maxlength': '16',
            'minlength': '6',
        })
        self.fields['email'].widget.attrs.update({
            'class':
            'form-control',
            'required':
            '',
            'name':
            'email',
            'id':
            'email',
            'type':
            'email',
            'placeholder':
            'cuddles69@mail.com',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'password',
            'maxlength': '22',
            'minlength': '3',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'required': '',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'placeholder': 'confirm password',
            'maxlength': '22',
            'minlength': '3',
        })

        username = forms.CharField(max_length=20, label=False)
        email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )