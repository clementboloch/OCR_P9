from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/review/login/'), name='root'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('home/', views.home, name='home'),
    path('follow/', views.follow, name='follow'),
    path('ticket/', views.ticket, name='ticket'),
    path('review/<int:ticket_id>/', views.review, name='review'),
    path('posts/', views.posts, name='my_posts'),
    path('unfollow/<int:unfollowed_user>/', views.unfollow, name='unfollow'),
]
