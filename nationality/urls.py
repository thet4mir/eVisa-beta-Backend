from django.urls import path
from . import views


urlpatterns = [
    path('admin/all/', views.all),
    path('admin/create/', views.save),
    path('admin/<int:pk>/update/', views.save),
    path('admin/<int:pk>/toggle-active/', views.toggle_active),
    path('admin/<int:pk>/delete/', views.delete),
]
