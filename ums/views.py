from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'base.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('signin')
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist.')
            return redirect('register')

        if any(char.isdigit() for char in fname):
            messages.error(
                request, 'First name must not contain numeric values.')
            return redirect('register')

        if any(char.isdigit() for char in lname):
            messages.error(
                request, 'Last name must not contain numeric values.')
            return redirect('register')

        if len(username) > 12:
            messages.error(
                request, 'Username must be less than 10 characters.')
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already in use.')
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Password didn't match.")
            return redirect('register')

        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname

        user.save()

        # subject = 'Welcome to Technical Discussion Forum'
        # message = 'Hi, '+user.first_name+'!\n'+'Welcome to TDF family.'
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        login(request, user)
        return redirect('home')
    return render(request, 'auth/register.html')


def signout(request):
    logout(request)
    return redirect('home')
