# main/views.py

from django.shortcuts import render


def home(request):
    return render(request, 'main.html')

def about_us(request):
    return render(request, 'about_us.html')

def rules(request):
    return render(request, 'rules.html')
