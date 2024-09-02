from django.shortcuts import render

# Create your views here.
# laesquina/main/views.py

from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("Hola mundo")
