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
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
