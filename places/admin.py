from django.contrib import admin

# Register your models here.
from . import models


admin.site.site_header = 'Around the World'
admin.site.site_title = 'ATW'
admin.site.index_title = '"Around the World" admin panel'

admin.site.register(models.Tour)
admin.site.register(models.Image)
admin.site.register(models.Account)
admin.site.register(models.VerifToken)