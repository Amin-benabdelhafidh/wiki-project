from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newpage", views.newpage, name="newpage"),
    path("RandomPage", views.random, name="random"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("PageNotFound", views.notfound, name='notfound'),
    path("search", views.search, name="search")
    
]
