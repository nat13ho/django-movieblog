import os
import absoluteuri

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from posts.models import Post
from profiles.models import Profile


@receiver(post_delete, sender=Post)
def auto_delete_image_on_post_delete(sender, instance, **kwargs):
    """
    Deletes post image from media folder when corresponding post is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Post)
def auto_delete_image_on_post_update(sender, instance, **kwargs):
    """
    Deletes old image of a post if new image is provided.
    """
    if not instance.pk:
        return False

    if instance.image:
        try:
            old_image = Post.objects.get(pk=instance.pk).image
        except Post.DoesNotExist:
            return False

        new_image = instance.image
        if old_image != new_image and old_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)


@receiver(post_save, sender=Post)
def auto_notify_user_on_post_create(sender, instance: Post, created, **kwargs):
    if created:
        post_url = absoluteuri.build_absolute_uri(instance.get_absolute_url())
        subject = 'Новость на MovieBlog'
        message = f'{instance.title}. Подробнее можно почитать по следующей ссылке: {post_url}'
        recipients = list(Profile.objects.filter(is_subscribed=True).values_list('user__email', flat=True))
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipients,
            from_email=None,
            fail_silently=False
        )
    else:
        Post.objects.filter(pk=instance.pk).update(mod_date=timezone.now())
