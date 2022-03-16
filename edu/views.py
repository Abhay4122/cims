from django.http import JsonResponse
from django.shortcuts import render
from eduapi.models import Student, Course

# Create your views here.

def index(request):
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
        
        if resp.course.course_name.lower() == 'adca':
            percent = ((int(resp.theory_s1) + int(resp.os) + int(resp.pretical_s1) + int(resp.theory_s2) + int(resp.pretical_s2) + int(resp.oral_s2)) * 100) / 400
            gred = get_gred(percent)
        else:
            percent = ((int(resp.theory_s1) + int(resp.pretical_s1) + int(resp.oral_s1)) * 100) / 200
            gred = get_gred(percent)

    return render(request, 'administrator/certificate.html', {'student': resp, 'gred': gred})

def student_portal(request):
    if request.POST:
        if request.POST.get('purpose') == 'result':
            student = Student.objects.filter(dob=request.POST.get('dob'), enroll_number=request.POST.get('enroll_number'))
            
            if student.exists():
                return render(request, 'user/result.html', {'data': student})
            else:
                msg = f'Student record not found, Please contact to admin.'
                resp = {
                    **{'status': '404'},
                    **{'title': 'Please notice !', 'msg': msg, 'lod_link': '/student-portal?purpose=result', 'alert_type': 'error'}
                }
                return JsonResponse(resp)
        elif request.POST.get('purpose') == 'certificate':
            student = Student.objects.filter(dob=request.POST.get('dob'), enroll_number=request.POST.get('enroll_number'))
            
            if student.exists():
                resp = None
                gred = None
                resp = student[0]
                
                if resp.course.course_name.lower() == 'adca':
                    percent = ((int(resp.theory_s1) + int(resp.os) + int(resp.pretical_s1) + int(resp.theory_s2) + int(resp.pretical_s2) + int(resp.oral_s2)) * 100) / 400
                    gred = get_gred(percent)
                else:
                    percent = ((int(resp.theory_s1) + int(resp.pretical_s1) + int(resp.oral_s1)) * 100) / 200
                    gred = get_gred(percent)

                return render(request, 'administrator/certificate.html', {'student': resp, 'gred': gred})
            else:
                msg = f'Student record not found, Please contact to admin.'
                resp = {
                    **{'status': '404'},
                    **{'title': 'Please notice !', 'msg': msg, 'lod_link': '/student-portal?purpose=certificate', 'alert_type': 'error'}
                }
                return JsonResponse(resp)
    else:
        return render(request, 'user/student_portal.html', {'student': 'active'})

def certification(request):
    return render(request, 'user/certification.html', {'student': 'active'})


def get_gred(percent):
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