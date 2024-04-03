from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def index(request, id):
    return HttpResponse("hello world")

def problem(request, id):
    return HttpResponse("hello world")