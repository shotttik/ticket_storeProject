from django.shortcuts import render, redirect
from django.contrib import auth
from user.models import User


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email=request.POST['email'])
                return render(request, 'pages/signup.html', {'error': 'Email already registered'})
            except User.DoesNotExist:
                user = User.objects.create_user(email=request.POST['email'], password=request.POST['password1'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.mobile_phone = request.POST['mobile_phone']
                user.save()
                return redirect('login')
    else:
        return render(request, 'pages/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'], password=request.POST['password'], )
        if user is not None:
            auth.login(request, user)
            # @TODO redirect to homepage
            return redirect('login')
        else:
            return render(request, 'pages/login.html', {'error': 'Email or password is incorrect'})
    return render(request, 'pages/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')
