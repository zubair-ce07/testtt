from django.db import models
from django.contrib.auth.models import User

from users.models import Cart


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', null=True, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, null=True, related_name='payment')
    time_of_transaction = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}_{self.id}"
