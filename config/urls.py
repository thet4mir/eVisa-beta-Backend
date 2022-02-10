from django.urls import path
from . import views_admin


urlpatterns = [
    # TODO deprecate these urls
    path('all/', views_admin.all),
    path('save/', views_admin.save),
    path('admin/test-send-mail/', views_admin.test_send_mail),

    path('admin/all/', views_admin.all),
    path('admin/save/', views_admin.save),
    path('admin/test-send-file/', views_admin.test_send_file)
]
