from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Vacantion
from .forms import FindForm

def home_view(request):
    print(request.GET)
    form = FindForm()
    context = {'form': form}
    return render(request, 'scrap_app/home.html', context)

def list_view(request):
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
        paginator = Paginator(qs, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    context = {'object_list': qs, 'form': form}
    return render(request, 'scrap_app/list.html', context)

