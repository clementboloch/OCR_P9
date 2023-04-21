from itertools import chain

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from . import models


# 1. Login view
class Login(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "registration/login.html"


# 2. Signup view
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# 3. Home view
def home(request):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    tickets = u.get_viewable_tickets()
    reviews = u.get_viewable_reviews()
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'home.html', context={'posts': posts})


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
