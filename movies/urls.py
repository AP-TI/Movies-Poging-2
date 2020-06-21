from django.urls import path

from . import views

urlpatterns = [path('', views.index, name='index'),
               path('load/', views.loadmovies, name='load'),
               path('search/', views.search, name='search'),
               ]
