from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def reviews(request):
    return HttpResponse("Welcome to ReelRatings!")