from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, CharField, Value


class CustomUser(AbstractUser):
    def get_followed_users(self):
        return CustomUser.objects.filter(followed_by__user=self)

    def get_following_users(self):
        return CustomUser.objects.filter(following__followed_user=self)

    def get_viewable_tickets(self):
        return Ticket.objects.filter(
            Q(user=self) | Q(user__in=self.get_followed_users())
        ).annotate(content_type=Value('TICKET', CharField()))

    def get_my_tickets(self):
        return Ticket.objects.filter(user=self).annotate(content_type=Value('TICKET', CharField()))

    def get_viewable_reviews(self):
        return Review.objects.filter(
            Q(user=self) | Q(user__in=self.get_followed_users()) | Q(ticket__user=self)
        ).annotate(content_type=Value('REVIEW', CharField()))

    def get_my_reviews(self):
        return Review.objects.filter(user=self).annotate(content_type=Value('REVIEW', CharField()))


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollow(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
