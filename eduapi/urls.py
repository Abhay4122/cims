from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('course-api', CourseApi.as_view()),
    path('student-api', StudentApi.as_view()),
    path('enroll-api', EnrollApi.as_view()),
    path('exam-api', ExamApi.as_view()),
    path('non-examinee-api', NonExamineeAPI.as_view()),
    path('generate-certificate-api', CertificateApi.as_view()),
]