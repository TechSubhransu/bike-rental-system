from rest_framework import serializers
from .models import  Profile
from renter.models import Bike, Booking

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'pno', 'profile_pic']
        
class BookingSerializer(serializers.ModelSerializer):
    bike_name = serializers.StringRelatedField()   # will use Bike.__str__()
    username = serializers.StringRelatedField()    # will use User.__str__()    
    bike_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'bike_name', 'bike_details', 'username', 'pickup_date', 'pickup_time', 'drop_date', 'drop_time', 'status']
        
    def get_bike_details(self, obj):
        return {
            'company': obj.bike_name.company.company,
            'bike_name': obj.bike_name.bike_name,
            'desc': obj.bike_name.desc,
            'photo': obj.bike_name.photo.url if obj.bike_name.photo else None,
            'price': obj.bike_name.price,
            'rating': obj.bike_name.rating,
            'is_available': obj.bike_name.is_available,
            'category': obj.bike_name.category,
            'bookings_count': obj.bike_name.bookings_count,
        }