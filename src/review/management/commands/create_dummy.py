from django.core.management.base import BaseCommand
from review.models import CustomUser, Ticket, Review, UserFollow
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake data (user accounts, tickets, reviews, follows)'

    def handle(self, *args, **options):
        fake = Faker()

        # create fake user
        for i in range(10):
            username = fake.user_name()
            password = fake.password()

            # create user if doesn't exist
            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create(username=username, password=password)

        # create fake tickets
        for i in range(10):
            title = fake.sentence(nb_words=6, variable_nb_words=True)
            description = fake.text(max_nb_chars=2048)
            user = CustomUser.objects.order_by('?').first()

            Ticket.objects.create(title=title, description=description, user=user)

        # create fake reviews
        for i in range(10):
            if i % 5 == 0:
                ticket = None
            else:
                ticket = Ticket.objects.order_by('?').first()
            rating = fake.random_int(min=0, max=5)
            headline = fake.sentence(nb_words=3, variable_nb_words=True)
            body = fake.text(max_nb_chars=8192)
            user = CustomUser.objects.order_by('?').first()

            Review.objects.create(ticket=ticket, rating=rating, headline=headline, body=body, user=user)

        # create fake follows
        for i in range(10):
            user = CustomUser.objects.order_by('?').first()
            followed_user = CustomUser.objects.order_by('?').first()
            same = user == followed_user
            while same:
                followed_user = CustomUser.objects.order_by('?').first()
                same = user == followed_user

            # create user follow if doesn't exist
            if not UserFollow.objects.filter(user=user, followed_user=followed_user).exists():
                UserFollow.objects.create(user=user, followed_user=followed_user)

        self.stdout.write(self.style.SUCCESS('Successfully created data (user accounts, tickets, reviews, follows).'))
