from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .serializers import *
from .models import *

from utils import prin, resp_fun, ViewUtil


class CourseApi(APIView):
    # permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Course, CourseSerializer, 'Course')
    
    def post(self, request):
        return self.obj.post(request, Course, CourseSerializer, 'Course')
    
    def put(self, request):
        return self.obj.put(request, Course, CourseSerializer, 'Course')
    
    def delete(self, request):
        return self.obj.delete(request, Course, CourseSerializer, 'Course')


class StudentApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Student, StudentSelectedFieldsSerializer, 'Student')
    
    def post(self, request):
        course = self.obj.get_model_data(Course, request.POST.get('course'))
        data = self.get_course_detail(course[0].cors_dur)
        request.data.update(data)
        
        return self.obj.post(request, Student, StudentSelectedFieldsSerializer, 'Student')
    
    def put(self, request):
        return self.obj.put(request, Student, StudentSelectedFieldsSerializer, 'Student')
    
    def delete(self, request):
        return self.obj.delete(request, Student, StudentSelectedFieldsSerializer, 'Student')
    
    def get_course_detail(self, course_dur):
        date = datetime.today().date()
        reg_year = date.year
        reg_mon = date.month
        session = date + relativedelta(months=int(course_dur))
        session_year = session.year
        session_mon = session.month
        enroll_no = 'CIMS-2018/0007'

        return {
            'reg_year': reg_year, 'reg_mon': reg_mon, 'session_year': session_year, 'session_month': session_mon,
            'enroll_number': enroll_no
        }
