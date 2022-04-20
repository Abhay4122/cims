from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('index', index),
    path('login', signin),
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
    path('result', result),
    path('certification', certification),
    path('logout', log_out)
]
