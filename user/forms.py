from django import forms
from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label="Username",
                             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Please input username'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Please input password'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise  forms.ValidationError('Username or Password wrong!!')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class Regform(forms.Form):
    username = forms.CharField(label="Username",
                               max_length = 30,
                               min_length = 3,
                               widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please input username'}))
    email =forms.EmailField(label="Email",
                               widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please input email'}))
    password = forms.CharField(label="Password",
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please input password'}))
    password_again = forms.CharField(label="Password again",
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please input password again'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Username exists')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again= self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('passwords not consistent')
        return password_again


class ChangeNicknameform(forms.Form):
    nickname_new = forms.CharField(
        label="New Nickname",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Please input new nickname'}
        )
    )

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameform,self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('Not login')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise forms.ValidationError('New nickname can not be empty')
        return nickname_new


class BindEmailform(forms.Form):
    email = forms.EmailField(
        label = 'email',
        widget = forms.EmailInput(
            attrs={'class': 'form-control', 'palceholder': 'Please input correct email'}
        )
    )
    verifications_code = forms.CharField(
        label='validation code',
        required = False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'palceholder': 'Click send validation code to email'}
        )
    )

    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailform,self).__init__(*args,**kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('Not login')

        if self.request.user.email != '':
            raise forms.ValidationError('You has binded a email')

        code = self.request.session.get('bind_email_code','')
        verification_code = self.cleaned_data.get('verification_code','')
        if not (code != '' and code != verification_code):
            raise forms.ValidationError('verfication code not correct')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email has binded')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == "":
            raise ValidationError('Verification code can not be empty')
        return verification_code
