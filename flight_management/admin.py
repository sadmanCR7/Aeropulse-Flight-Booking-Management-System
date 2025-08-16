# flight_management/admin.py
from django.contrib import admin
from .models import (
    Airport, Airline, Flight, PassengerProfile,
    Booking, Payment, Ticket, Invoice, Review, Notification, Cancellation
)

# Customizing how the Flight model is displayed
class FlightAdmin(admin.ModelAdmin):
    # CORRECTED: Uses the new class-based field names
    list_display = (
        'flight_id', 'airline', 'departure_airport', 'destination_airport',
        'departure_time', 'economy_price', 'economy_seats', 'business_price', 'business_seats'
    )
    list_filter = ('airline', 'departure_airport', 'destination_airport')
    search_fields = ('flight_id', 'airline__airline_name')

# Customizing the Booking model display
class BookingAdmin(admin.ModelAdmin):
    # CORRECTED: Uses the new passenger and class detail names
    list_display = (
        'booking_id', 'user', 'flight', 'booking_date', 'status',
        'seat_class', 'num_adults', 'num_children', 'total_fare'
    )
    list_filter = ('status', 'seat_class', 'flight__airline')
    search_fields = ('booking_id', 'user__username', 'flight__flight_id')

# Registering models with their custom admin classes
admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Flight, FlightAdmin)
admin.site.register(PassengerProfile)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(Invoice)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(Cancellation)

# Admin site customization
admin.site.site_header = "AeroPulse Admin Dashboard"
admin.site.site_title = "AeroPulse Admin Portal"
admin.site.index_title = "Welcome to the AeroPulse Administration"