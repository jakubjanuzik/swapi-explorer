"""Explorer-related urls."""
from django.urls import path
from explorer import views
urlpatterns = [
    path('', views.index, name='index-page'),
    path('collections', views.index, name='collections'),
]
