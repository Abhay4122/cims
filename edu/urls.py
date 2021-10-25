from django.urls import path
from .views import *

urlpatterns = [
    path('', index , name='index'),
    path('about', about , name='about'),
    path('facility', facility , name='facility'),
    path('contact', contact , name='contact'),
    path('dashboard', dashboard , name='dashboard'),
]
