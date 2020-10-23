from autoslug import AutoSlugField
from django.db import models


def upload_path_handler(instance, filename):
    return "tribes/tribe_pic/{}/{}".format(instance.name, filename)


class Tribe(models.Model):
    name = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(default='default.png', upload_to=upload_path_handler)
    members = models.ManyToManyField('users.Profile', blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return "/tribes/{}".format(self.slug)


class Membership(models.Model):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    tribe = models.ForeignKey('tribes.Tribe', on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
