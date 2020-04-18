from django.shortcuts import render
from base64 import b64encode
from .models import Users
from django.db.models import Q
from django.core.files.storage import default_storage
from project import settings
import os
from datetime import datetime


def login(request):
    if request.method == 'POST':
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        hashed_pwd = b64encode(password.encode('utf-8'))
        users = Users.objects.filter(email=email, password=hashed_pwd)
        if len(users) <= 0:
            return render(request, 'user_management/login.html', {'context': {'message': 'Invalid Email or Password.'}})
        request.session['user_id'] = users[0].pk
        return dashboard(request)
    if 'user_id' in request.session:
        return dashboard(request)
    return render(request, 'user_management/login.html', {})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('inputEmail')
        phone = request.POST.get('phone')
        password = request.POST.get('inputPassword')
        cpassword = request.POST.get('confirmPassword')
        print(request.FILES)
        message = ''
        if password != cpassword:
            message = 'Password and Confirm Password not matched.'
        elif len(phone) != 10:
            message = 'Enter valid Phone.'
        if message == '':
            users = Users.objects.filter(Q(email=email) | Q(phone=phone))
            if len(users) > 0:
                message = "Email or Phone already registered."
        if message != '':
            context = {'context': {'fname': first_name, 'lname': last_name, 'email': email, 'phone': phone,
                                   'message': message}}
            return render(request, 'user_management/signup.html', context)

        hashed_pwd = b64encode(password.encode('utf-8'))
        new_user = Users(first_name=first_name, last_name=last_name, email=email, phone=phone, password=hashed_pwd,
                         image='')
        new_user.save()
        if len(request.FILES) > 0:
            image = request.FILES.get('image')
            default_storage.save(image.name, image)
            init_url = settings.BASE_DIR + default_storage.url(image.name)
            new_file_name = '/media/profile_images/' + str(new_user.pk) + "_" + str(datetime.now()) + "_" + str(image.name)
            new_url = settings.BASE_DIR + new_file_name
            os.rename(init_url, new_url)
            new_user.image = new_file_name
            new_user.save()
        message = 'You Registered Successfully.'
        return render(request, 'user_management/login.html', {'context': {'message': message}})
    context = {}
    return render(request, 'user_management/signup.html', context)


def dashboard(request):
    if 'user_id' not in request.session:
        return render(request, 'user_management/login.html', {})
    print(request.session['user_id'])
    user = Users.objects.get(pk=request.session['user_id'])
    user_context = dict()
    user_context['email'] = user.email
    user_context['fname'] = user.first_name
    user_context['lname'] = user.last_name
    user_context['image'] = user.image
    user_context['phone'] = user.phone
    context = {'context': {'user': user_context}}
    return render(request, 'user_management/dashboard.html', context)


def logout(request):
    try:
        del request.session['user_id']
    except Exception as e:
        pass
    return render(request, 'user_management/login.html', {})
