from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Create your views here.


def login_view(request, *args, **kwargs):
    form= AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        userprofile= form.get_user()
        login(request, userprofile)
        return redirect("/")
    context= {
        "form":form,
        "btn_label":"login",
        "title":"login"
    }
    return render(request, "account/auth.html", context)

def logout_view(request, *args, **kwargs):
    if request.method== "POST":
        logout(request)
        return redirect("/login")
    context= {
        "form":None,
        "description": "Are you sure to logout?",
        "btn_label":"Click Here To Confirm",
        "title":"logout"
    }
    return render(request, "account/auth.html", context)

def signup_view(request, *args, **kwargs):
    form= UserCreationForm(request.POST or None)
    if form.is_valid():
        user= form.save(commit=True)
        login(request, user)
        user.set_password(form.cleaned_data.get("password1"))
        return redirect("/")
    context= {
        "form":form,
        "btn_label":"Signup",
        "title":"Signup"
    }
    return render(request, "account/auth.html", context)
