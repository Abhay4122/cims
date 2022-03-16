from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('about', about),
    path('facility', facility),
    path('contact', contact),
    path('courses', courses),
    path('dashboard', dashboard),
    path('student', student),
    path('course', course),
    path('exam', exam),
    path('certificate', certificate),
    path('student-portal', student_portal),
    path('certification', certification)
]
