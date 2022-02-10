from django.urls import path

from . import views_admin
from . import views


urlpatterns = [
    path('admin/all/', views_admin.all),
    path('admin/create/', views_admin.save),
    path('admin/<int:pk>/', views_admin.detail),
    path('admin/<int:pk>/update/', views_admin.save),
    path('admin/<int:pk>/toggle-active/', views_admin.toggle_active),
    path('admin/<int:pk>/delete/', views_admin.delete),
    path('all/', views.all),
]
