from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('api/config/', include('config.urls')),
    path('api/auth/', include('secure.urls')),
    path('api/user/', include('user.urls')),
    path('api/doc/', include('doc.urls')),
    path('api/', include('faq.urls')),
    path('api/error500/', include('error500.urls')),
    path('api/language/', include('language.urls')),
    path('api/country/', include('country.urls')),
    path('api/log/', include('log.urls')),
    path('api/nationality/', include('nationality.urls')),
    path('api/visa/person-number/', include('visa.person_number.urls')),
    path('api/visa/document/', include('visa.document.urls')),
    path('api/visa/field/', include('visa.field.urls')),
    path('api/visa/kind/', include('visa.kind.urls')),
    path('api/visa/', include('visa.visa.urls')),
]
