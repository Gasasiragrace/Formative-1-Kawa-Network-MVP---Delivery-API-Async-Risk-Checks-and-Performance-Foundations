from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Delivery, Farmer, Plot
from .serializers import DeliverySerializer, FarmerSerializer, PlotSerializer


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