from django.shortcuts import render


def home_page(request):
    return render(request, 'base.html')


def business_entities(request):
    return render(request, 'business_entities.html')