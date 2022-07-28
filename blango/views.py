from django.shortcuts import render
from django.shortcuts import render,redirect #render - built in templater
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html')