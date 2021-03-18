from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import LoginForm, SignupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You have been already logged in")
        return redirect('/')

    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email = email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been sucessfully logged in')
                return redirect('/')
            else:
                messages.warning(request, 'Incorrect credientials')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

def LogoutView(request):
    logout(request)
    messages.success(request, "You have been sucessfully logged out")
    return redirect('/')

def SignupView(request):
    form = SignupForm()
    if request.method=='POST':  
        form = SignupForm(request.POST)
        print(f'form {form}')
        if form.is_valid():
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            phonenumber = form.cleaned_data.get('phonenumber')
            password = form.cleaned_data.get('password1')
            UserModel.objects.create_user(email,phonenumber, password, name)
            messages.success(request, "You can login now")
            return redirect('/login/')
        else:
            messages.danger(request, "The credintails you have provided is not valid")
    return render(request, 'signup.html',{'form':form})            



