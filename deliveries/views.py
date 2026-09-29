from rest_framework import generics

from .models import Delivery, Farmer, Plot, PriceSchedule
from .serializers import (
    DeliverySerializer,
    FarmerSerializer,
    PlotSerializer,
    PriceScheduleSerializer,
)


class FarmerListCreateView(generics.ListCreateAPIView):
    queryset = Farmer.objects.all().order_by('id')
    serializer_class = FarmerSerializer


class PlotListCreateView(generics.ListCreateAPIView):
    serializer_class = PlotSerializer

    def get_queryset(self):
        queryset = Plot.objects.all().order_by('id')
        station = self.request.query_params.get('station')
        if station:
            queryset = queryset.filter(station=station)
        return queryset


class DeliveryListCreateView(generics.ListCreateAPIView):
    """Station feed: newest first, optionally filtered with ?station=..."""
    serializer_class = DeliverySerializer

    def get_queryset(self):
        queryset = Delivery.objects.select_related('plot').order_by('-delivered_at')
        station = self.request.query_params.get('station')
        if station:
            queryset = queryset.filter(plot__station=station)
        return queryset


class PriceScheduleView(generics.ListAPIView):
    queryset = PriceSchedule.objects.all().order_by('season', 'grade')
    serializer_class = PriceScheduleSerializer
    pagination_class = None