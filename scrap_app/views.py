from django.shortcuts import render
from .models import Vacantion

def home_view(request):
    # print(request.GET)
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if language:
            _filter['language__name'] = language
        qs = Vacantion.objects.filter(**_filter)
    context = {'object_list': qs}
    return render(request, 'scrap_app/home.html', context)
