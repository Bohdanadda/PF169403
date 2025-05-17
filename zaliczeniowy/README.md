# System Zarządzania Kinem

System do zarządzania kinem, który umożliwia zarządzanie seansami, rezerwacjami, biletami i płatnościami.

## Funkcjonalności

### Zarządzanie Filmami
- Dodawanie i usuwanie filmów
- Walidacja danych filmu (tytuł, czas trwania, rating)
- Zarządzanie seansami filmowymi
- Sprawdzanie konfliktów w harmonogramie seansów

### Zarządzanie Salami
- Dodawanie i usuwanie sal kinowych
- Zarządzanie miejscami w salach
- Rezerwacja miejsc na seanse

### System Rezerwacji
- Rezerwacja miejsc na seanse
- Anulowanie rezerwacji
- Sprawdzanie dostępności miejsc

### System Biletów
- Różne typy biletów (regularny, studencki, VIP)
- Walidacja biletów
- Historia zakupów

### System Płatności
- Obsługa różnych metod płatności (karta, gotówka, przelew)
- Walidacja kwot płatności
- Obsługa promocji i zniżek

### System Widzów
- Zarządzanie danymi widzów
- Historia zakupów
- System lojalnościowy
- Walidacja wieku i ratingów filmów

## Wymagania

- unittest (dołączony w standardowej bibliotece Pythona)

## Uruchomienia

1. Uruchom testy:
```bash
python3 -m unittest discover -s tests
```

## Struktura Projektu

```.
├── src/
│   ├── __init__.py
│   ├── admin.py           # Zarządzanie administracją
│   ├── cinema.py          # Zarządzanie kinem i salami
│   ├── exceptions.py      # Własne wyjątki
│   ├── film.py            # Zarządzanie filmami i seansami
│   ├── json_handler.py    # Obsługa plików JSON
│   ├── loyalty.py         # System lojalnościowy
│   ├── payment.py         # System płatności
│   ├── promotions.py      # Obsługa promocji
│   ├── statistics.py      # Statystyki
│   ├── ticket.py          # System biletów
│   └── viewer.py          # Zarządzanie widzami
├── tests/
│   ├── test_admin.py
│   ├── test_cinema.py
│   ├── test_edge_json_handling.py
│   ├── test_film.py
│   ├── test_loyalty.py
│   ├── test_payment.py
│   ├── test_promotions.py
│   ├── test_ticket.py
│   └── test_viewer.py
└── README.md
```

## Przykład Użycia

```python
from src.cinema import Cinema, Hall
from src.film import Film, ScreeningTime
from src.viewer import Viewer
from src.ticket import Ticket, TicketType
from datetime import datetime, timedelta

# Tworzenie kina
cinema = Cinema("Multikino")
hall = Hall(number=1, capacity=100)
cinema.add_hall(hall)

# Dodawanie filmu
film = Film("Inception", 120, "PG-13")
screening = ScreeningTime(start=datetime.now() + timedelta(days=1), hall=1)
film.add_screening(screening)

# Rezerwacja miejsc
viewer = Viewer("John Doe", "john@example.com", 25)
cinema.reserve(film, screening, seats=2)

# Zakup biletu
ticket = Ticket(
    film=film,
    screening=screening,
    type=TicketType.REGULAR,
    seat_number=1,
    price=25.0,
    purchase_date=datetime.now()
)
viewer.add_ticket(ticket)
```


Projekt częściowo został stworzony za pomocą CURSOR

