from django.db import models

class Tour(models.Model):
    title = models.EmailField(max_length=50)
    main_image = models.ImageField(upload_to="places/images/",null=True)

    def __str__(self) :
        return self.title

class Image(models.Model):
    picture = models.ImageField(upload_to="places/images/")
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)

    def __str__(self):
        return self.tour.title

class Account(models.Model):
    ip = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,primary_key=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class VerifToken(models.Model):
    email = models.CharField(max_length=25, primary_key=True)
    token = models.IntegerField(default=0,null=True)