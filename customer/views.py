from django.shortcuts import render
from customer.forms import *
from renter.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
from renter.models import *
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
# Create your views here.


def home(request):
    un = request.session.get('username')
    context = {}

    if un:
        UO = User.objects.get(username=un)
        context['UO'] = UO

    brands = Brand.objects.all()
    bikes = Bike.objects.all()

    # --- Filtering & Sorting ---
    sort = request.GET.get("sort")
    category = request.GET.get("category")
    brand = request.GET.get("brand")

    # Filter by brand
    if brand:
        bikes = Bike.objects.filter(company__company__iexact=brand)

    # Filter by category (make sure Bike model has a category field)
    if category:
        bikes = bikes.filter(category__iexact=category)

    # Sorting
    if sort == "price":
        bikes = bikes.order_by("price")   # ascending price
    elif sort == "availability":
        bikes = bikes.filter(is_available=True)   # assuming you have an availability field
    elif sort == "popularity":
        bikes = bikes.order_by("-bookings_count")  # assuming you track bookings

    # Pagination (12 bikes per page)
    paginator = Paginator(bikes, 12)
    page_number = request.GET.get("page")
    bikes = paginator.get_page(page_number)

    # Pass data to template
    context['brands'] = brands
    context['bikes'] = bikes

    return render(request, 'customer/home.html', context)



def register(request):
    EUFO = UserForm()
    ECFO = ProfileForm()
    d = {'EUFO': EUFO, 'ECFO': ECFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        CFDO = ProfileForm(request.POST,request.FILES)


        if UFDO.is_valid() and CFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MCFDO = CFDO.save(commit=False)
            MCFDO.username = MUFDO
            MUFDO.save()
            MCFDO.save()
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Data')
    return render(request, 'customer/register.html', d)


def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO.is_staff:
            return HttpResponse('Invalid creds')
        elif AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'customer/user_login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def forgetpw(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        UO = User.objects.get(username=un)
        if UO:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['username'] = un
            print(otp)
            return HttpResponseRedirect(reverse('otp'))
    return render(request, 'customer/forgetpw.html')


def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(otp) == gotp:
            return HttpResponseRedirect(reverse('newpw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'customer/otp.html')


def newpw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            if UO:
                UO.set_password(pw)
                UO.save()
                return HttpResponseRedirect(reverse('user_login'))
            return HttpResponse('Session expired')         
        return HttpResponse("Password doesn't Match")      
    return render(request, 'customer/newpw.html') 


def changepw(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    if UO:
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['username'] = un
        print(otp)
        return HttpResponseRedirect(reverse('otp'))
    

def display_profile(request):
   un = request.session.get('username')
   UO = User.objects.get(username=un)
   PO = Profile.objects.get(username=UO)
   d = {'UO': UO, 'PO': PO}
   return render(request, 'customer/display_profile.html', d)

def display(request, brand):
    bikes = Bike.objects.filter(company=brand)
    d = {'bikes': bikes, 'brand': brand}
    return render(request, 'customer/home.html', d)

def book(request, pk):
    un = request.session.get('username')
    if un:
        bike = Bike.objects.get(pk=pk)
        EBFO = BookingForm()
        d = {'bike': bike, 'EBFO': EBFO}
        if request.method == 'POST':
            BFDO = BookingForm(request.POST)
            UO = User.objects.get(username=un)
            BO = Bike.objects.get(pk=pk)
            bookings = Booking.objects.filter(bike_name=BO)
            for booking in bookings:
                if str(booking.pickup_date) == request.POST.get('pickup_date'):
                    return render(request, 'customer/not_avail.html')
            MBFDO = BFDO.save(commit=False)
            MBFDO.username = UO
            MBFDO.bike_name=bike
            MBFDO.save()
            return render(request, 'customer/conf.html')
        return render(request, 'customer/book.html', d)
    return HttpResponseRedirect(reverse('user_login'))

def search(request):
    if request.method == 'POST':
        bike = request.POST.get('srch')
        BO = Bike.objects.get(bike_name=bike)
        d = {'BO': BO}
        return render(request, 'customer/display.html', d)   
    
def show(request, pk):
    BO = Bike.objects.get(pk=pk)
    d = {'BO': BO}
    return render(request, 'customer/display.html', d)   

def my_bookings(request):
    un =  request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        bookings = Booking.objects.filter(username=UO)
        d = {'bookings': bookings}
        return render(request, 'customer/my_bookings.html', d)
    return HttpResponse('Invalid User')

def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "conf.html", {"booking": booking})