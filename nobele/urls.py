from django.urls import path
from . import views

app_name = 'nobele'

urlpatterns = [
    path("", views.main_page, name='main'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('login/verify/',views.verify,name='verify'),
    path('login/verificate/',views.verificate_manually,name='verificate'),
    path('user/',views.user_page,name='user'),
    path('user/logout/',views.logout_from_account,name='logout'),
    path('country/<int:pk>',views.CountryView.as_view(),name='country'),
    path('country/<int:pk>/new_comment',views.new_comment,name='new_comment'),
    path('country/<int:id>/city/<int:pk>',views.CityView.as_view(),name='city'),
    path('hotel/<int:pk>/rate',views.rate_hotel,name='rate'),
]
