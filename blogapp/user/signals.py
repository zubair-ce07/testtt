import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from blog.models import Blog
from comment.models import Comment
from user.models import UserProfile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def save_user_info(sender, instance, created, **kwargs):
    if not instance.is_staff and created:
        user_info = getattr(instance, 'info', None)
        user_profile = UserProfile(user=instance, phone_no=user_info['phone_num'], address=user_info['address'],
                                   date_of_birth=user_info['dob'], gender=user_info['gender'],
                                   created_at=user_info['created_at'])
        user_profile.info = user_info
        user_profile.save()


@receiver(post_save, sender=UserProfile)
def save_user_blog(sender, instance, created, **kwargs):
    if created:
        blog_info = getattr(instance, 'info', None)
        print(instance.user)
        blog = Blog(created_by=instance.user, slug=blog_info['blog_slug'],
                    text=blog_info['blog_text'], created_on=datetime.datetime.now().date(),
                    is_published=blog_info['blog_is_published'] == 'TRUE',
                    comments_allowed=blog_info['blog_comments_allowed'] == 'TRUE',
                    is_public=blog_info['blog_is_public'] == 'TRUE')
        blog.info = blog_info
        blog.save()


@receiver(post_save, sender=Blog)
def save_blog_comments(sender, instance, created, **kwargs):
    if created:
        comment_info = getattr(instance, 'info', None)
        comment = Comment(comment_for=instance, text=comment_info['comment_text'],
                          created_on=datetime.datetime.now(), created_by=instance.created_by,
                          user_ip=comment_info['ip'])
        comment.save()
