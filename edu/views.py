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

def dashboard(request):
    return render(request, 'administrator/dashboard.html')