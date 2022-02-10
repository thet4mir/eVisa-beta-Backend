from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    path('admin/all/',                      views_admin.all),
    path('admin/create/',                   views_admin.create),
    path('admin/<int:pk>/toggle-active/',   views_admin.toggle_active),
    path('admin/<int:pk>/set-default/',     views_admin.set_default),
    path('admin/<int:pk>/update/',          views_admin.update),
    path('admin/<int:pk>/',                 views_admin.detail),
    path('admin/<int:pk>/delete/',          views_admin.delete),
    path('all/',                            views.public_all),
]
