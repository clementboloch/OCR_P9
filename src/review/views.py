from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms


# 1. Login view
class Login(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "review/registration/login.html"


# 2. Signup view
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "review/registration/signup.html"


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
    return render(request, 'review/home.html', context={'posts': posts})


# 4. Follow view
def follow(request):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    followed = list(u.get_followed_users().values())
    following = list(u.get_following_users().values())
    follow = {'followed': followed, 'following': following}
    return render(request, 'review/follow.html', context=follow)


# 5. Ticket creation view
def ticket(request):
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES or None)
        if form.is_valid():
            my_ticket = form.save(commit=False)
            # u = request.user
            u = models.CustomUser.objects.get(username='smithkaren')
            my_ticket.user = u
            my_ticket.save()
            return redirect('home')

    else:
        form = forms.TicketForm()

    return render(request, "review/ticket.html", {"form": form})


# 6. Review creation view
def review(request):
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            my_review = form.save(commit=False)
            # u = request.user
            u = models.CustomUser.objects.get(username='smithkaren')
            my_review.user = u
            my_review.save()
            return redirect('home')

    else:
        form = forms.ReviewForm()

    return render(request, "review/review.html", {"form": form})


# 7. My posts view
def posts(request):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    tickets = u.get_my_tickets()
    reviews = u.get_my_reviews()
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'review/posts.html', context={'posts': posts})
