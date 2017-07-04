from .models import UserProfile, Trainer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    import pdb; pdb.set_trace()
    if created:
        user = UserProfile.objects.create(user=instance,
                                          name=instance.first_name,
                                          picture=instance.picture)
        Trainer.objects.create(user=instance)
