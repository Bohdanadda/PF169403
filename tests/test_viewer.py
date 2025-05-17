from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from src.exceptions import ValidationError
from src.film import Film, ScreeningTime
from src.ticket import Ticket, TicketType
from src.viewer import Viewer


def base_time():
    """Helper function to create a base datetime for testing."""
    return datetime(2024, 3, 15, 19, 30)


def film():
    """Helper function to create a test film."""
    return Film("Test Film", 120, "PG-13")


def screening():
    """Helper function to create a test screening."""
    return ScreeningTime(start=base_time(), hall=1)


def ticket(film, screening, price=25.0):
    """Helper function to create a test ticket."""
    return Ticket(
        film=film,
        screening=screening,
        type=TicketType.REGULAR,
        seat_number=1,
        price=price,
        purchase_date=datetime.now()
    )


class TestViewer(unittest.TestCase):
    """Test cases for Viewer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.viewer = Viewer("John Doe", "john@example.com", 25)

    def test_viewer_creation(self):
        """Test that viewer is created with correct attributes."""
        self.assertEqual(self.viewer.name, "John Doe")
        self.assertEqual(self.viewer.email, "john@example.com")
        self.assertEqual(len(self.viewer.reservations), 0)

    def test_viewer_invalid_email(self):
        """Test that viewer creation fails with invalid email."""
        test_cases = [
            {
                "name": "John Doe",
                "email": "invalid-email",
                "expected_error": "Invalid email format"
            },
            {
                "name": "John Doe",
                "email": "missing@domain",
                "expected_error": "Invalid email format"
            },
            {
                "name": "John Doe",
                "email": "@missing-local.com",
                "expected_error": "Invalid email format"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(ValidationError) as context:
                    Viewer(test_case["name"], test_case["email"], 25)
                self.assertIn(
                    test_case["expected_error"], str(
                        context.exception))

    def test_viewer_empty_name(self):
        """Test that viewer creation fails with empty name."""
        with self.assertRaises(ValidationError) as context:
            Viewer("", "john@example.com", 25)
        self.assertIn("Name cannot be empty", str(context.exception))

    def test_add_reservation(self):
        """Test that reservation can be added to viewer."""
        screening_time = datetime.now() + timedelta(hours=1)
        self.viewer.add_reservation(screening_time, 2)
        self.assertEqual(len(self.viewer.reservations), 1)
        self.assertEqual(self.viewer.reservations[screening_time]["seats"], 2)

    def test_add_duplicate_reservation(self):
        """Test that adding duplicate reservation raises error."""
        screening_time = datetime.now() + timedelta(hours=1)
        self.viewer.add_reservation(screening_time, 2)
        with self.assertRaises(ValidationError):
            self.viewer.add_reservation(screening_time, 3)

    def test_add_reservation_past_time(self):
        """Test that adding reservation for past time raises error."""
        screening_time = datetime.now() - timedelta(hours=1)
        with self.assertRaises(ValidationError) as context:
            self.viewer.add_reservation(screening_time, 2)
        self.assertIn(
            "Cannot make reservation for past time", str(
                context.exception))

    def test_add_reservation_negative_seats(self):
        """Test that adding reservation with negative seats raises error."""
        screening_time = datetime.now() + timedelta(hours=1)
        with self.assertRaises(ValidationError) as context:
            self.viewer.add_reservation(screening_time, -2)
        self.assertIn(
            "Number of seats must be positive", str(
                context.exception))

    def test_add_reservation_zero_seats(self):
        """Test that adding reservation with zero seats raises error."""
        screening_time = datetime.now() + timedelta(hours=1)
        with self.assertRaises(ValidationError) as context:
            self.viewer.add_reservation(screening_time, 0)
        self.assertIn(
            "Number of seats must be positive", str(
                context.exception))

    def test_cancel_reservation(self):
        """Test that reservation can be cancelled."""
        screening_time = datetime.now() + timedelta(hours=1)
        self.viewer.add_reservation(screening_time, 2)
        self.viewer.cancel_reservation(screening_time)
        self.assertEqual(len(self.viewer.reservations), 0)

    def test_cancel_nonexistent_reservation(self):
        """Test that cancelling nonexistent reservation raises error."""
        screening_time = datetime.now() + timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.viewer.cancel_reservation(screening_time)

    def test_get_reservation(self):
        """Test that reservation can be retrieved."""
        screening_time = datetime.now() + timedelta(hours=1)
        self.viewer.add_reservation(screening_time, 2)
        reservation = self.viewer.get_reservation(screening_time)
        self.assertEqual(reservation["seats"], 2)

    def test_get_nonexistent_reservation(self):
        """Test that getting nonexistent reservation raises error."""
        screening_time = datetime.now() + timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.viewer.get_reservation(screening_time)


if __name__ == "__main__":
    unittest.main()
