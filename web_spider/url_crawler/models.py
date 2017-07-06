from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from url_crawler.utils import URLSpider


class WebPage(models.Model):
    """
    Model class to store address of web page and meta data about web page
    """
    url = models.URLField()
    # size of the page in bytes
    size_of_page = models.PositiveIntegerField()
    tags_count = models.PositiveIntegerField()
    meta_tags_count = models.PositiveIntegerField()
    links_count = models.PositiveIntegerField()

    def __str__(self):
        return self.url

    @classmethod
    def get_or_create(cls, url):
        """
        Checks if url is already visited and data is in database
        if not visits url and saves to database and returns the result

        Arguments:
            url (str): url against which to search
        Returns:
            page (WebPage()): content of the web page at given url

        Raises:
            TypeError: if response in not text or status is not OK
            ConnectionError: if connection to URL can not be made
        """
        page_set = cls.objects.filter(url=url)

        # not found in the database
        if not page_set.exists():
            spider = URLSpider(url)

            try:
                results = spider.crawl()
            except (TypeError, ConnectionError):
                raise

            page = cls.objects.create(
                url=url,
                size_of_page=results['size'],
                tags_count=results['tags_count'],
                meta_tags_count=results['meta_tags'],
                links_count=len(results['links'])
            )

            # storing all links on the page to database
            Link.objects.bulk_create(
                [Link(url=link_url, web_page=page) for link_url in results['links']]
            )

        # found in database
        else:
            # saving first in queryset
            page = page_set.first()

        return page


class Link(models.Model):
    """
    Model class to store urls found on a web page
    """
    web_page = models.ForeignKey(WebPage, on_delete=models.CASCADE)
    # address in href attribute in links on page
    url = models.URLField(max_length=500)


class CustomUserManager(BaseUserManager):
    """
    Provides a manager to create user objects and super user
    """
    def create_user(self, email, password, date_of_birth=None, first_name=None, last_name=None):
        """
        Save user object created with given parameters to database and returns user

        Arguments:
            email (str): email address
            password (str): password to be set
            date_of_birth (Date): date of birth
            first_name (str): first name of user
            last_name (str): last name of user
        Returns:
             user (CustomUser): user created with given attributes
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates user as admin for staff privileges

        Arguments:
            email (str): email address
            password (str): password to be set
        Returns:
            user (CustomUser): user created with given attributes
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    Custom User model class to store users
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.last_name

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
