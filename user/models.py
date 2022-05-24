from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static


class Profile(models.Model):
    phone = models.CharField(max_length=255, default="")
    avatar = models.ImageField(upload_to='avatars/', default=static('user/img/avatar.webp'))
    facebook = models.CharField(max_length=500, default="", blank=True)
    linkedin = models.CharField(max_length=500, default="", blank=True)
    youtube = models.CharField(max_length=500, default="", blank=True)
    instagram = models.CharField(max_length=500, default="", blank=True)
    skype = models.CharField(max_length=500, default="", blank=True)
    whatsapp = models.CharField(max_length=500, default="", blank=True)
    viber = models.CharField(max_length=500, default="", blank=True)
    telegram = models.CharField(max_length=500, default="", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
