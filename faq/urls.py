from django.urls import path

from . import views
from . import views_admin


patterns_public = [
    path('faq/all/', views.all),
]


patterns_admin = [
    path('faq/admin/all/', views_admin.all),
    path('faq/admin/save-sort/', views_admin.save_sort),
    path('faq/admin/create/', views_admin.save),
    path('faq/admin/<int:pk>/', views_admin.detail),
    path('faq/admin/<int:pk>/update/', views_admin.save),
    path('faq/admin/<int:pk>/toggle-active/', views_admin.toggle_active),
    path('faq/admin/<int:pk>/delete/', views_admin.delete),
]


urlpatterns = patterns_public + patterns_admin
