from django.db import models

# Create your models here.

class TouristicZone(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='places/images/')
    trending = models.IntegerField('Trending',blank=True,null=True)