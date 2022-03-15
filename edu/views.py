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

def diploma(request):
    data = Course.objects.filter(course_category='Diploma')
    return render(request, 'user/diploma.html', {'cources': 'active', 'data': data})

def tution(request):
    return render(request, 'user/tution.html', {'cources': 'active'})

def distance(request):
    return render(request, 'user/distance.html', {'cources': 'active'})

def regular(request):
    return render(request, 'user/regular.html', {'cources': 'active'})

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