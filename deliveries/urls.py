from django.urls import path

from .views import (
    DeliveryListCreateView,
    FarmerListCreateView,
    PlotListCreateView,
    PriceScheduleView,
)

urlpatterns = [
    path('farmers/', FarmerListCreateView.as_view(), name='farmer-list'),
    path('plots/', PlotListCreateView.as_view(), name='plot-list'),
    path('deliveries/', DeliveryListCreateView.as_view(), name='delivery-list'),
    path('price-schedule/', PriceScheduleView.as_view(), name='price-schedule'),
]
