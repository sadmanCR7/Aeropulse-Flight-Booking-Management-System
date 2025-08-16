# flight_management/models.py

from django.db import models
from django.contrib.auth.models import User


# --- Airport and Airline models are unchanged ---
class Airport(models.Model):
    airport_code = models.CharField(max_length=3, primary_key=True)
    airport_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self): return f"{self.airport_name} ({self.airport_code})"


class Airline(models.Model):
    airline_code = models.CharField(max_length=5, primary_key=True)
    airline_name = models.CharField(max_length=50)

    def __str__(self): return self.airline_name


# === FLIGHT MODEL: MAJOR UPGRADE ===
class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    # REMOVED: Simple price and seat fields
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # total_seats = models.PositiveIntegerField()
    # seats_available = models.PositiveIntegerField()

    # ADDED: Fields for different classes
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    economy_seats = models.PositiveIntegerField()
    business_price = models.DecimalField(max_digits=10, decimal_places=2)
    business_seats = models.PositiveIntegerField()

    def __str__(
            self): return f"{self.airline.airline_name} - {self.departure_airport.airport_code} to {self.destination_airport.airport_code}"


# === PASSENGER PROFILE MODEL: ADDED GENDER ===
class PassengerProfile(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True,
                                      default='profile_photos/default.png')
    # ADDED: New gender field
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self): return self.user.username


# === BOOKING MODEL: MAJOR UPGRADE ===
class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('PENDING', 'Pending')]
    SEAT_CLASS_CHOICES = [('ECONOMY', 'Economy'), ('BUSINESS', 'Business')]

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, default='PENDING')

    # REMOVED: Simple number_of_tickets field
    # number_of_tickets = models.PositiveIntegerField(default=1)

    # ADDED: Fields for passenger types and class
    seat_class = models.CharField(max_length=10, choices=SEAT_CLASS_CHOICES)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    num_infants = models.PositiveIntegerField(default=0)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    @property
    def total_passengers(self):
        # Infants don't occupy a seat
        return self.num_adults + self.num_children

    def __str__(self): return f"Booking {self.booking_id} by {self.user.username}"


# --- Other models (Payment, Ticket, Invoice, etc.) are unchanged but depend on Booking ---
# We will need to update the logic that creates them later.

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self): return f"Payment {self.payment_id} for Booking {self.booking.booking_id}"


# ... (Ticket, Invoice, Review, Notification, Cancellation models remain structurally the same) ...
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Ticket for Booking {self.booking.booking_id}"


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Invoice {self.invoice_id}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Review by {self.user.username}"


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self): return f"Notification for {self.user.username}"


class Cancellation(models.Model):
    cancellation_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    cancellation_date = models.DateTimeField(auto_now_add=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self): return f"Cancellation for Booking {self.booking.id}"