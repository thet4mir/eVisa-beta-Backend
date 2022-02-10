from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    path('submit/', views.submit),
    path('admin/list/', views_admin.list),
    path('admin/<int:pk>/', views_admin.details),
    path('admin/<int:pk>/approve/', views_admin.approve),
    path('admin/<int:pk>/decline/', views_admin.decline),
]
