from datetime import datetime, date
from random import uniform, randint

from django.core.management import BaseCommand, call_command

from web.posts.models import Post, Request
from web.users.models import User, Address


class Command(BaseCommand):
    args = 'none'
    help = 'Adds 10 new users and some new posts and requests to each user'

    USERS_INFO = [{'first_name': 'Muhammad', 'last_name': 'Rehan', 'gender': 'male'},
                  {'first_name': 'Arooj', 'last_name': 'Hussain', 'gender': 'female'},
                  {'first_name': 'Talha', 'last_name': 'baber', 'gender': 'male'},
                  {'first_name': 'Verdan', 'last_name': 'Mahmood', 'gender': 'male'},
                  {'first_name': 'Erum', 'last_name': 'Naureen', 'gender': 'female'},
                  {'first_name': 'Muzammil', 'last_name': 'Hussain', 'gender': 'male'},
                  {'first_name': 'Asad', 'last_name': 'Riaz', 'gender': 'male'},
                  {'first_name': 'Rukhsar', 'last_name': 'Fiaz', 'gender': 'female'},
                  {'first_name': 'Rabbiya', 'last_name': 'Zaheer', 'gender': 'female'},
                  {'first_name': 'Mir', 'last_name': 'Waleed', 'gender': 'male'}]

    # noinspection PyMethodMayBeStatic
    def flush_eproperty_database(self):
        call_command('flush', interactive=False)

    # noinspection PyMethodMayBeStatic
    def create_user(self, user_id):

        email = "testuser+%d@eproperty.com" % user_id
        password = '123456789!'
        zip_code = '%d' % (randint(5000, 6000))
        street = '%d %s' % (randint(50, 150), chr(randint(65, 90)))

        if user_id in [1, 2]:
            city = "Lahore"
            state = "Punjab"
            route = "Allama Iqbal Town"
        elif user_id in [3, 5, 7]:
            city = "Islamabad"
            state = "Punjab"
            route = "Jinnah Super Market"
        else:
            city = "Karachi"
            state = "Sindh"
            route = "Clifton Bridge"

        address = Address(zip_code=zip_code, street=street, route=route,
                          city=city, state=state, country='Pakistan')
        address.save()
        user = User.objects.create_user(email=email, first_name=self.USERS_INFO[user_id-1].get('first_name'),
                                        last_name=self.USERS_INFO[user_id-1].get('last_name'), address=address,
                                        gender=self.USERS_INFO[user_id-1].get('gender'), born_on=date(1993, 4, 25),
                                        password=password)
        user.save()
        return user

    # noinspection PyMethodMayBeStatic
    def create_posts_of_user(self, user):

        max_posts = 2 if user.id in [1, 2] else 4

        if user.id != 4:
            for posts_count in range(0, max_posts):

                zip_code = '%d' % (randint(5000, 6000))
                street = '%d %s' % (randint(50, 150), chr(randint(65, 90)))

                if user.id in [3, 5, 7, 8, 9, 10]:
                    city = "Islamabad"
                    state = "Punjab"
                    route = "Faisal Mosque"
                    if posts_count == 1:
                        kind = Post.KindChoices.HOUSE
                    else:
                        kind = Post.KindChoices.PLOT
                else:
                    city = "Lahore"
                    state = "Punjab"
                    route = "Johar Town"
                    kind = Post.KindChoices.FLAT

                location = Address(zip_code=zip_code, street=street, route=route,
                                   city=city, state=state, country='Pakistan')
                location.save()
                Post(posted_by=user, title='I want to sell my house only serious buyers contact!',
                     area=round(uniform(100.000, 1000.000), 3), location=location,
                     description='its beautiful place to live in. %d bedrooms,yard,double story,%d bathrooms.'
                                 % (randint(1, 10), randint(1, 10)), kind=kind, contact_number='+923238447265',
                     demanded_price=50000.000, expired_on=date(2015, 8, 27)).save()

    # noinspection PyMethodMayBeStatic
    def create_requests_on_posts_by_other_users(self, user):

        if user.id in [2, 3, 4, 8, 9, 10]:
            posts_other_users = Post.objects.exclude(posted_by=user)
            for post_to_be_offered_on in posts_other_users:
                for requests_count in range(0, 3):
                    Request(requested_by=user, post=post_to_be_offered_on, price=round(uniform(30000.000, 50000.000), 3)
                            , message='would you please sell it to me ?').save()

    def handle(self, *args, **options):

        self.flush_eproperty_database()

        output = ' -Success ! \n Registered user\'s emails : \n'

        for user_id in range(1, 11):
            user = self.create_user(user_id=user_id)
            self.create_posts_of_user(user=user)
            self.create_requests_on_posts_by_other_users(user=user)
            output += ' %s \n' % user.email

        self.stdout.write(output)