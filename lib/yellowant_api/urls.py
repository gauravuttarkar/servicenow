"""
Different URL paths used.
"""
from django.urls import path

from .views import request_yellowant_oauth_code, yellowant_oauth_redirect, yellowant_api, api_key,service_now_auth\
    ,webhooks


urlpatterns = [
    path("create-new-integration/", request_yellowant_oauth_code, name="request-yellowant-oauth"),
    path("service-now-integration/", request_yellowant_oauth_code, name="request-yellowant-oauth"),
    path("yellowant-oauth-redirect/", yellowant_oauth_redirect, name="yellowant-oauth-redirect"),
    path("yellowant-api/", yellowant_api, name="yellowant-api"),
    path("service-now-auth/", service_now_auth, name="service-now-auth"),
    path("apikey/", api_key, name="yellowant-api"),
    path("webhooks/<str:id>",webhooks,name="webhooks"),
]

