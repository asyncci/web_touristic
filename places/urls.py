from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('',views.Places.as_view(),name='tours'),
    path('tour/<int:pk>/',views.Place.as_view(),name='tour'),
    path('login/',views.login,name='login'),
    path('login/verify/',views.verify,name='verify'),
]
