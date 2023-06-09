from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/review/login/'), name='root'),
    path('login/', views.Login.as_view(redirect_authenticated_user=True), name='login'),
    path('signup/', views.signUp, name='signup'),
    path('logout/', views.Logout.as_view(), name='logout'),
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
