from django.urls import path, re_path
from . import views
from .tools import api

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_, name='settings'),
    path('new-real-estate/', views.new_real_estate, name='new-real-estate'),
    path('delete-real-estate/<int:pk>', views.delete_real_estate, name='delete-real-estate'),
    path('update-real-estate/<int:pk>', views.update_real_estate, name='update-real-estate'),
    path('password-reset/', views.password_reset, name="password-reset"),
    path('password-reset/done/', views.password_reset_done, name="password-reset-done"),
    re_path(r'^password-reset/confirm/(?P<uidb64>[\dA-Za-z_\-]+)/(?P<token>[\dA-Za-z]{1,13}-[\dA-Za-z]{1,100})/$',
            views.password_reset_confirm, name="password-reset-confirm"),
    path('password-reset/complete/', views.password_reset_complete, name="password-reset-complete"),
    re_path(r'^activate/(?P<uidb64>[\dA-Za-z_\-]+)/(?P<token>[\dA-Za-z]{1,13}-[\dA-Za-z]{1,100})/$',
            views.activate, name='activate'),

    path('api/change-user-avatar/', api.change_user_avatar, name='api-change-user-avatar'),
]