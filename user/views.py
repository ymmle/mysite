import string
import random
import time
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import LoginForm, Regform, ChangeNicknameform, BindEmailform
from .models import Profile


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'user/login.html',context)


def register(request):
    if request.method == 'POST':
        reg_form = Regform(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            user = settings.AUTH_USER_MODEL.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('form',reverse('home')))
    else:
        reg_form = Regform()

    context ={}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context={}
    return render(request,'user/user_info.html',context)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameform(request.POST,user = request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameform()

    context = {}
    context['page_title'] = 'Edit nickname'
    context['form_title'] = 'Edit nickname'
    context['submit_text'] = 'Edit'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request,'form.html',context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailform(request.POST, user = request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailform()

    context = {}
    context['page_title'] = 'Binding email'
    context['form_title'] = 'Binding email'
    context['submit_text'] = 'Bind'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request,'user/bind_email.html',context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != "":
        code = ''.join(random.sample(string.ascii_letters+string.digits,4))
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now - send_code_time <30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

            send_mail(
                      'bind mail',
                      'validate code:%s' %code,
                      '547179342@qq.com',
                      [email],
                      fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)