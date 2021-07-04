"""Explorer-related urls."""
from django.urls import path
from explorer import views
urlpatterns = [
    path('', views.index, name='index-page'),
    path('collections/', views.CollectionListView.as_view(), name='collections'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-view'),
]
