from django.urls import path
from . import views_admin


urlpatterns = [
    path('admin/generate/', views_admin.generate),
    path('admin/statistics/', views_admin.statistics),
]
