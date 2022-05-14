from django.urls import path
from . import views
from public.tools import api

urlpatterns = [
    path('', views.home, name="home"),
    path('catalog/', views.catalog, name="catalog"),
    path('real-estate/<int:pk>', views.real_estate, name="real-estate"),

    path('api/get-real-estates', api.get_real_estate, name="api-get-real-estates")
]
