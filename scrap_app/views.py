from django.shortcuts import render
from .models import Vacantion

def home_view(request):
    qs = Vacantion.objects.all()
    context = {'object_list': qs}
    return render(request, 'scrap_app/home.html', context)
