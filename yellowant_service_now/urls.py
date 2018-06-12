"""yellowant_service_now URL Configuration"""
from django.urls import include, path
from django.contrib import admin


from lib.web import urls as web_urls
from lib.yellowant_api import urls as yellowant_api_urls

urlpatterns = [
    path('', include(yellowant_api_urls)),
    path("accounts/", include('django.contrib.auth.urls')),
    path("admin/", admin.site.urls),
    path('', include(web_urls)),
]
