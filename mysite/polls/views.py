from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.


def index(request):
    return HttpResponse("Hello this is my first view in django")
