"""
Different URL addresses required
"""
from django.conf.urls import url
#from django.urls import path
from django.urls import path
from django.contrib import admin
from .views import index, userdetails, delete_integration, view_integration
admin.autodiscover()
app_name = 'web'

urlpatterns = [

    path("", index, name="index"),
    path("user/", userdetails, name="userdetails"),
    path("user/<int:id>", delete_integration, name="delete"),
    path("accounts/<int:id>/", view_integration, name="accounts"),
    url(r"^(?P<path>.*)$", index, name="path"),
]
