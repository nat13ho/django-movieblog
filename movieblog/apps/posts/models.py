from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils import timezone
from ckeditor import fields

from movieblog.apps.profiles.models import Profile
from movieblog.tools import compress_image


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = fields.RichTextField()
    pub_date = models.DateTimeField(default=timezone.now, editable=False)
    mod_date = models.DateTimeField(blank=True, null=True, editable=False)
    image = models.ImageField(upload_to='movieblog/posts/images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_details', kwargs={'pk': str(self.pk)})

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'

    class Meta:
        ordering = ['pub_date']
