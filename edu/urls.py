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
    path('std-list', std_list),
    path('course', course),
    path('generate-enroll', generate_enroll),
    path('enroll-list', enroll_list),
    path('exam-marks', exam_marks),
    path('result-list', result_list),
]
