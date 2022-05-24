from django.http import JsonResponse

from user.models import Profile


def change_user_avatar(request):
    if 'avatar' in request.FILES:
        profile = Profile.objects.get(user=request.user.pk)
        profile.avatar = request.FILES.get('avatar')
        profile.save()
        response = {'avatar': profile.avatar.url}
        return JsonResponse({'type': 'success', 'data': response})
    return JsonResponse({'message': "no image", 'type': 'error'})
