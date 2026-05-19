from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/login/')

    return render(request, 'accounts/register.html')

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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            return redirect(next_url or 'dashboard')

        error_message = 'Invalid username or password. Please try again.'

    return render(request, 'accounts/login.html', {
        'error_message': error_message,
        'username': username,
        'next_url': next_url,
    })

def logout_page(request):

    logout(request)

    return redirect('/login/')  