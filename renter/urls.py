from django.urls import path
from renter.views import *

urlpatterns = [
    path('', renter_home, name='renter_home'),
    path('renter_register/', renter_register, name='renter_register'),
    path('renter_login/', renter_login, name='renter_login'),
    path('renter_logout/', renter_logout, name='renter_logout'),
    path('renter_display_profile/',  renter_display_profile, name='renter_display_profile'),
    path('renter_forgetpw/', renter_forgetpw, name='renter_forgetpw'),
    path('renter_otp/', renter_otp, name='renter_otp'),
    path('newpw/', newpw, name='newpw'),
    path('renter_changepw/', renter_changepw, name='renter_changepw'),
    path('renter_display<brand>', renter_display, name='renter_display'),
    path('allbooking/', allbooking, name ='allbooking'),
    path('approve<pk>', approve, name='approve'),
    path('reject<pk>', reject, name='reject'),
    path('add_bikes/', add_bikes, name='add_bikes'),
]
