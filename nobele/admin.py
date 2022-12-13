from django.contrib import admin
from . import models
from .models import Hotel
# Register your models here.

admin.site.register(models.Account)
admin.site.register(models.VerificationToken)
admin.site.register(models.Session)

admin.site.register(models.Country)
admin.site.register(models.City)
admin.site.register(models.Comment)
admin.site.register(Hotel)

admin.site.register(models.HotelRating)

class HotelAdmin(admin.ModelAdmin):
    exclude=('country',)
    readonly_fields=('country', )