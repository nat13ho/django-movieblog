from django.contrib.auth.models import User
from django.db import models


from movieblog.tools import compress_image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='movieblog/profiles/images', blank=True, null=True)
    posts = models.ManyToManyField('posts.Post')
    is_subscribed = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(image=self.image, max_res=640)
        super().save(*args, **kwargs)
