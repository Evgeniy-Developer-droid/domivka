import requests
from public.models import Region, City
import copy
import time


def init_e(request):
    url_regions = "https://www.olx.ua/api/v1/geo-encoder/regions/"
    req = requests.get(url_regions, headers={'accept-language':'uk'})
    regions = req.json()['data']
    for region in regions:
        reqion_obj = copy.copy(region)
        reqion_obj.pop('id', None)
        r = Region(**reqion_obj)
        r.save()
        city_r = requests.get("https://www.olx.ua/api/v1/geo-encoder/regions/{}/cities/".format(region['id']),headers={'accept-language':'uk'})
        citys = city_r.json()['data']
        for city in citys:
            city.pop('county', None)
            city.pop('id', None)
            c = City(region=region['normalized_name'], **city)
            c.save()
        time.sleep(1)

    return JsonResponse({})