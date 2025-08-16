# flight_management/migrations/0002_populate_initial_data.py

from django.db import migrations


def populate_data(apps, schema_editor):
    Airport = apps.get_model('flight_management', 'Airport')
    Airline = apps.get_model('flight_management', 'Airline')


    airports_data = [
        # North America
        {"airport_code": "JFK", "airport_name": "John F. Kennedy International Airport", "location": "New York, USA"},
        {"airport_code": "LAX", "airport_name": "Los Angeles International Airport", "location": "Los Angeles, USA"},
        {"airport_code": "ORD", "airport_name": "O'Hare International Airport", "location": "Chicago, USA"},
        {"airport_code": "DFW", "airport_name": "Dallas/Fort Worth International Airport", "location": "Dallas, USA"},
        {"airport_code": "ATL", "airport_name": "Hartsfield-Jackson Atlanta International Airport",
         "location": "Atlanta, USA"},
        {"airport_code": "YYZ", "airport_name": "Toronto Pearson International Airport", "location": "Toronto, Canada"},
        {"airport_code": "YVR", "airport_name": "Vancouver International Airport", "location": "Vancouver, Canada"},
        {"airport_code": "MEX", "airport_name": "Mexico City International Airport", "location": "Mexico City, Mexico"},

        # Europe
        {"airport_code": "LHR", "airport_name": "Heathrow Airport", "location": "London, UK"},
        {"airport_code": "CDG", "airport_name": "Charles de Gaulle Airport", "location": "Paris, France"},
        {"airport_code": "AMS", "airport_name": "Amsterdam Airport Schiphol", "location": "Amsterdam, Netherlands"},
        {"airport_code": "FRA", "airport_name": "Frankfurt Airport", "location": "Frankfurt, Germany"},
        {"airport_code": "IST", "airport_name": "Istanbul Airport", "location": "Istanbul, Turkey"},
        {"airport_code": "MAD", "airport_name": "Adolfo Suárez Madrid–Barajas Airport", "location": "Madrid, Spain"},
        {"airport_code": "MUC", "airport_name": "Munich Airport", "location": "Munich, Germany"},
        {"airport_code": "FCO", "airport_name": "Leonardo da Vinci–Fiumicino Airport", "location": "Rome, Italy"},
        {"airport_code": "ZRH", "airport_name": "Zurich Airport", "location": "Zurich, Switzerland"},

        # Asia
        {"airport_code": "DXB", "airport_name": "Dubai International Airport", "location": "Dubai, UAE"},
        {"airport_code": "HND", "airport_name": "Haneda Airport", "location": "Tokyo, Japan"},
        {"airport_code": "NRT", "airport_name": "Narita International Airport", "location": "Tokyo, Japan"},
        {"airport_code": "SIN", "airport_name": "Singapore Changi Airport", "location": "Singapore"},
        {"airport_code": "ICN", "airport_name": "Incheon International Airport", "location": "Seoul, South Korea"},
        {"airport_code": "HKG", "airport_name": "Hong Kong International Airport", "location": "Hong Kong"},
        {"airport_code": "PEK", "airport_name": "Beijing Capital International Airport", "location": "Beijing, China"},
        {"airport_code": "PVG", "airport_name": "Shanghai Pudong International Airport", "location": "Shanghai, China"},
        {"airport_code": "BKK", "airport_name": "Suvarnabhumi Airport", "location": "Bangkok, Thailand"},
        {"airport_code": "KUL", "airport_name": "Kuala Lumpur International Airport",
         "location": "Kuala Lumpur, Malaysia"},
        {"airport_code": "DEL", "airport_name": "Indira Gandhi International Airport", "location": "Delhi, India"},
        {"airport_code": "BOM", "airport_name": "Chhatrapati Shivaji Maharaj International Airport",
         "location": "Mumbai, India"},
        {"airport_code": "DOH", "airport_name": "Hamad International Airport", "location": "Doha, Qatar"},
        {"airport_code": "DAC", "airport_name": "Hazrat Shahjalal International Airport",
         "location": "Dhaka, Bangladesh"},

        # Oceania
        {"airport_code": "SYD", "airport_name": "Sydney Kingsford Smith Airport", "location": "Sydney, Australia"},
        {"airport_code": "MEL", "airport_name": "Melbourne Airport", "location": "Melbourne, Australia"},
        {"airport_code": "AKL", "airport_name": "Auckland Airport", "location": "Auckland, New Zealand"},

        # South America
        {"airport_code": "GRU", "airport_name": "São Paulo/Guarulhos International Airport",
         "location": "São Paulo, Brazil"},
        {"airport_code": "EZE", "airport_name": "Ministro Pistarini International Airport",
         "location": "Buenos Aires, Argentina"},
        {"airport_code": "SCL", "airport_name": "Arturo Merino Benítez International Airport",
         "location": "Santiago, Chile"},

        # Africa
        {"airport_code": "JNB", "airport_name": "O. R. Tambo International Airport",
         "location": "Johannesburg, South Africa"},
        {"airport_code": "CAI", "airport_name": "Cairo International Airport", "location": "Cairo, Egypt"},
        {"airport_code": "ADD", "airport_name": "Bole International Airport", "location": "Addis Ababa, Ethiopia"},
    ]

    # --- UPDATED AND EXPANDED AIRLINE LIST ---
    airlines_data = [
        # Americas
        {"airline_code": "AA", "airline_name": "American Airlines"},
        {"airline_code": "UA", "airline_name": "United Airlines"},
        {"airline_code": "DL", "airline_name": "Delta Air Lines"},
        {"airline_code": "AC", "airline_name": "Air Canada"},

        # Europe
        {"airline_code": "BA", "airline_name": "British Airways"},
        {"airline_code": "AF", "airline_name": "Air France"},
        {"airline_code": "LH", "airline_name": "Lufthansa"},
        {"airline_code": "KL", "airline_name": "KLM Royal Dutch Airlines"},
        {"airline_code": "TK", "airline_name": "Turkish Airlines"},
        {"airline_code": "VS", "airline_name": "Virgin Atlantic"},
        {"airline_code": "IB", "airline_name": "Iberia"},

        # Asia & Oceania
        {"airline_code": "SQ", "airline_name": "Singapore Airlines"},
        {"airline_code": "QF", "airline_name": "Qantas"},
        {"airline_code": "CX", "airline_name": "Cathay Pacific"},
        {"airline_code": "KE", "airline_name": "Korean Air"},
        {"airline_code": "JL", "airline_name": "Japan Airlines"},
        {"airline_code": "AI", "airline_name": "Air India"},
        {"airline_code": "BG", "airline_name": "Biman Bangladesh Airlines"},
        {"airline_code": "MH", "airline_name": "Malaysia Airlines"},
        {"airline_code": "NZ", "airline_name": "Air New Zealand"},
        {"airline_code": "GA", "airline_name": "Garuda Indonesia"},

        # Middle East & Africa
        {"airline_code": "EK", "airline_name": "Emirates"},
        {"airline_code": "QR", "airline_name": "Qatar Airways"},
        {"airline_code": "EY", "airline_name": "Etihad Airways"},
        {"airline_code": "ET", "airline_name": "Ethiopian Airlines"},
    ]

    for data in airports_data:
        Airport.objects.get_or_create(airport_code=data['airport_code'], defaults=data)

    for data in airlines_data:
        Airline.objects.get_or_create(airline_code=data['airline_code'], defaults=data)


class Migration(migrations.Migration):
    dependencies = [
        ('flight_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]