from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Email Required")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def get_logged_in_user(self, email=None, username=None):
        pass


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.first_name


class Category(models.Model):
    category_name = models.CharField(max_length=15)

    def __str__(self):
        return self.category_name


class Movie(models.Model):
    movie_id = models.CharField(max_length=12, unique=True)
    category = models.ManyToManyField(Category, related_name='Movie')
    title = models.CharField(max_length=75)
    date_of_release = models.DateField(max_length=12)
    poster = models.URLField(max_length=400, null=True)
    content_rating = models.CharField(max_length=7)
    plot = models.TextField()

    def __str__(self):
        return self.title


class Website(models.Model):
    url = models.URLField(max_length=100, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    website_base_url = models.ForeignKey(Website, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    website_url = models.URLField(max_length=200)

    def __str__(self):
        return self.movie.title


class UserRating(models.Model):
    user = models.ManyToManyField(User)
    movie = models.ManyToManyField(Movie)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.rating)


class Favorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    movies = models.ManyToManyField(Movie)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Creates Token for each new user created"""
    if created:
        Token.objects.create(user=instance)
