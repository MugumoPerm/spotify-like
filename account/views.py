from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.utils import timezone
import datetime
from django.contrib import messages
# Create your views here.
from .forms import CreateUserForm

def login_user(request ):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("songs")
        else:
            messages.error(request, "Invalid Username or password")

    return render(request, template_name="login.html")


def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("username")
            messages.success(request, "account for "+ name + " was created succesfully")
            return redirect('login')
    else:
        form = CreateUserForm()
    
    
    return render(request,"register.html", {
        "form":form,
    })

def home(request):
    return render(request, template_name="index.html")
@login_required(login_url='login')
def songs(request):
    time = datetime.datetime.now()
    ctime = time.hour
    ntime = ""
    if ctime < 11:
        ntime = "good morning"
    elif ctime < 17:
        ntime = "afternoon"
    else:
        ntime = "evening"
    return render(request,"songs.html",{
        "time": ntime
    })

def logout_user(request):
    logout(request)
    return redirect("login")