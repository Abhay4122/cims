from django.http import JsonResponse
from django.shortcuts import render
from eduapi.models import Student, Course

# Create your views here.

def index(request):
    db_update()
    return render(request, 'user/index.html', {'home': 'active'})

def about(request):
    return render(request, 'user/about.html', {'about': 'active'})

def facility(request):
    return render(request, 'user/facility.html', {'facility': 'active'})

def contact(request):
    return render(request, 'user/contact.html', {'contact': 'active'})

def courses(request):
    data = Course.objects.filter(course_category=request.GET.get('type'))
    return render(request, 'user/courses.html', {'courses': 'active', 'data': data})

def dashboard(request):
    return render(request, 'administrator/dashboard.html')

def student(request):
    return render(request, 'administrator/student.html', {'student': 'active'})

def course(request):
    return render(request, 'administrator/course.html', {'course': 'active'})

def exam(request):
    return render(request, 'administrator/exam.html', {'exam': 'active'})

def certificate(request):
    resp = None
    gred = None

    if request.GET:
        resp = Student.objects.filter(id=request.GET.get('id'))[0]
        gred = get_gred(resp)

    return render(request, 'administrator/certificate.html', {'student': resp, 'gred': gred})

def student_portal(request):
    if request.POST:
        if request.POST.get('purpose') == 'result':
            student = Student.objects.filter(dob=request.POST.get('dob'), enroll_number=request.POST.get('enroll_number'), is_certified=1)
            
            if student.exists():
                return JsonResponse({'id': student[0].id})
            else:
                msg = f'Student record not found OR not authorize, Please contact to Varanasi office.'
                resp = {
                    **{'status': '404'},
                    **{'title': 'Please notice !', 'msg': msg, 'lod_link': '/student-portal?purpose=result', 'alert_type': 'error'}
                }
                return JsonResponse(resp)
        elif request.POST.get('purpose') == 'certificate':
            student = Student.objects.filter(dob=request.POST.get('dob'), enroll_number=request.POST.get('enroll_number'), is_certified=1)
            
            if student.exists():
                return JsonResponse({'id': student[0].id})
            else:
                msg = f'Student record not found OR not authorize, Please contact to Varanasi office.'
                resp = {
                    **{'status': '404'},
                    **{'title': 'Please notice !', 'msg': msg, 'lod_link': '/student-portal?purpose=certificate', 'alert_type': 'error'}
                }
                return JsonResponse(resp)
    else:
        return render(request, 'user/student_portal.html', {'student': 'active'})

def certification(request):
    student = Student.objects.filter(id=request.GET.get('id'), is_certified=1)
    if student.exists():
        resp = None
        gred = None
        resp = student[0]

        gred = get_gred(resp)

        return render(request, 'administrator/certificate.html', {'student': resp, 'gred': gred})
    else:
        return render(request, 'user/student_portal.html', {'student': 'active'})

def result(request):
    student = Student.objects.filter(id=request.GET.get('id'))
    
    if student.exists():
        gred = get_gred(student[0])

        return render(request, 'user/result.html', {'data': student[0], 'gred': gred})


def get_gred(resp):
    if resp.course.course_name.lower() == 'adca':
        percent = ((int(resp.theory_s1) + int(resp.os) + int(resp.pretical_s1) + int(resp.theory_s2) + int(resp.pretical_s2) + int(resp.oral_s2)) * 100) / 400
    else:
        percent = ((int(resp.theory_s1) + int(resp.pretical_s1) + int(resp.oral_s1)) * 100) / 200
    
    if percent >= 85:
        return 'A+'
    elif percent >= 74:
        return 'A'
    elif percent >= 65:
        return 'B'
    elif percent >= 55:
        return 'C'
    elif percent >= 40:
        return 'D'
    else:
        return 'F'


def db_update():
    from pathlib import Path
    import pandas as pd

    BASE_DIR = Path(__file__).resolve().parent.parent

    # old_std = pd.read_csv(BASE_DIR / 'old_DB/student.csv')
    # print(old_std)

    import csv

    # with open(BASE_DIR / 'old_DB/course.csv', mode='r') as course_raw:
    #     old_course = csv.reader(course_raw)
    #     old_course = [rows for rows in old_course]
    
    # for i in old_course:
    #     course = Course(
    #         course_category = i[1].split(' ')[0], course_name = i[2],
    #         course_full_form = i[3], course_duration = i[4],
    #         course_detail = i[5], course_package = i[6]
    #     )
        
    #     course.save()


    # with open(BASE_DIR / 'old_DB/student.csv', mode='r') as std_raw:
    #     old_std = csv.reader(std_raw)
    #     old_std = [rows for rows in old_std]
    
    # for i in old_std:
    #     course = Course.objects.get(course_name=i[10])

    #     #Insert the Student SR817534671
    #     std = Student(
    #         name=i[1] + ' ' + i[2], gender=i[3], father=i[4], mother=i[5], dob=i[6], address=i[7],
    #         contact=i[8], category=i[9], course=course, lpc=i[11], passing_year=i[12],
    #         board=i[13], gread=i[14], photo=i[15], reg_year=i[16], reg_mon=i[19],
    #         session_year=i[21], session_month=i[20], is_registerd=True
    #     )

    #     std.save()


    with open(BASE_DIR / 'old_DB/total_fee.csv', mode='r') as std_raw:
        old_std = csv.reader(std_raw)
        old_std = [rows for rows in old_std]
    
    for i in old_std:
        # Update the enroll number
        # std = Student.objects.filter(name=i[1] + ' ' + i[2]).update(enroll_number=)
        print(i)
        break