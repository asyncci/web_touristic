from django.shortcuts import render
from django.views.generic import ListView
from . import models


class Places(ListView):
    model = models.TouristicZone
    template_name = "places/touristic_zones.html"