from django.db import models

# account

class Account(models.Model):
    email = models.EmailField('Account Email',max_length=50, primary_key=True)
    password = models.CharField('Hashed Password',max_length=100)
    
    name = models.CharField('Name',max_length=100,null=True)
    surname = models.CharField('Surname',max_length=100,null=True)

    verified = models.BooleanField('Verified',default=False)

    def __str__(self) -> str:
        return self.email

class VerificationToken(models.Model):
    email = models.CharField(max_length=50)
    token = models.IntegerField(null=False)

    def __str__(self) -> str:
        return self.email 

class Session(models.Model):
    ip = models.CharField(max_length=30,primary_key=True)
    account = models.OneToOneField(Account,on_delete=models.CASCADE)

# account








# touring 

class Country(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name + ' --- ' + self.country.name


class Comment(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    author = models.ForeignKey(Account,on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)

    def __str__(self) -> str:
        return self.country.name + ' :: ' + self.author.name

class Hotel(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,editable=False)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stars = models.IntegerField('Rating',default=0)

    def __str__(self) -> str:
        return self.name + ' :in: ' + self.country.name

    def save(self, *args, **kwargs):
        self.country = self.country_of()
        super().save(*args, **kwargs)

    def country_of(self):
        return self.city.country


class HotelRating(models.Model):
    hotel = models.OneToOneField(Hotel,on_delete=models.CASCADE,primary_key=True)
    count = models.IntegerField('How many people voted',default=0)
    summary = models.IntegerField('Rating summary',default=0)
    key = models.IntegerField('Hotel PK',editable=False)

    def save(self, *args, **kwargs):
        self.hotel_id = self.hotel.pk
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.hotel.name
# touring