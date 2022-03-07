from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from .serializers import *
from .models import *

from utils import ViewUtil


class CourseApi(APIView):
    # permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Course, CourseListSerializer, CourseSerializer, 'Course')
    
    def post(self, request):
        return self.obj.post(request, Course, CourseSerializer, 'Course created', '/course')
    
    def put(self, request):
        return self.obj.put(request, Course, CourseSerializer, 'Course updated', '/course')
    
    def delete(self, request):
        return self.obj.delete(request, Course, 'Course', '/course')


class StudentApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Student, StudentListSerializer, StudentDetailSerializer, 'Student')
    
    def post(self, request):
        return self.obj.post(request, Student, StudentSerializer, 'Student registerd', '/student')
    
    def put(self, request):
        return self.obj.put(request, Student, StudentSerializer, 'Student updated', '/student')
    
    def delete(self, request):
        return self.obj.delete(request, Student, 'Student', '/student')


class EnrollApi(APIView):
    # permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        get_data = Student.objects.filter(id=request.GET.get('id'), enroll_number=None).values('name', 'reg_year')
        if get_data.exists():
            return_str = get_data[0]['name']

            generated_number = self.create_enroll(get_data[0]['reg_year'])

            get_data.update(enroll_number=generated_number)
            msg = f'{return_str}\'s enroll has been generated successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/student', 'success')
            }
        else:
            msg = f'Student data not found'
            resp = {
                **{'status': status.HTTP_404_NOT_FOUND},
                **self.obj.resp_fun(msg, '/student', 'error')
            }
        
        return Response(resp)

    def create_enroll(self, year):
        from django.db.models import Max
        get_data = Student.objects.filter(Q(reg_year=year), ~Q(enroll_number=None)).aggregate(Max('enroll_number'))

        if get_data['enroll_number__max']:
            return int(get_data['enroll_number__max']) + 1
        else:
            return 1


class ExamApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Student, StudentListSerializer, StudentDetailSerializer, 'Student')
    
    def post(self, request):
        return self.obj.post(request, Student, StudentSerializer, 'Student registerd', '/student')
    
    def put(self, request):
        return self.obj.put(request, Student, StudentSerializer, 'Student updated', '/student')
    
    def delete(self, request):
        return self.obj.delete(request, Student, 'Student', '/student')

