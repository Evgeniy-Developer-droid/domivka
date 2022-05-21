from django.shortcuts import render

from public.forms import ContactUsForm
from public.models import RealEstate, RealEstateImage, Report
from public.tools.functions import get_seo


def home(request):
    return render(request, 'public/home.html', {"title": "Головна сторінка", 'seo': get_seo()})


def catalog(request):
    return render(request, 'public/catalog.html', {"title": "Каталог", 'seo': get_seo()})


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            email = form.cleaned_data.get('email', '')
            text = form.cleaned_data.get('text', '')
            Report(name=name, email=email, text=text).save()
            return render(request, 'public/contact_us.html', {"saved": True, "title": "Зв'яжіться з нами", 'seo': get_seo()})
    form = ContactUsForm()
    return render(request, 'public/contact_us.html', {'form': form, "title": "Зв'яжіться з нами", 'seo': get_seo()})


def real_estate(request, pk):
    try:
        instance = RealEstate.objects.get(pk=pk)
        if request.user.pk != instance.user.pk:
            instance.viewed += 1
            instance.save()
        images = RealEstateImage.objects.filter(real_estate=instance.pk)
        return render(request, 'public/single.html', {"title": "Нерухомість", "item": instance, "images":images, 'seo': get_seo()})
    except RealEstate.DoesNotExist:
        return render(request, 'user/info.html', {"title": "Помилка", "content": "Нерухомість не знайдено", 'seo': get_seo()})
