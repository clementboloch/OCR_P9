# from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# 1. Login view
def login(request):
    return HttpResponse("Login")


# 2. Signup view
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# 3. Home view
def home(request):
    return HttpResponse("Home")


# 4. Follow view
def follow(request):
    return HttpResponse("Follow")


# 5. Ticket creation view
def ticket(request):
    return HttpResponse("Ticket creation")


# 6. Review creation view
def review(request):
    return HttpResponse("Review creation")


# 7. My posts view
def posts(request):
    return HttpResponse("My posts")
