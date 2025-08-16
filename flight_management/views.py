# flight_management/views.py

from decimal import Decimal
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse # Add this import
from django.db.models import Min # Add this import

# Import all models and forms
from .models import (
    Flight, Airport, Booking, Payment, Ticket, Invoice, Cancellation,
    Review, User, PassengerProfile
)
from .forms import (
    ReviewForm, CustomLoginForm, UserUpdateForm, ProfileUpdateForm,
    RegistrationStep1Form, RegistrationStep2Form, RegistrationStep3Form, PhotoUploadForm
)


# === GUEST AND CORE VIEWS ===

def home_page(request):
    airports = Airport.objects.all()
    context = {'airports': airports}
    return render(request, 'home.html', context)


def search_results(request):
    departure_code = request.GET.get('departure_airport')
    destination_code = request.GET.get('destination_airport')
    num_adults = request.GET.get('num_adults', 1)
    num_children = request.GET.get('num_children', 0)
    num_infants = request.GET.get('num_infants', 0)
    seat_class = request.GET.get('seat_class', 'ECONOMY').upper()
    total_passengers = int(num_adults) + int(num_children)

    query = Q()
    if departure_code: query &= Q(departure_airport__airport_code=departure_code)
    if destination_code: query &= Q(destination_airport__airport_code=destination_code)

    flights = Flight.objects.filter(query)

    # Filter flights by seat availability based on class
    if seat_class == 'BUSINESS':
        flights = flights.filter(business_seats__gte=total_passengers)
    else:  # Default to Economy
        flights = flights.filter(economy_seats__gte=total_passengers)

    context = {
        'flights': flights,
        'departure_airport': Airport.objects.get(airport_code=departure_code) if departure_code else None,
        'destination_airport': Airport.objects.get(airport_code=destination_code) if destination_code else None,
        'num_adults': num_adults,
        'num_children': num_children,
        'num_infants': num_infants,
        'seat_class': seat_class,
        'total_passengers': total_passengers,
    }
    return render(request, 'search_results.html', context)


# === AUTHENTICATION AND REGISTRATION VIEWS ===

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('home_page')


def register_step1(request):
    if request.method == 'POST':
        form = RegistrationStep1Form(request.POST)
        if form.is_valid():
            request.session['step1_data'] = form.cleaned_data
            return redirect('register_step2')
    else:
        form = RegistrationStep1Form()
    return render(request, 'register_step1.html', {'form': form})


def register_step2(request):
    if 'step1_data' not in request.session: return redirect('register_step1')
    if request.method == 'POST':
        form = RegistrationStep2Form(request.POST)
        if form.is_valid():
            request.session['step2_data'] = form.cleaned_data
            return redirect('register_step3')
    else:
        form = RegistrationStep2Form()
    return render(request, 'register_step2.html', {'form': form})


def register_step3(request):
    if 'step2_data' not in request.session: return redirect('register_step1')
    if request.method == 'POST':
        form = RegistrationStep3Form(request.POST)
        if form.is_valid():
            step3_data = form.cleaned_data
            step3_data['password'] = make_password(step3_data['password'])
            request.session['step3_data'] = step3_data
            return redirect('register_step4_photo')
    else:
        form = RegistrationStep3Form()
    return render(request, 'register_step3.html', {'form': form})


@transaction.atomic
def register_step4_photo(request):
    if 'step3_data' not in request.session: return redirect('register_step1')
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            step1 = request.session['step1_data']
            step2 = request.session['step2_data']
            step3 = request.session['step3_data']
            user = User.objects.create(
                username=step3['username'], password=step3['password'],
                first_name=step1['first_name'], last_name=step1['last_name'], email=step1['email']
            )
            PassengerProfile.objects.create(
                user=user, phone_number=step2['phone_number'], address=step2['address'],
                gender=step2.get('gender'), profile_photo=form.cleaned_data.get('profile_photo')
            )
            for key in list(request.session.keys()):
                if 'step' in key: del request.session[key]
            login(request, user)
            messages.success(request, 'Registration complete! Welcome to AeroPulse.')
            return redirect('dashboard')
    else:
        form = PhotoUploadForm()
    return render(request, 'register_step4_photo.html', {'form': form})


# === PASSENGER-FOCUSED VIEWS (DASHBOARD, PROFILE, BOOKING) ===

@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    context = {'bookings': bookings}
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'profile_view.html')


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.passengerprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.passengerprofile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'profile_update.html', context)


@login_required
def book_flight_view(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    adults = int(request.GET.get('adults', 1))
    children = int(request.GET.get('children', 0))
    infants = int(request.GET.get('infants', 0))
    seat_class = request.GET.get('class', 'ECONOMY').upper()

    if seat_class == 'BUSINESS':
        price_per_person = flight.business_price
        seats_available = flight.business_seats
    else:
        price_per_person = flight.economy_price
        seats_available = flight.economy_seats

    total_passengers = adults + children
    total_fare = price_per_person * total_passengers

    if request.method == 'POST':
        if seats_available >= total_passengers:
            booking = Booking.objects.create(
                user=request.user, flight=flight, seat_class=seat_class,
                num_adults=adults, num_children=children, num_infants=infants,
                total_fare=total_fare, status='PENDING'
            )
            if seat_class == 'BUSINESS':
                flight.business_seats -= total_passengers
            else:
                flight.economy_seats -= total_passengers
            flight.save()
            messages.success(request, 'Booking created. Please proceed to payment.')
            return redirect('payment', booking_id=booking.pk)
        else:
            messages.error(request, 'Seats are no longer available. Please try another flight.')
            return redirect('home_page')

    context = {
        'flight': flight, 'num_adults': adults, 'num_children': children,
        'num_infants': infants, 'seat_class': seat_class,
        'price_per_person': price_per_person, 'total_fare': total_fare,
    }
    return render(request, 'book_flight.html', context)


@login_required
def payment_view(request, booking_id):
    booking = Booking.objects.get(pk=booking_id, user=request.user)
    total_amount = booking.total_fare
    if request.method == 'POST':
        payment = Payment.objects.create(
            booking=booking, amount=total_amount, method='Credit Card (Simulated)'
        )
        booking.status = 'CONFIRMED'
        booking.save()
        Ticket.objects.create(booking=booking)
        Invoice.objects.create(payment=payment)
        messages.success(request, 'Payment successful! Your flight is confirmed.')
        return redirect('payment_success', booking_id=booking.pk)
    context = {'booking': booking, 'total_amount': total_amount}
    return render(request, 'payment.html', context)


@login_required
def payment_success_view(request, booking_id):
    booking = Booking.objects.get(pk=booking_id, user=request.user)
    context = {'booking': booking}
    return render(request, 'payment_success.html', context)


@login_required
def view_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id, booking__user=request.user)
    context = {'ticket': ticket}
    return render(request, 'ticket.html', context)


@login_required
def view_invoice_view(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id, payment__booking__user=request.user)
    context = {'invoice': invoice}
    return render(request, 'invoice.html', context)


@login_required
def cancel_booking_view(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id, user=request.user)
        if booking.status == 'CONFIRMED':
            flight = booking.flight
            if booking.seat_class == 'BUSINESS':
                flight.business_seats += booking.total_passengers
            else:
                flight.economy_seats += booking.total_passengers
            flight.save()
            booking.status = 'CANCELLED'
            booking.save()
            refund_amount = booking.payment.amount * Decimal('0.90')
            Cancellation.objects.create(booking=booking, refund_amount=refund_amount)
            messages.success(request, 'Your booking has been successfully cancelled.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
    return redirect('dashboard')


def flight_detail_view(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    reviews = Review.objects.filter(flight=flight).order_by('-review_date')
    context = {'flight': flight, 'reviews': reviews}
    return render(request, 'flight_detail.html', context)


@login_required
def add_review_view(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    if not Booking.objects.filter(user=request.user, flight=flight, status='CONFIRMED').exists():
        messages.error(request, "You can only review flights you have taken.")
        return redirect('flight_detail', flight_id=flight.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('flight_detail', flight_id=flight.pk)
    else:
        form = ReviewForm()
    context = {'form': form, 'flight': flight}
    return render(request, 'add_review.html', context)


def explorer_view(request):
    airports = Airport.objects.all()
    context = {'airports': airports}
    return render(request, 'explorer_view.html', context)


def explorer_results_view(request):
    departure_code = request.GET.get('departure_airport')
    max_budget = request.GET.get('max_budget')
    seat_class = request.GET.get('seat_class', 'ECONOMY').upper()

    if not departure_code or not max_budget:
        messages.error(request, 'Please select a departure airport and provide a budget.')
        return redirect('explorer_view')

    base_query = Flight.objects.filter(departure_airport__airport_code=departure_code)
    if seat_class == 'BUSINESS':
        affordable_flights = base_query.filter(business_price__lte=max_budget)
    else:
        affordable_flights = base_query.filter(economy_price__lte=max_budget)

    distinct_destinations = affordable_flights.order_by('destination_airport', 'economy_price').distinct(
        'destination_airport')
    flights_to_show = affordable_flights.filter(pk__in=[flight.pk for flight in distinct_destinations])

    context = {
        'flights': flights_to_show,
        'departure_airport': Airport.objects.get(airport_code=departure_code),
        'max_budget': max_budget,
        'seat_class': seat_class,
    }
    return render(request, 'explorer_results.html', context)


def price_map_view(request):
    airports = Airport.objects.all()
    context = {'airports': airports}
    return render(request, 'price_map.html', context)


def price_map_api_view(request):
    origin_airport_code = request.GET.get('origin')
    if not origin_airport_code:
        return JsonResponse({'error': 'Origin airport code is required.'}, status=400)

    cheapest_flights = Flight.objects.filter(
        departure_airport__airport_code=origin_airport_code
    ).values(
        'destination_airport__location'
    ).annotate(
        min_price=Min('economy_price')
    )

    country_prices = {}
    for flight in cheapest_flights:
        try:
            country = flight['destination_airport__location'].split(',')[-1].strip()
            price = flight['min_price']
            if country not in country_prices or price < country_prices[country]:
                country_prices[country] = price
        except (IndexError, AttributeError):
            continue

    return JsonResponse(country_prices)