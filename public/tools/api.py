from django.http import JsonResponse
from django.core.paginator import Paginator
from public.models import RealEstate
from django.templatetags.static import static
from django.urls import reverse


def get_real_estate(request):
    response = dict()

    def queryset_to_dict(query):
        return {
            "url": reverse('real-estate', args=(query.pk,)),
            "price": query.price,
            "thumbnail": query.thumbnail.url if query.thumbnail else static('public/img/empty.jpeg'),
            "type_real_estate": query.type_real_estate,
            "city": query.city
        }

    real_estates = RealEstate.objects.all()
    paginator = Paginator(real_estates, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response['has_previous'] = page_obj.has_previous()
    response['has_next'] = page_obj.has_next()
    response['count_pages'] = paginator.num_pages
    response['now_page'] = page_obj.number
    response['data'] = [queryset_to_dict(item) for item in page_obj.object_list]
    return JsonResponse(response)
