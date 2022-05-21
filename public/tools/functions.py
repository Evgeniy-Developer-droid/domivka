from public.models import RealEstateImage, SEO


def create_real_estate(request, form):
    if form.is_valid() and ('thumbnail' in request.FILES):
        instance = form.save()
        instance.refresh_from_db()
        instance.user = request.user
        instance.thumbnail = request.FILES['thumbnail']
        instance.save()
        images = [int(v) for k, v in request.POST.items() if k.startswith('img_')]
        image_instances = RealEstateImage.objects.filter(pk__in=images)
        image_instances.update(real_estate=instance)
        return {'message': "success", 'type': 'success'}
    return {'message': "Невірні дані", 'type': 'error'}


def get_seo():
    result = {'keywords': "", 'description': "", 'image': ""}
    instance = SEO.objects.all().first()
    if instance:
        result['keywords'] = instance.keywords
        result['description'] = instance.description
        result['image'] = instance.image.url if instance.image else ""
    return result