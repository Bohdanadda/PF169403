from __future__ import annotations

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import src.film as film_module
from src.exceptions import ScheduleConflictError, ValidationError
from src.film import Film, ScreeningTime


def base_time():
    """Helper function to create a base datetime for testing."""
    return datetime.now() + timedelta(days=1)


def film():
    """Helper function to create a test film."""
    return Film("Inception", 120, "PG-13")


class TestFilm(unittest.TestCase):
    """Test cases for Film class."""

    def setUp(self):
        """Set up test fixtures."""
        self.film = Film("Test Film", 120, "PG-13")
        self.screening = ScreeningTime(
            start=datetime.now() + timedelta(hours=1),
            hall=1
        )

    def test_film_creation(self):
        """Test that film is created with correct attributes."""
        self.assertEqual(self.film.title, "Test Film")
        self.assertEqual(self.film.duration, 120)
        self.assertEqual(len(self.film.screenings), 0)

    def test_film_negative_duration(self):
        """Test that film creation fails with negative duration."""
        with self.assertRaises(ValidationError):
            Film("Test Film", -120, "PG-13")

    def test_film_zero_duration(self):
        """Test that film creation fails with zero duration."""
        with self.assertRaises(ValidationError):
            Film("Test Film", 0, "PG-13")

    def test_add_screening(self):
        """Test that screening can be added to film."""
        self.film.add_screening(self.screening)
        self.assertEqual(len(self.film.screenings), 1)
        self.assertIn(self.screening, self.film.screenings)

    def test_add_duplicate_screening(self):
        """Test that adding duplicate screening raises error."""
        self.film.add_screening(self.screening)
        with self.assertRaises(ValidationError):
            self.film.add_screening(self.screening)

    def test_remove_screening(self):
        """Test that screening can be removed from film."""
        self.film.add_screening(self.screening)
        self.film.remove_screening(self.screening)
        self.assertEqual(len(self.film.screenings), 0)

    def test_remove_nonexistent_screening(self):
        """Test that removing nonexistent screening raises error."""
        with self.assertRaises(ValidationError):
            self.film.remove_screening(self.screening)

    def test_screening_time_validation(self):
        """Test screening time validation."""
        test_cases = [
            {
                "start": datetime.now() - timedelta(hours=1),
                "hall": 1,
                "expected_error": "Screening time must be in the future"
            },
            {
                "start": datetime.now(),
                "hall": 1,
                "expected_error": "Screening time must be in the future"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(ValidationError) as context:
                    ScreeningTime(
                        start=test_case["start"],
                        hall=test_case["hall"]
                    )
                self.assertIn(
                    test_case["expected_error"], str(
                        context.exception))

    def test_screening_hall_validation(self):
        """Test screening hall validation."""
        test_cases = [
            {
                "start": datetime.now() + timedelta(hours=1),
                "hall": -1,
                "expected_error": "Hall number must be positive"
            },
            {
                "start": datetime.now() + timedelta(hours=1),
                "hall": 0,
                "expected_error": "Hall number must be positive"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(ValidationError) as context:
                    ScreeningTime(
                        start=test_case["start"],
                        hall=test_case["hall"]
                    )
                self.assertIn(
                    test_case["expected_error"], str(
                        context.exception))

    def test_add_screening_back_to_back_same_hall_no_conflict(self):
        """Screenings that start exactly at the previous one's end in the same hall are allowed."""
        first = ScreeningTime(start=base_time(), hall=1)
        second = ScreeningTime(
            start=base_time() +
            timedelta(
                minutes=self.film.duration),
            hall=1)
        self.film.add_screening(first)
        # Should not raise ScheduleConflictError
        self.film.add_screening(second)

    def test_add_screening_overlap_same_hall(self):
        """Test that adding overlapping screenings in the same hall raises ScheduleConflictError."""
        first = ScreeningTime(start=base_time(), hall=1)
        second = ScreeningTime(
            start=base_time() +
            timedelta(
                minutes=60),
            hall=1)
        self.film.add_screening(first)
        with self.assertRaises(ScheduleConflictError):
            self.film.add_screening(second)

    def test_upcoming_screenings(self):
        """Test filtering screenings by start time."""
        future1 = ScreeningTime(start=base_time() + timedelta(hours=1), hall=1)
        future2 = ScreeningTime(start=base_time() + timedelta(days=1), hall=1)
        self.film.add_screening(future1)
        self.film.add_screening(future2)
        upcoming = self.film.upcoming_screenings(base_time())
        self.assertEqual(len(upcoming), 2)
        self.assertIn(future1, upcoming)
        self.assertIn(future2, upcoming)

    def test_add_screening_conflict_same_hall(self) -> None:
        f = film()
        first = ScreeningTime(start=base_time(), hall=1)
        f.add_screening(first)

        overlapping = ScreeningTime(
            start=base_time() +
            timedelta(
                minutes=30),
            hall=1)
        with self.assertRaises(ScheduleConflictError):
            f.add_screening(overlapping)

    def test_add_screening_no_conflict_different_hall(self) -> None:
        f = film()
        f.add_screening(ScreeningTime(start=base_time(), hall=1))
        second = ScreeningTime(
            start=base_time() +
            timedelta(
                minutes=30),
            hall=2)
        f.add_screening(second)

        self.assertIn(second, f.screenings)
        self.assertEqual(len(f.screenings), 2)

    def test_upcoming_screenings_filters_past(self) -> None:
        f = film()
        future1 = ScreeningTime(start=base_time() + timedelta(hours=1), hall=1)
        future2 = ScreeningTime(start=base_time() + timedelta(days=1), hall=1)
        f.add_screening(future1)
        f.add_screening(future2)

        upcoming = f.upcoming_screenings(now=base_time())

        self.assertIsInstance(upcoming, list)
        self.assertIn(future1, upcoming)
        self.assertIn(future2, upcoming)

    def test_screenings_return_chronological_order(self) -> None:
        """Screenings should always be returned in chronological order, even if added out of order."""
        f = film()
        later = ScreeningTime(start=base_time() + timedelta(hours=3), hall=1)
        earlier = ScreeningTime(start=base_time(), hall=1)
        f.add_screening(later)
        f.add_screening(earlier)
        self.assertEqual(f.screenings, [earlier, later])

    def test_add_screening_same_time_different_hall_success(self) -> None:
        """Two screenings at the same time but in different halls should not conflict."""
        f = film()
        first = ScreeningTime(start=base_time(), hall=1)
        second = ScreeningTime(start=base_time(), hall=2)
        f.add_screening(first)
        f.add_screening(second)
        self.assertEqual(len(f.screenings), 2)

    def test_upcoming_screenings_default_now(self) -> None:
        """When *now* is omitted, upcoming_screenings should rely on datetime.now()."""
        f = film()
        future1 = ScreeningTime(start=base_time() + timedelta(hours=1), hall=1)
        future2 = ScreeningTime(start=base_time() + timedelta(days=1), hall=1)
        f.add_screening(future1)
        f.add_screening(future2)

        with patch('src.film.datetime') as mock_datetime:
            mock_datetime.now.return_value = base_time()
            upcoming = f.upcoming_screenings()
            self.assertIn(future1, upcoming)
            self.assertIn(future2, upcoming)

    def test_remove_screening_twice_raises(self) -> None:
        """Removing the same screening twice should raise ValidationError the second time."""
        f = film()
        s = ScreeningTime(start=base_time(), hall=1)
        f.add_screening(s)
        f.remove_screening(s)

        with self.assertRaises(ValidationError):
            f.remove_screening(s)

    def test_screening_overlap_different_durations(self) -> None:
        """Test that screenings with different durations do not overlap incorrectly."""
        f = film()
        first = ScreeningTime(start=base_time(), hall=1)
        second = ScreeningTime(
            start=base_time() +
            timedelta(
                minutes=90),
            hall=1)
        f.add_screening(first)
        with self.assertRaises(ScheduleConflictError):
            f.add_screening(second)

    def test_adding_multiple_screenings(self) -> None:
        """Test adding multiple screenings in different orders maintains chronological order."""
        f = film()
        first = ScreeningTime(start=base_time(), hall=1)
        second = ScreeningTime(start=base_time() + timedelta(hours=2), hall=1)
        third = ScreeningTime(
            start=base_time() +
            timedelta(
                hours=4,
                minutes=30),
            hall=1)
        f.add_screening(second)
        f.add_screening(first)
        f.add_screening(third)
        self.assertEqual(f.screenings, [first, second, third])


# Additional tests from test_film_extra.py
class TestFilmExtra(unittest.TestCase):
    def setUp(self):
        self.film = Film("Test Film", 120, "PG-13")
        self.screening = ScreeningTime(start=base_time(), hall=1)

    def test_film_rating_validation(self):
        """Test that film ratings are properly validated"""
        with self.assertRaises(ValidationError):
            Film("Invalid Film", 120, "INVALID_RATING")
        with self.assertRaises(ValidationError):
            Film("Invalid Film", 120, None)
        with self.assertRaises(ValidationError):
            Film("Invalid Film", 120, "")

    def test_screening_time_validation(self):
        """Test that screening times are properly validated"""
        with self.assertRaises(ValidationError):
            ScreeningTime(start=datetime.now() - timedelta(days=1), hall=1)
        with self.assertRaises(ValidationError):
            ScreeningTime(start=datetime.now(), hall=1)

    def test_film_duration_limits(self):
        """Test that film duration has reasonable limits"""
        with self.assertRaises(ValidationError):
            Film("Too Long Film", 1000, "PG-13")  # Film dłuższy niż 16 godzin
        with self.assertRaises(ValidationError):
            Film("Too Short Film", 0, "PG-13")    # Film o zerowej długości
        with self.assertRaises(ValidationError):
            Film("Negative Film", -120, "PG-13")  # Film o ujemnej długości


if __name__ == "__main__":
    unittest.main()
