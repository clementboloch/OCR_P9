from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from django.db import IntegrityError
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
    error_message = ""
    if request.method == "POST":
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            my_follow = form.cleaned_data['user']
            try:
                my_follow = models.CustomUser.objects.get(username=my_follow)
            except models.CustomUser.DoesNotExist:
                my_follow = None
            if my_follow is not None:
                new_follow = models.UserFollow(user=u, followed_user=my_follow)
                try:
                    new_follow.save()
                except IntegrityError:
                    error_message = "You are already following this user"
            else:
                error_message = "User does not exist"
    form = forms.FollowForm()
    followed = list(u.get_followed_users().values())
    following = list(u.get_following_users().values())
    follow = {'error_message': error_message, 'form': form, 'followed': followed, 'following': following}
    return render(request, 'review/follow.html', context=follow)


def unfollow(request, unfollowed_user):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    unfollowed_user = models.CustomUser.objects.get(id=unfollowed_user)
    models.UserFollow.objects.filter(user=u, followed_user=unfollowed_user).delete()
    return redirect('follow')


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
def review(request, ticket_id):
    if request.method == "POST":
        ticketForm = {}
        reviewForm = {}
        for key, value in request.POST.items():
            if key in ['title', 'description', 'image']:
                ticketForm[key] = value
            elif key in ['headline', 'rating', 'body']:
                reviewForm[key] = value
        ticketForm = forms.TicketForm(ticketForm)
        reviewForm = forms.ReviewForm(reviewForm)
        if ticketForm.is_valid() and reviewForm.is_valid():
            my_ticket = ticketForm.save(commit=False)
            # u = request.user
            u = models.CustomUser.objects.get(username='smithkaren')
            my_ticket.user = u
            my_ticket.save()
            my_review = reviewForm.save(commit=False)
            my_review.ticket = my_ticket
            my_review.user = u
            my_review.save()
        return redirect('home')

    else:
        if ticket_id != 0:
            ticket = models.Ticket.objects.get(id=ticket_id)
            ticketForm = None
        else:
            ticket = None
            ticketForm = forms.TicketForm()
        reviewForm = forms.ReviewForm()
        return render(request, "review/review.html",
                      {"ticket": ticket, "ticketForm": ticketForm, "reviewForm": reviewForm})


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
