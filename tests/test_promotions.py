import unittest
from datetime import datetime, timedelta

from src.film import Film, ScreeningTime
from src.promotions import CinemaPromotion, ScreeningType, SpecialScreening


def base_time():
    """Helper function to create a base datetime for testing."""
    return datetime.now() + timedelta(days=1)


def film():
    """Helper function to create a test film."""
    return Film("Test Film", 120, "PG-13")


def screening():
    """Helper function to create a test screening."""
    return ScreeningTime(start=base_time(), hall=1)


class TestPromotions(unittest.TestCase):
    """Tests for the Promotions class."""

    def setUp(self):
        self.film = film()
        self.screening = screening()

    def test_special_screening_creation(self):
        """Test creating special screenings with different types."""
        promotion = CinemaPromotion(
            "Test Promotion",
            0.8,
            {},
            datetime.now() + timedelta(days=7))
        self.film.add_screening(self.screening)
        self.film.apply_promotion(self.screening, promotion)
        self.assertEqual(self.film.get_promotion(self.screening), promotion)

    def test_special_screening_invalid_type(self):
        """Test that creating a special screening with invalid type raises ValueError."""
        with self.assertRaises(ValueError):
            SpecialScreening(self.film, self.screening, "INVALID_TYPE", "Opis")

    def test_special_screening_empty_description(self):
        """Test that creating a special screening with empty description raises ValueError."""
        with self.assertRaises(ValueError):
            SpecialScreening(self.film, self.screening, ScreeningType.REGULAR, "")

    def test_promotion_application(self):
        """Test applying promotions to screenings."""
        promotion = CinemaPromotion(
            "Test Promotion",
            0.8,
            {},
            datetime.now() + timedelta(days=7))
        self.film.add_screening(self.screening)
        self.film.apply_promotion(self.screening, promotion)
        self.assertEqual(self.film.get_promotion(self.screening), promotion)

    def test_promotion_removal(self):
        """Test removing promotions from screenings."""
        promotion = CinemaPromotion(
            "Test Promotion",
            0.8,
            {},
            datetime.now() + timedelta(days=7))
        self.film.add_screening(self.screening)
        self.film.apply_promotion(self.screening, promotion)
        self.film.remove_promotion(self.screening)
        self.assertIsNone(self.film.get_promotion(self.screening))

    def test_promotion_expiration(self):
        """Test that expired promotions cannot be applied."""
        promotion = CinemaPromotion(
            "Test Promotion",
            0.8,
            {},
            datetime.now() - timedelta(days=1))
        self.film.add_screening(self.screening)
        with self.assertRaises(ValueError):
            self.film.apply_promotion(self.screening, promotion)

    def test_promotion_duplicate_application(self):
        """Test that a promotion cannot be applied twice to the same screening."""
        promotion = CinemaPromotion(
            "Test Promotion",
            0.8,
            {},
            datetime.now() + timedelta(days=7))
        self.film.add_screening(self.screening)
        self.film.apply_promotion(self.screening, promotion)
        with self.assertRaises(ValueError):
            self.film.apply_promotion(self.screening, promotion)

    def test_promotion_creation(self):
        conditions = {"min_tickets": 2, "max_discount": 0.5}
        expires_at = datetime.now() + timedelta(days=7)
        promo = CinemaPromotion("Weekend Special", 0.2, conditions, expires_at)
        self.assertEqual(promo.name, "Weekend Special")
        self.assertEqual(promo.discount_percent, 0.2)
        self.assertEqual(promo.conditions, conditions)
        self.assertEqual(promo.expires_at, expires_at)

    def test_promotion_application_new(self):
        expires_at = datetime.now() + timedelta(days=7)
        promo = CinemaPromotion("Test Promo", 0.15, {}, expires_at)
        screening_id = "test_screening_1"
        self.assertFalse(promo.is_applied(screening_id))
        promo.apply(screening_id)
        self.assertTrue(promo.is_applied(screening_id))

    def test_promotion_conditions(self):
        conditions = {
            "min_tickets": 2,
            "max_discount": 0.5,
            "valid_days": ["Saturday", "Sunday"]
        }
        expires_at = datetime.now() + timedelta(days=7)
        promo = CinemaPromotion("Weekend Special", 0.2, conditions, expires_at)
        self.assertEqual(promo.conditions["min_tickets"], 2)
        self.assertEqual(promo.conditions["max_discount"], 0.5)
        self.assertTrue("Saturday" in promo.conditions["valid_days"])

    def test_promotion_screening(self):
        film = Film("Test Film", 120, "PG-13")
        screening_time = datetime.now() + timedelta(days=1)
        screening = ScreeningTime(screening_time, 1)
        special = SpecialScreening(film, screening, ScreeningType.REGULAR, "3D")
        expires_at = datetime.now() + timedelta(days=7)
        promo = CinemaPromotion("3D Special", 0.25, {"type": "3D"}, expires_at)
        promo.apply_to_screening(special)
        self.assertTrue(promo.is_applied(special))

    def test_multiple_promotions(self):
        expires_at = datetime.now() + timedelta(days=7)
        promo1 = CinemaPromotion("First Promo", 0.1, {}, expires_at)
        promo2 = CinemaPromotion("Second Promo", 0.2, {}, expires_at)
        screening_id = "test_screening_2"
        promo1.apply(screening_id)
        promo2.apply(screening_id)
        self.assertTrue(promo1.is_applied(screening_id))
        self.assertTrue(promo2.is_applied(screening_id))


if __name__ == "__main__":
    unittest.main()
