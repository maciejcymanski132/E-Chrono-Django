from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext


def signup(request):
    return render(request, 'accounts/signup.html')


def user_page(request, id):
    if request.user.is_authenticated:
        return render(request, 'accounts/userpage.html', {"user": User.objects.filter(id=id).first()})
    return render(request, 'home.html')


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html', {'form': AuthenticationForm()})


def handle404(request, exception):
    return redirect('404')
