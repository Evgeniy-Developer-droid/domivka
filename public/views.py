from django.shortcuts import render


def home(request):
    return render(request, 'public/home.html', {"title": "Home"})


def catalog(request):
    return render(request, 'public/catalog.html', {"title": "Catalog"})


def real_estate(request, pk):
    return render(request, 'public/home.html', {"title": "Real estate"})
