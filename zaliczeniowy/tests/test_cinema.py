"""
tests/test_cinema.py
~~~~~~~~~~~~~~~~~~~~

Comprehensive unit‑tests for `src.cinema` covering:

* hall validation & management
* seat reservation logic (positive and negative paths)
* persistence round‑trip (`save` → `load`)
* a variety of assertions and parametrisation (PEP 8 compliant)
"""

import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from src.cinema import Cinema, Hall
from src.exceptions import ReservationError, ValidationError
from src.film import Film, ScreeningTime


def base_time():
    """Helper function to create a base datetime for testing."""
    return datetime.now() + timedelta(days=1)


def hall() -> Hall:
    """Return a test hall with 100 seats."""
    return Hall(number=1, capacity=100)


def cinema() -> Cinema:
    """Return a cinema with one test hall."""
    return Cinema("Test Cinema", halls=[hall()])


def film():
    """Helper function to create a test film."""
    return Film("Test Film", 120, "PG-13")


def screening():
    """Helper function to create a test screening."""
    return ScreeningTime(start=base_time(), hall=1)


class TestHall(unittest.TestCase):
    """Test cases for Hall class."""

    def test_hall_creation(self):
        """Test that hall is created with correct attributes."""
        h = Hall(number=1, capacity=100)
        self.assertEqual(h.number, 1)
        self.assertEqual(h.capacity, 100)
        self.assertEqual(h.available_seats, 100)

    def test_hall_negative_capacity(self):
        """Test that hall creation fails with negative capacity."""
        with self.assertRaises(ValidationError):
            Hall(number=1, capacity=-1)

    def test_hall_zero_capacity(self):
        """Test that hall creation fails with zero capacity."""
        with self.assertRaises(ValidationError):
            Hall(number=1, capacity=0)

    def test_hall_reserve_seats(self):
        """Test that seats can be reserved."""
        h = Hall(number=1, capacity=100)
        h.reserve_seats(50)
        self.assertEqual(h.available_seats, 50)

    def test_hall_reserve_too_many_seats(self):
        """Test that reserving too many seats raises error."""
        h = Hall(number=1, capacity=100)
        with self.assertRaises(ReservationError):
            h.reserve_seats(150)

    def test_hall_cancel_reservation(self):
        """Test that reservation can be cancelled."""
        h = Hall(number=1, capacity=100)
        h.reserve_seats(50)
        h.cancel_reservation(30)
        self.assertEqual(h.available_seats, 80)

    def test_hall_cancel_too_many_seats(self):
        """Test that cancelling too many seats raises error."""
        h = Hall(number=1, capacity=100)
        h.reserve_seats(50)
        with self.assertRaises(ReservationError):
            h.cancel_reservation(70)


class TestCinema(unittest.TestCase):
    """Test cases for Cinema class."""

    def setUp(self):
        """Set up test fixtures."""
        self.c = Cinema("Test Cinema")
        self.h = Hall(number=1, capacity=100)
        self.c.add_hall(self.h)
        self.f = Film("Test Film", 120, "PG-13")
        self.s = ScreeningTime(
            start=datetime.now() + timedelta(hours=1),
            hall=1
        )
        self.f.add_screening(self.s)

    def test_cinema_creation(self):
        """Test that cinema is created with correct attributes."""
        self.assertEqual(self.c.name, "Test Cinema")
        self.assertEqual(len(self.c.halls), 1)

    def test_add_hall(self):
        """Test that hall can be added to cinema."""
        h2 = Hall(number=2, capacity=150)
        self.c.add_hall(h2)
        self.assertEqual(len(self.c.halls), 2)

    def test_add_duplicate_hall(self):
        """Test that adding a duplicate hall number raises error."""
        h = Hall(number=1, capacity=150)
        with self.assertRaises(ValidationError):
            self.c.add_hall(h)

    def test_remove_hall(self):
        """Test that hall can be removed from cinema."""
        self.c.remove_hall(self.h)
        self.assertEqual(len(self.c.halls), 0)

    def test_remove_nonexistent_hall(self):
        """Test that removing nonexistent hall raises error."""
        h = Hall(number=2, capacity=150)
        with self.assertRaises(ValidationError):
            self.c.remove_hall(h)

    def test_reserve_seats(self):
        """Test that seats can be reserved for screening."""
        self.c.reserve(self.f, self.s, seats=50)
        self.assertEqual(self.c.available_seats(self.s), 50)

    def test_reserve_negative_seats(self):
        """Test that reserving negative seats raises error."""
        with self.assertRaises(ValidationError):
            self.c.reserve(self.f, self.s, seats=-1)

    def test_reserve_zero_seats(self):
        """Test that reserving zero seats raises error."""
        with self.assertRaises(ValidationError):
            self.c.reserve(self.f, self.s, seats=0)

    def test_reserve_too_many_seats(self):
        """Test that reserving too many seats raises error."""
        with self.assertRaises(ReservationError):
            self.c.reserve(self.f, self.s, seats=150)

    def test_cancel_reservation(self):
        """Test that reservation can be cancelled."""
        self.c.reserve(self.f, self.s, seats=50)
        self.c.cancel_reservation(self.f, self.s, seats=30)
        self.assertEqual(self.c.available_seats(self.s), 80)

    def test_cancel_too_many_seats(self):
        """Test that cancelling too many seats raises error."""
        self.c.reserve(self.f, self.s, seats=50)
        with self.assertRaises(ReservationError):
            self.c.cancel_reservation(self.f, self.s, seats=70)

    def test_available_seats(self):
        """Test that available seats are correctly calculated."""
        self.c.reserve(self.f, self.s, seats=50)
        self.assertEqual(self.c.available_seats(self.s), 50)

    def test_save_and_load(self):
        """Test that cinema data can be saved and loaded."""
        self.c.reserve(self.f, self.s, seats=50)
        self.c.save("test_cinema.json")
        loaded_cinema = Cinema.load("test_cinema.json")
        self.assertEqual(loaded_cinema.name, self.c.name)
        self.assertEqual(len(loaded_cinema.halls), len(self.c.halls))
        self.assertEqual(loaded_cinema.available_seats(self.s), 50)


# Additional tests from test_cinema_extra.py
class TestCinemaExtra(unittest.TestCase):
    def setUp(self):
        self.cinema = Cinema("Test Cinema")
        self.hall = Hall(1, 100)
        self.cinema.add_hall(self.hall)
        self.film = Film("Test Film", 120, "PG-13")
        self.screening = ScreeningTime(start=base_time(), hall=1)
        self.cinema.add_screening(self.film, self.screening)

    def test_hall_capacity_limits(self):
        """Test that hall capacity limits are properly enforced"""
        # Try to reserve more seats than available
        with self.assertRaises(ReservationError):
            self.cinema.reserve(self.film, self.screening, 101)

    def test_multiple_hall_management(self):
        """Test managing multiple halls simultaneously"""
        hall2 = Hall(2, 50)
        self.cinema.add_hall(hall2)
        self.assertEqual(len(self.cinema.halls), 2)
        self.assertEqual(self.cinema.hall(2).capacity, 50)

    def test_hall_removal(self):
        """Test removing a hall from the cinema"""
        self.cinema.remove_hall(self.hall)
        self.assertEqual(len(self.cinema.halls), 0)
        with self.assertRaises(KeyError):
            self.cinema.hall(1)


if __name__ == "__main__":
    unittest.main()
