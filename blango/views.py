from django.shortcuts import render
from django.shortcuts import render,redirect #render - built in templater
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html')

'''
def registerpage(request): #check if its unique user and register
    if request.method == 'GET':
        return render(request, template_name='register.html')
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #basically built-in model "User"
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'User logged in!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('register')


def loginpage(request):
    if request.method == "GET":
        return render(request, template_name='login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are logged in as {user.username}')
            return redirect('index')
        else:
            messages.error(request, 'The combination of the user name and the password is wrong!')
            return redirect('login')


def logoutpage(request):
    logout(request)
    messages.success(request, f'You have been logged out!')
    return redirect('index')

'''