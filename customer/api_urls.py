from django.urls import path
from customer.views import BookingList, BookingDetail, ProfileDetail

urlpatterns = [
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingDetail.as_view(), name='booking-detail'),
    path('profile/<str:username>/', ProfileDetail.as_view(), name='profile-detail'),
]
