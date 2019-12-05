from django.urls import path, include

from . import api

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('api/search', api.search)
]
