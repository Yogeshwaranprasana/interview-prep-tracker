from django.db import IntegrityError, OperationalError, ProgrammingError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register(request):
    error_message = None
    username = ''
    email = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
        except IntegrityError:
            error_message = 'That username is already taken. Choose a different one.'
        except (ProgrammingError, OperationalError):
            error_message = 'Database not ready. Please run migrations or contact the administrator.'

    return render(request, 'accounts/register.html', {
        'error_message': error_message,
        'username': username,
        'email': email,
    })

# def login_page(request):
#      return render(request, 'accounts/login.html')

def login_page(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = None
    username = ''
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            user = authenticate(
                request,
                username=username,
                password=password
            )
        except (ProgrammingError, OperationalError):
            error_message = 'Database not ready. Please run migrations or contact the administrator.'
            user = None

        if user is not None:
            login(request, user)
            return redirect(next_url or 'dashboard')

        if error_message is None:
            error_message = 'Invalid username or password. Please try again.'

    return render(request, 'accounts/login.html', {
        'error_message': error_message,
        'username': username,
        'next_url': next_url,
    })

def logout_page(request):

    logout(request)

    return redirect('/login/')  