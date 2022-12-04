from django.contrib import admin

# Register your models here.
from .models import TouristicZone


admin.site.site_header = 'Around the World'
admin.site.site_title = 'ATW'
admin.site.index_title = '"Around the World" admin panel'

admin.site.register(TouristicZone)