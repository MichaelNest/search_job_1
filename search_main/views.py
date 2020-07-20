from django.shortcuts import render
import datetime


def home(request):
    date = datetime.datetime.now().date()
    name = 'Vasiliy'
    context = {'name': name, 'date': date}

    return render(request, 'home.html', context)