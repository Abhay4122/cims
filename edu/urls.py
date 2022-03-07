from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('about', about),
    path('facility', facility),
    path('contact', contact),
    path('deploma', deploma),
    path('tution', tution),
    path('distance', distance),
    path('regular', regular),
    path('dashboard', dashboard),
    path('student', student),
    path('course', course),
    path('exam', exam)
]
