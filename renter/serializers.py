from rest_framework import serializers
from .models import Brand, Bike

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['company']
        
class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['company', 'bike_name', 'desc', 'photo', 'price', 'rating', 'is_available', 'category', 'bookings_count']

