from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"), 
    path("wiki/<str:entry>/edit", views.edit, name="edit")
]
