from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):

    blog_text = models.CharField(max_length=100000)
    blog_date = models.DateTimeField('date of blog')
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=200)
    status = models.IntegerField(choices=((1, ("Public")),
                                          (2, ("Private"))),
                                 default=1)
    #user = models.OneToOneField(User)



