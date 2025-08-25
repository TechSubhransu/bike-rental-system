from django import forms
from django.contrib.auth.models import User
from customer.models import *
from renter.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        help_texts = {'username': ''}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['username']

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['username', 'bike_name', 'booking_id', 'status']
        widgets = {'pickup_date': DateInput(), 'pickup_time': TimeInput(), 'drop_date': DateInput(), 'drop_time': TimeInput()}