from django.urls import path
from . import views


urlpatterns = [
    path('create/',                 views.create),
    path('<int:pk>/update/',        views.update),
    path('<int:pk>/remove/',        views.remove),
    path('all/',                    views.all),
    path('<int:pk>/',               views.details),
    path('<int:pk>/toggle-active/', views.toggle_active),
]
