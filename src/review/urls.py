from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/review/login/'), name='root'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('follow/', views.follow, name='follow'),
    path('ticket/', views.ticket, name='ticket'),
    path('review/', views.review, name='review'),
    path('posts/', views.posts, name='my_posts'),
]
