from django.db import models


class RealEstate(models.Model):
    TYPE_REAL_ESTATE = (
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('office', 'Office'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='real_estate/', null=True, blank=True)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    type_real_estate = models.CharField(max_length=10, choices=TYPE_REAL_ESTATE, default='house')


class RealEstateImage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='real_estate_images/')
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
