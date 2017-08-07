import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from wblog.models import Blog, Comment, User, UserProfile


@receiver(post_save, sender=User)
def save_userinfo(sender, instance, created, **kwargs):
    if not instance.is_staff and created:
        user_info = getattr(instance, 'info', None)
        UserProfile(user=instance, phone_no=user_info['phone_num'], address=user_info['address'],
                    date_of_birth=user_info['dob'], gender=user_info['gender'],
                    created_at=user_info['created_at']).save()


@receiver(post_save, sender=UserProfile)
def save_userblog(sender, instance, created, **kwargs):
    if created:
        blog_info = getattr(instance, 'info', None)
        blog = Blog(created_by=instance.user, slug=blog_info['blog_slug'],
                    text=blog_info['blog_text'], created_on=datetime.datetime.now().date(),
                    is_published=blog_info['blog_is_published'],
                    comments_allowed=blog_info['blog_comments_allowed'],
                    is_public=blog_info['blog_is_public'])
        blog.save()


@receiver(post_save, sender=Blog)
def save_blog_comments(sender, instance, created, **kwargs):
    if created:
        comment_info = getattr(instance, 'info', None)
        comment = Comment(comment_for=instance, text=comment_info['comment_text'],
                          created_on=datetime.datetime.now(), created_by=instance.user,
                          user_ip=comment_info['ip'])
        comment.save()
