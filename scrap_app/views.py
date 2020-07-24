from django.shortcuts import render
from .models import Vacantion
from .forms import FindForm

def home_view(request):
    print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacantion.objects.filter(**_filter)
    context = {'object_list': qs, 'form': form}
    return render(request, 'scrap_app/home.html', context)
