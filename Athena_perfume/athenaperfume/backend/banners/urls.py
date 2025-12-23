from django.urls import path
from .views import BannerListCreateView, BannerDeleteView

urlpatterns = [
    path('', BannerListCreateView.as_view(), name='banner-list-create'),
    path('<int:pk>/', BannerDeleteView.as_view(), name='banner-delete'),
]