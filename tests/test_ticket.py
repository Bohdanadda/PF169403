import unittest
from datetime import datetime, timedelta

from src.exceptions import ValidationError
from src.film import Film, ScreeningTime
from src.ticket import Ticket, TicketType


def base_time():
    """Helper function to create a base datetime for testing."""
    return datetime.now() + timedelta(days=1)


def film():
    """Helper function to create a test film."""
    return Film("Test Film", 120, "PG-13")


def screening():
    """Helper function to create a test screening."""
    return ScreeningTime(start=base_time(), hall=1)


class TestTicket(unittest.TestCase):
    """Tests for the Ticket class."""

    def setUp(self):
        self.film = film()
        self.screening = screening()
        self.purchase_date = datetime.now()
        self.base_price = 25.0

    def test_ticket_creation(self):
        """Test creating a valid ticket."""
        ticket = Ticket(
            film=self.film,
            screening=self.screening,
            type=TicketType.REGULAR,
            seat_number=1,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        self.assertEqual(ticket.film, self.film)
        self.assertEqual(ticket.screening, self.screening)
        self.assertEqual(ticket.type, TicketType.REGULAR)
        self.assertEqual(ticket.seat_number, 1)
        self.assertEqual(ticket.price, self.base_price)
        self.assertEqual(ticket.purchase_date, self.purchase_date)

    def test_ticket_invalid_seat(self):
        """Test that creating a ticket with invalid seat number raises ValueError."""
        with self.assertRaises(ValueError):
            Ticket(
                film=self.film,
                screening=self.screening,
                type=TicketType.REGULAR,
                seat_number=0,
                price=self.base_price,
                purchase_date=self.purchase_date
            )

    def test_ticket_invalid_price(self):
        """Test that creating a ticket with invalid price raises ValueError."""
        with self.assertRaises(ValueError):
            Ticket(
                film=self.film,
                screening=self.screening,
                type=TicketType.REGULAR,
                seat_number=1,
                price=-10.0,
                purchase_date=self.purchase_date
            )

    def test_ticket_validity(self):
        """Test ticket validity check."""
        # Future screening - valid ticket
        future_screening = ScreeningTime(
            start=datetime.now() + timedelta(days=1),
            hall=1
        )
        valid_ticket = Ticket(
            film=self.film,
            screening=future_screening,
            type=TicketType.REGULAR,
            seat_number=1,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        self.assertTrue(valid_ticket.is_valid)

        # Past screening - invalid ticket
        with self.assertRaises(ValidationError):
            ScreeningTime(
                start=datetime.now() - timedelta(days=1),
                hall=1
            )

    def test_ticket_price_calculation(self):
        """Test ticket price calculation with different ticket types."""
        # Regular ticket
        regular_ticket = Ticket(
            film=self.film,
            screening=self.screening,
            type=TicketType.REGULAR,
            seat_number=1,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        self.assertEqual(
            regular_ticket.calculate_final_price(
                self.base_price), 25.0)

        # Student ticket
        student_ticket = Ticket(
            film=self.film,
            screening=self.screening,
            type=TicketType.STUDENT,
            seat_number=2,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        self.assertEqual(
            student_ticket.calculate_final_price(
                self.base_price), 20.0)

        # VIP ticket
        vip_ticket = Ticket(
            film=self.film,
            screening=self.screening,
            type=TicketType.VIP,
            seat_number=3,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        self.assertEqual(
            vip_ticket.calculate_final_price(
                self.base_price), 37.5)

    def test_ticket_string_representation(self):
        """Test ticket string representation."""
        ticket = Ticket(
            film=self.film,
            screening=self.screening,
            type=TicketType.REGULAR,
            seat_number=1,
            price=self.base_price,
            purchase_date=self.purchase_date
        )
        expected_str = (
            f"Ticket for {self.film.title} at {self.screening.start.strftime('%Y-%m-%d %H:%M')}\n"
            f"Type: REGULAR\n"
            f"Seat: 1\n"
            f"Price: {self.base_price:.2f}\n"
            f"Purchased: {self.purchase_date.strftime('%Y-%m-%d %H:%M')}"
        )
        self.assertEqual(str(ticket), expected_str)


if __name__ == "__main__":
    unittest.main()
