from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'user/index.html', {'home': 'active'})

def about(request):
    return render(request, 'user/about.html', {'about': 'active'})

def facility(request):
    return render(request, 'user/facility.html', {'facility': 'active'})

def contact(request):
    return render(request, 'user/contact.html', {'contact': 'active'})

def deploma(request):
    return render(request, 'user/deploma.html', {'cources': 'active'})

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