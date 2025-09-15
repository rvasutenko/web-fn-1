from django.shortcuts import render

def about_page(request):
    return render(request, 'about.html')

def materials_page(request):
    return render(request, 'materials.html')