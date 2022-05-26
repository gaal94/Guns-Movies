from django.db import models
from django.conf import settings

class GunType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Gun(models.Model):
    gun_name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    gun_weight = models.CharField(max_length=50)
    gun_length = models.CharField(max_length=50)
    gun_caliber = models.CharField(max_length=50)
    gun_image_path = models.CharField(max_length=200)
    gun_youtube_url = models.CharField(max_length=300, null=True, blank=True)
    gun_type = models.ForeignKey(GunType, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_guns', blank=True)

    def __str__(self):
        return self.gun_name