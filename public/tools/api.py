from django.http import JsonResponse
from django.core.paginator import Paginator
from public.models import RealEstate, Region, City, RealEstateImage
from django.templatetags.static import static
from django.urls import reverse


def upload_image(request):
    if 'image' in request.FILES:
        img = RealEstateImage(image=request.FILES.get('image'))
        img.save()
        response = {'id': img.pk, 'image': img.image.url}
        return JsonResponse({'type': 'success', 'data': response})
    return JsonResponse({'message': "no image", 'type': 'error'})


def delete_image(request):
    RealEstateImage.objects.get(id=request.POST.get('id')).delete()
    return JsonResponse({'message':'ok'})


def phone_check(request):
    try:
        instance = RealEstate.objects.get(pk=request.POST.get('id'))
        instance.viewed_phone += 1
        instance.save()
        return JsonResponse({'message':"ok"})
    except RealEstate.DoesNotExist:
        return JsonResponse({})


def get_regions(request):
    regions = Region.objects.values()
    return JsonResponse(list(regions), safe=False)


def get_cities(request):
    cities = City.objects.filter(region=request.GET.get('reg', '')).values()
    return JsonResponse(list(cities), safe=False)


def get_real_estate(request):
    response = dict()

    def set_if_not_none(mapping, key, value):
        if value:
            mapping[key] = value

    def queryset_to_dict(query):
        return {
            "url": reverse('real-estate', args=(query.pk,)),
            "price": query.price,
            "thumbnail": query.thumbnail.url if query.thumbnail else static('public/img/empty.jpeg'),
            "type_real_estate": query.type_real_estate,
            "city": query.city,
            "rooms": query.rooms,
            "name": query.name,
            "service_type": query.service_type,
            "count_photos": RealEstateImage.objects.filter(real_estate=query.pk).count(),
            "user_logo": query.user.profile.avatar.url if query.user.profile.avatar else static('user/img/avatar.webp'),
            "user_full_name": " ".join([query.user.first_name, query.user.last_name])
        }

    sort_params = dict()
    sort_service_type = request.GET.get('service_type')
    sort_type_real_estate = request.GET.get('type_real_estate')
    sort_p_min = request.GET.get('price_min')
    sort_p_max = request.GET.get('price_max')
    sort_rooms = request.GET.get('rooms')
    sort_region = request.GET.get('region')
    sort_city = request.GET.get('city')

    set_if_not_none(sort_params, 'service_type', sort_service_type)
    set_if_not_none(sort_params, 'type_real_estate', sort_type_real_estate)

    real_estates = RealEstate.objects.filter(**sort_params)

    if sort_p_min and sort_p_max:
        real_estates = real_estates.filter(price__gte=sort_p_min, price__lte=sort_p_max)
    elif sort_p_min:
        real_estates = real_estates.filter(price__gte=sort_p_min)
    elif sort_p_max:
        real_estates = real_estates.filter(price__lte=sort_p_max)

    if sort_rooms:
        sort_rooms = int(sort_rooms)
        if sort_rooms == 3:
            real_estates = real_estates.filter(rooms__gte=sort_rooms)
        else:
            real_estates = real_estates.filter(rooms=sort_rooms)

    if sort_region:
        real_estates = real_estates.filter(region_code=sort_region)
    if sort_city:
        real_estates = real_estates.filter(city_code=sort_city)

    paginator = Paginator(real_estates, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response['has_previous'] = page_obj.has_previous()
    response['has_next'] = page_obj.has_next()
    response['count_pages'] = paginator.num_pages
    response['now_page'] = page_obj.number
    response['data'] = [queryset_to_dict(item) for item in page_obj.object_list]
    return JsonResponse(response)

