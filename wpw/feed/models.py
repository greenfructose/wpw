from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


def upload_path_handler(instance, filename):
    return "posts/images/{}/{}".format(instance.user_name.id, filename)


class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=upload_path_handler)
    tags = models.CharField(max_length=100, blank=True)
    tribe = models.ForeignKey('tribes.Tribe', related_name='tribe', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
