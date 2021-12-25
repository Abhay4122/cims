from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('facility', facility, name='facility'),
    path('contact', contact, name='contact'),
    path('deploma', deploma, name='deploma'),
    path('tution', tution, name='tution'),
    path('distance', distance, name='distance'),
    path('regular', regular, name='regular'),
    path('dashboard', dashboard, name='dashboard'),
    path('std-registration', std_registration, name='std-registration'),
    path('std-list', std_list, name='std_list'),
    path('course', course, name='course'),
    path('generate-enroll', generate_enroll, name='generate_enroll'),
    path('enroll-list', enroll_list, name='enroll_list'),
    path('exam-marks', exam_marks, name='exam_marks'),
    path('result-list', result_list, name='result_list'),
]
