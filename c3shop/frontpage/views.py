from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("<h1>index: Not yet implemented</h1>")


def detailedarticle(resquest):
    return HttpResponse("<h1>article: Not yet implemented</h1>")

