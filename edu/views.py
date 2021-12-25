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

def std_registration(request):
    if request.method == 'POST':
        print(f'\n\n\{request.POST}\n\n\n')
        response = {'response': 200, 'msg_type': 'success', 'msg': 'Student created succesfully', 'student': 'active'}
    else:
        response = {'student': 'active'}

    return render(request, 'administrator/std_registration.html', response)

def std_list(request):
    return render(request, 'administrator/std_list.html')

def course(request):
    return render(request, 'administrator/course.html')

def generate_enroll(request):
    return render(request, 'administrator/generate_enroll.html')

def enroll_list(request):
    return render(request, 'administrator/enroll_list.html')

def exam_marks(request):
    return render(request, 'administrator/exam_marks.html')

def result_list(request):
    return render(request, 'administrator/result_list.html')