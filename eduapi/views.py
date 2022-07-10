import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .serializers import *
from .models import *
from django.db.models import Max

from utils import ViewUtil


class CourseApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        return self.obj.get(request, Course, CourseListSerializer, CourseSerializer, 'Course')
    
    def post(self, request: dict) -> dict:
        return self.obj.post(request, CourseSerializer, 'Course created', '/course')
    
    def put(self, request: dict) -> dict:
        return self.obj.put(request, Course, CourseSerializer, 'Course updated', '/course')
    
    def delete(self, request: dict) -> dict:
        return self.obj.delete(request, Course, 'Course', '/course')


class StudentApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        if bool(dict(request.GET)):
            if request.GET.get('id'):
                get_value = Student.objects.filter(id=request.GET.get('id'))

                if get_value.exists():
                    resp = StudentDetailSerializer(get_value[0], many=False).data
                else:
                    msg = f'Student data not found.'
                    resp = {
                        **{'status': status.HTTP_404_NOT_FOUND},
                        **self.resp_fun(msg, '', 'error')
                    }
            elif request.GET.get('year'):
                resp = RegStudentListSerializer(Student.objects.filter(reg_year=request.GET.get('year'), is_registerd=True, is_enrolled=False, is_examinee=False, is_certified=False), many=True).data
        else:
            year = Student.objects.aggregate(Max('reg_year'))
            resp = RegStudentListSerializer(Student.objects.filter(reg_year=year['reg_year__max'], is_registerd=True, is_enrolled=False, is_examinee=False, is_certified=False), many=True).data
        
        return Response(resp)
        # return self.obj.get(request, Student, RegStudentListSerializer, StudentDetailSerializer, 'Student')
    
    def post(self, request: dict) -> dict:
        try:
            request.data._mutable = True
        except Exception as e:
            self.obj.prin(e)

        request.data.update({'is_registerd': True})
        return self.obj.post(request, StudentSerializer, 'Student registerd', '/student')
    
    def put(self, request: dict) -> dict:
        if request.FILES:
            try:
                request.data._mutable = True
            except Exception as e:
                self.obj.prin(e)

            request.data.update({'is_registerd': True})
            return self.obj.put(request, Student, StudentSerializer, 'Student updated', '/student')
        else:
            try:
                request.data._mutable = True
            except Exception as e:
                self.obj.prin(e)

            request.data.update({'is_registerd': True})
            return self.obj.put(request, Student, StudentWithoutPhotoSerializer, 'Student updated', '/student')
    
    def delete(self, request: dict) -> dict:
        return self.obj.delete(request, Student, 'Student', '/student')


class EnrollApi(APIView):
    # permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        get_data = Student.objects.filter(id=request.GET.get('id'), enroll_number=None).values('name', 'reg_year')
        if get_data.exists():
            return_str = get_data[0]['name']

            generated_number = self.create_enroll(get_data[0]['reg_year'])

            get_data.update(enroll_number=generated_number, is_enrolled=True)
            msg = f'{return_str}\'s enroll has been generated successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/exam', 'success')
            }
        else:
            msg = f'Enrollment for this student is alredy exists.'
            resp = {
                **{'status': status.HTTP_404_NOT_FOUND},
                **self.obj.resp_fun(msg, '/exam', 'error')
            }
        
        return Response(resp)

    def create_enroll(self, year):
        get_data = Student.objects.filter(Q(reg_year=year), ~Q(enroll_number=None)).aggregate(Max('enroll_number'))
        
        if get_data['enroll_number__max']:
            return f"CIMS-{year}/{'%04d' % ((int(get_data['enroll_number__max'].split('/')[1]) + 1),)}"
        else:
            return f"CIMS-{year}/{'%04d' % (1,)}"


class NonExamineeAPI(APIView):
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        if bool(dict(request.GET)):
            examinee = Student.objects.filter(is_examinee=False, is_enrolled=True, id=request.GET.get('id'))
            resp = StudentDetailSerializer(examinee, many=False).data
        else:
            non_examinee = Student.objects.filter(is_examinee=False, is_enrolled=True)
            resp = StudentListSerializer(non_examinee, many=True).data
        
        return Response(resp)


class ExamApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        if bool(dict(request.GET)):
            if request.GET.get('id'):
                examinee = Student.objects.filter(id=request.GET.get('id'), is_enrolled=True, is_examinee=False, is_certified=False)
                if examinee[0].course.course_name.lower() == 'adca':
                    resp = StudentADCAExamineeDetailSerializer(examinee[0], many=False).data
                else:
                    resp = StudentDCAExamineeDetailSerializer(examinee[0], many=False).data

            if request.GET.get('year'):
                examinee = Student.objects.filter(reg_year=request.GET.get('year'), is_enrolled=True, is_examinee=False, is_certified=False)
                resp = StudentExamineeListSerializer(examinee, many=True).data
        else:
            year = Student.objects.aggregate(Max('reg_year'))
            examinee = Student.objects.filter(reg_year=year['reg_year__max'], is_enrolled=True, is_examinee=False, is_certified=False)
            resp = StudentExamineeListSerializer(examinee, many=True).data
        
        return Response(resp)
    
    def post(self, request: dict) -> dict:
        resp = request_filter(request, 'add')
        if resp:
            msg = f'Exam marks has been added successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/exam', 'success')
            }
        else:
            msg = f'Exam marks has not been added.'
            resp = {
                **{'status': status.HTTP_406_NOT_ACCEPTABLE},
                **self.obj.resp_fun(msg, '', 'error')
            }
        
        return Response(resp)


class CertificateAPI(APIView):
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        if bool(dict(request.GET)):
            if request.GET.get('id'):
                certified = Student.objects.filter(id=request.GET.get('id'), is_examinee=True)
                if certified.exists():
                    if certified[0].course.course_name.lower() == 'adca':
                        resp = StudentADCAExamineeDetailSerializer(certified[0], many=False).data
                    else:
                        resp = StudentDCAExamineeDetailSerializer(certified[0], many=False).data
                else:
                    msg = f'Student Does not exists.'
                    resp = {
                        **{'status': status.HTTP_404_NOT_FOUND},
                        **self.obj.resp_fun(msg, '/exam', 'error')
                    }
            if request.GET.get('year'):
                certificate = Student.objects.filter(reg_year=request.GET.get('year'), is_registerd=True, is_enrolled=True, is_examinee=True)
                resp = StudentCertifiedListSerializer(certificate, many=True).data
        else:
            year = Student.objects.aggregate(Max('reg_year'))
            cretificate = Student.objects.filter(reg_year=year['reg_year__max'], is_registerd=True, is_enrolled=True, is_examinee=True)
            resp = StudentCertifiedListSerializer(cretificate, many=True).data
        
        return Response(resp)
    
    def put(self, request: dict) -> dict:
        resp = request_filter(request, 'update')
        if resp:
            msg = f'Exam marks has been updated successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/certificate-list', 'success')
            }
        else:
            msg = f'Exam marks has not been updated.'
            resp = {
                **{'status': status.HTTP_406_NOT_ACCEPTABLE},
                **self.obj.resp_fun(msg, '', 'error')
            }
        
        return Response(resp)


class EnableDisableCertiApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request: dict) -> dict:
        toggle = True if request.GET.get('is_certi') == 'false' else False
        Student.objects.filter(id=request.GET.get('id')).update(is_certified=toggle)
        
        msg = f'Certificate has been {"Enabled" if toggle else "Disabled"} successfully.'
        resp = {
            **{'status': status.HTTP_200_OK},
            **self.obj.resp_fun(msg, '/certificate-list', 'success'),
            **{'status': toggle}
        }
        
        return Response(resp)


def request_filter(request: dict, method: str) -> bool:
    req = request.POST
    std = req.get('name').split('*')

    try:
        if method == 'add':
            certi_no = gen_certi_no(std[4].split('- ')[1].split(' to')[0])

            if std[3].lower() == 'adca':
                Student.objects.filter(id=std[0]).update(
                    theory_s1=req.get('theory_s1'), os=req.get('os'), pretical_s1=req.get('pretical_s1'),
                    theory_s2=req.get('theory_s2'), pretical_s2=req.get('pretical_s2'), oral_s2=req.get('oral_s2'),
                    exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True,
                    cretificate_no=certi_no
                )
            else:
                Student.objects.filter(id=std[0]).update(
                    theory_s1=req.get('theory_s1'), pretical_s1=req.get('pretical_s1'), oral_s1=req.get('oral_s1'),
                    exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True,
                    cretificate_no=certi_no
                )
        else:
            if std[3].lower() == 'adca':
                Student.objects.filter(id=std[0]).update(
                    theory_s1=req.get('theory_s1'), os=req.get('os'), pretical_s1=req.get('pretical_s1'),
                    theory_s2=req.get('theory_s2'), pretical_s2=req.get('pretical_s2'), oral_s2=req.get('oral_s2'),
                    exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True
                )
            else:
                Student.objects.filter(id=std[0]).update(
                    theory_s1=req.get('theory_s1'), pretical_s1=req.get('pretical_s1'), oral_s1=req.get('oral_s1'),
                    exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True
                )
        
        return True
    except Exception as e:
        self.obj.prin(e)
        return False

def gen_certi_no(year: str) -> str:
    year_numbering = {'2017': '', '2018': 'A', '2019': 'B', '2020': 'C', '2021': 'D', '2022': 'E', '2023': 'F', '2024': 'G', '2025': 'H'}
    get_data = Student.objects.filter(Q(reg_year=year), ~Q(cretificate_no=None)).aggregate(Max('cretificate_no'))

    if get_data['cretificate_no__max']:
        return f"C{year_numbering[year]}{'%03d' % ((int(get_data['cretificate_no__max'][2:]) + 1),)}"
    else:
        return f"C{year_numbering[year]}{'%03d' % (501,)}"