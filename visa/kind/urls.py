from django.urls import path
from . import views_admin
from . import views

urlpatterns = [
    path('all/', views_admin.list),
    path('create/', views_admin.save),
    path('<int:pk>/update/', views_admin.save),
    path('<int:pk>/delete/', views_admin.delete),
    path('<int:pk>/', views_admin.details),
    path('<int:pk>/toggle-active/', views_admin.toggle_active),

    # Public
    path('public/<int:pk>/', views.details),
    path('public/all/', views.list)
]
