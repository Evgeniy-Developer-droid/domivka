

def create_real_estate(request, form):
    if form.is_valid() and ('thumbnail' in request.FILES):
        instance = form.save()
        instance.refresh_from_db()
        instance.user = request.user
        instance.thumbnail = request.FILES['thumbnail']
        instance.save()
        return {'message': "success", 'type': 'success'}
    print(request.FILES, form.errors)
    return {'message': "Невірні дані", 'type': 'error'}
