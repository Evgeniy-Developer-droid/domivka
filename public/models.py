from django.contrib.auth.models import User
from django.db import models


class RealEstate(models.Model):
    TYPE_REAL_ESTATE = (
        ('house', 'Дім'),
        ('apartment', 'Квартира'),
        ('office', 'Офіс'),
    )
    SERVICE_TYPE = (
        ('sale', 'Продаж'),
        ('rent', 'Оренда'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='real_estate/', null=True, blank=True)
    price = models.IntegerField(default=0)
    rooms = models.IntegerField(default=1)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=1000, default="")
    region = models.CharField(max_length=1000, default="")
    city_code = models.CharField(max_length=255, default="")
    region_code = models.CharField(max_length=255, default="")
    viewed = models.IntegerField(default=0)
    viewed_phone = models.IntegerField(default=0)
    type_real_estate = models.CharField(max_length=10, choices=TYPE_REAL_ESTATE, default='house')
    service_type = models.CharField(max_length=4, choices=SERVICE_TYPE, default='rent')


class RealEstateImage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='real_estate_images/')
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True, blank=True)


class Region(models.Model):
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    has_districts = models.BooleanField(default=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    radius = models.IntegerField(default=1)
    zoom = models.IntegerField(default=1)
    region = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name+" - "+self.region


class Report(models.Model):
    name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    text = models.TextField()
    