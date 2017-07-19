from django.db.models.signals import post_save
from django.dispatch import receiver
from models import User, UserInfo


@receiver(post_save, sender=User)
def save_userinfo(sender, instance, created, **kwargs):
    if created:
        user_info = getattr(instance, 'info', None)
        info = UserInfo(user=instance, phone_no=user_info['phone_num'],
                        address=user_info['address'], date_of_birth=user_info['dob'],
                        gender=user_info['gender'], created_at=user_info['created_at']
                        )
        info.save()
