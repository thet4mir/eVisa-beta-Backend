from django.urls import path
from . import views


urlpatterns = [
    path('all/',  views.doc_all,     name="doc_all"),
]
