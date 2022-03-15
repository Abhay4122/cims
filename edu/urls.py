from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('about', about),
    path('facility', facility),
    path('contact', contact),
    path('diploma', diploma),
    path('tution', tution),
    path('distance', distance),
    path('regular', regular),
    path('dashboard', dashboard),
    path('student', student),
    path('course', course),
    path('exam', exam),
    path('certificate', certificate)
]
