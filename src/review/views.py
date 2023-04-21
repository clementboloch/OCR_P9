# from django.shortcuts import render
from django.http import HttpResponse


# 1. Login view
def login(request):
    return HttpResponse("Login")


# 2. Signup view
def signup(request):
    return HttpResponse("Signup")


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
