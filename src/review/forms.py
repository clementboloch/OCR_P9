
from django import forms
from .models import Ticket, Review, CustomUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image"
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire"
        }


class FollowForm(forms.Form):
    user = forms.CharField(label='User', max_length=100)
