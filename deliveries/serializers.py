from rest_framework import serializers

from .models import Delivery, Farmer, Plot


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'phone_number', 'national_id']


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = ['id', 'farmer', 'sector', 'station', 'risk_status']
        read_only_fields = ['risk_status']

    def validate_sector(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Sector is required.")
        return value

    def validate_station(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Station is required.")
        return value


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'plot', 'weight_kg', 'delivered_at']
        read_only_fields = ['delivered_at']

    def validate_weight_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0.")
        return value