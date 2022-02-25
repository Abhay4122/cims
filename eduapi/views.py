from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
        return self.obj.put(request, Course, CourseSerializer, 'Course')
    
    def delete(self, request):
        return self.obj.delete(request, Course, 'Course')


class StudentApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Student, StudentListSerializer, StudentSerializer, 'Student')
    
    def post(self, request):
        course = self.obj.get_model_data(Course, request.POST.get('course'))
        data = self.get_course_detail(course[0].cors_dur)
        try:
            request.data._mutable = True
        except Exception as e:
            self.obj.prin(e)

        request.data.update(data)
        
        return self.obj.post(request, Student, StudentSerializer, 'Student registerd', '/student')
    
    def put(self, request):
        course = self.obj.get_model_data(Course, request.POST.get('course'))
        data = self.get_course_detail(course[0].cors_dur)
        request.data.update(data)
        
        return self.obj.put(request, Student, StudentSerializer, 'Student')
    
    def delete(self, request):
        return self.obj.delete(request, Student, 'Student')
    
    def get_course_detail(self, course_dur):
        date = datetime.today().date()
        reg_year = date.year
        reg_mon = f"{date.strftime('%b')}_{date.month}"
        session = date + relativedelta(months=int(course_dur))
        session_year = session.year
        session_mon = f"{session.strftime('%b')}_{session.month}"
        enroll_no = 'CIMS-2018/0007'

        return {
            'reg_year': reg_year, 'reg_mon': reg_mon, 'session_year': session_year, 'session_month': session_mon,
            'enroll_number': enroll_no
        }
