from django.urls import path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index),
    path("admin/", admin.site.urls),
    re_path(r"units/(?P<id>\d+)/$", views.UnitListView.as_view(), name="unit-list"),
]
