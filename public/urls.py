from django.urls import path
from . import views
from public.tools import api
from user.views import sign_out, sign_in, sign_up


urlpatterns = [
    path('', views.home, name="home"),
    # path('catalog/', views.catalog, name="catalog"),
    path('catalog/', views.catalog_blog, name="catalog"),
    path('real-estate/<int:pk>', views.real_estate, name="real-estate"),
    path('sign-out/', sign_out, name="sign-out"),
    path('sign-in/', sign_in, name="sign-in"),
    path('sign-up/', sign_up, name="sign-up"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('test/', views.test, name="test"),

    path('api/get-real-estates', api.get_real_estate, name="api-get-real-estates"),
    path('api/get-regions', api.get_regions, name="api-get-regions"),
    path('api/get-cities', api.get_cities, name="api-get-cities"),
    path('api/phone-check', api.phone_check, name="api-phone-check"),

    path('api/upload-image', api.upload_image, name="api-upload-image"),
    path('api/delete-image', api.delete_image, name="api-delete-image"),
]
