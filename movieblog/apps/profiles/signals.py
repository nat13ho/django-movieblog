import os

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def auto_delete_image_on_profile_delete(sender, instance, **kwargs):
    """
    Deletes image when corresponding profile is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Profile)
def delete_old_image_on_profile_update(sender, instance, **kwargs):
    """
    Deletes old image of a profile if new image is provided.
    """
    if not instance.pk:
        return False

    if instance.image:
        try:
            old_image = Profile.objects.get(pk=instance.pk).image
        except Profile.DoesNotExist:
            return False

        new_image = instance.image
        if new_image != old_image and old_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)