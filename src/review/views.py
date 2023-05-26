from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.db import IntegrityError
from . import models
from . import forms


# Login view
class Login(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "review/registration/login.html"


# Signup view
def signUp(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
    return render(request, 'review/registration/signup.html', {'form': form})


# Logout view
class Logout(LogoutView):
    pass


# Home view
@login_required(login_url='/review/login/')
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
    return render(request, 'review/home.html', context={'posts': posts, 'answerable': True})


# Follow view
@login_required(login_url='/review/login/')
def follow(request):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    error_message = ""
    if request.method == "POST":
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            my_follow = form.cleaned_data['user']
            try:
                my_follow = get_object_or_404(models.CustomUser, username=my_follow)
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


@login_required(login_url='/review/login/')
def unfollow(request, unfollowed_user):
    u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    unfollowed_user = get_object_or_404(models.CustomUser, id=unfollowed_user)
    models.UserFollow.objects.filter(user=u, followed_user=unfollowed_user).delete()
    return redirect('follow')


# Ticket creation view
@login_required(login_url='/review/login/')
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

    return render(request, "review/form.html", {"title": "Créer un ticket", "forms": [{'form': form}]})


# Review creation view
@login_required(login_url='/review/login/')
def review(request, ticket_id):
    # u = request.user
    u = models.CustomUser.objects.get(username='smithkaren')
    if request.method == "POST":
        ticketForm = {}
        reviewForm = {}
        for key, value in request.POST.items():
            if key in ['title', 'description', 'image']:
                ticketForm[key] = value
            elif key in ['headline', 'rating', 'body']:
                reviewForm[key] = value
        if ticketForm:
            ticketForm = forms.TicketForm(ticketForm)
            if ticketForm.is_valid():
                my_ticket = ticketForm.save(commit=False)
                my_ticket.user = u
                my_ticket.save()
            else:
                # TODO: add an error message somewhere
                return redirect('review', ticket_id)
        else:
            my_ticket = get_object_or_404(models.Ticket, id=ticket_id)
        reviewForm = forms.ReviewForm(reviewForm)
        if reviewForm.is_valid():
            my_review = reviewForm.save(commit=False)
            my_review.ticket = my_ticket
            my_review.user = u
            my_review.save()
        return redirect('home')

    else:
        if ticket_id != 0:
            ticket = get_object_or_404(models.Ticket, id=ticket_id)
            ticketForm = None
        else:
            ticket = None
            ticketForm = forms.TicketForm()
        reviewForm = forms.ReviewForm()
        return render(request, "review/form.html",
                      {"title": "Créer une critique",
                       "forms": [{'ticket': ticket, 'subtitle': 'Vous êtes en train de poster en réponse à'},
                                 {'form': ticketForm, 'subtitle': 'Livre / Article'},
                                 {'form': reviewForm, 'subtitle': 'Critique'}
                                 ]})


# Ticket modification view
@login_required(login_url='/review/login/')
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES or None, instance=ticket)
        if form.is_valid():
            my_ticket = form.save(commit=False)
            # u = request.user
            u = models.CustomUser.objects.get(username='smithkaren')
            my_ticket.user = u
            my_ticket.save()
        return redirect(posts)
    else:
        form = forms.TicketForm(instance=ticket)
        return render(request, "review/form.html",
                      {"title": "Modifier votre ticket",
                       "forms": [{'form': form}]
                       })


# Review modification view
@login_required(login_url='/review/login/')
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            my_review = form.save(commit=False)
            # u = request.user
            u = models.CustomUser.objects.get(username='smithkaren')
            my_review.user = u
            my_review.save()
        return redirect(posts)
    else:
        ticket = review.ticket
        form = forms.ReviewForm(instance=review)
        return render(request, "review/form.html",
                      {"title": "Modifier votre critique",
                       "forms": [{'ticket': ticket, 'subtitle': 'Vous êtes en train de poster en réponse à'},
                                 {'form': form, 'subtitle': 'Critique'}
                                 ]})


# Ticket deletion view
@login_required(login_url='/review/login/')
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket.delete()
    return redirect(posts)


# Review deletion view
@login_required(login_url='/review/login/')
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review.delete()
    return redirect(posts)


# My posts view
@login_required(login_url='/review/login/')
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
    return render(request, 'review/posts.html', context={'posts': posts, 'editable': True})
