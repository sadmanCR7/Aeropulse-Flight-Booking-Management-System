# flight_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Core pages
    path('', views.home_page, name='home_page'),
    path('search/', views.search_results, name='search_results'),

    # OLD Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # NEW Multi-Step Registration URLs (These replace the old 'register' path)
    path('register/', views.register_step1, name='register_step1'),
    path('register/step-2/', views.register_step2, name='register_step2'),
    path('register/step-3/', views.register_step3, name='register_step3'),
    path('register/photo-upload/', views.register_step4_photo, name='register_step4_photo'),

    # Passenger authenticated pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.profile_update_view, name='profile_update'),

    # Booking and related pages
    path('book/<int:flight_id>/', views.book_flight_view, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('payment/success/<int:booking_id>/', views.payment_success_view, name='payment_success'),
    path('booking/ticket/<int:ticket_id>/', views.view_ticket_view, name='view_ticket'),
    path('booking/invoice/<int:invoice_id>/', views.view_invoice_view, name='view_invoice'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),

    # Review pages
    path('flight/<int:flight_id>/', views.flight_detail_view, name='flight_detail'),
    path('flight/<int:flight_id>/review/', views.add_review_view, name='add_review'),
    path('explorer/results/', views.explorer_results_view, name='explorer_results'),
    path('explorer/results/', views.explorer_results_view, name='explorer_results'),
    path('api/price-map/', views.price_map_api_view, name='price_map_api'),
    path('price-map/', views.price_map_view, name='price_map_view'),

]