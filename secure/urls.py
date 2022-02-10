from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('me/', views.me),
    path('csrf-refresh/', views.csrf_refresh),
    path('change-password/',  views.change_password),
    path('login/options/', views.options),
]
