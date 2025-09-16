from django.shortcuts import render
from .models import Material, News
from collections import defaultdict


def about_page(request):
    return render(request, 'about.html')

def materials_page(request):
    materials_grouped = Material.objects.for_other_faculties()

    def convert_dd(d):
        if isinstance(d, defaultdict):
            d = {k: convert_dd(v) for k, v in d.items()}
        return d

    materials_dict = convert_dd(materials_grouped)

    news = News.objects.all()

    return render(request, "materials.html", {"materials": materials_dict, "news": news})