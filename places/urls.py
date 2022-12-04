from django.urls import path
from . import views

app_name = 'places'


urlpatterns = [
    path('',views.Places.as_view(),name='places'),
]
