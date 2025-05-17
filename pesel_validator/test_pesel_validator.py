import unittest
from pesel_validator import PeselValidator

class TestPeselValidator(unittest.TestCase):
    def test_pesel_format(self):
        self.assertTrue(PeselValidator.validate_format("44051404359"))
        self.assertFalse(PeselValidator.validate_format("123456"))
        self.assertFalse(PeselValidator.validate_format("abcd1234567"))
        self.assertFalse(PeselValidator.validate_format("123456789012"))

    def test_check_digit(self):
        self.assertTrue(PeselValidator.validate_check_digit("44051401359"))
        self.assertFalse(PeselValidator.validate_check_digit("44051401358"))
        self.assertFalse(PeselValidator.validate_check_digit("12345678901"))

    def test_birth_date(self):
        self.assertTrue(PeselValidator.validate_birth_date("25040616213"))
        self.assertFalse(PeselValidator.validate_birth_date("99023012345"))

    def test_gender(self):
        pesel_male = "44051401359"
        pesel_female = "44051401244"
        self.assertEqual(PeselValidator.get_gender(pesel_male), "Mężczyzna")
        self.assertEqual(PeselValidator.get_gender(pesel_female), "Kobieta")

    def test_is_valid(self):
        valid_pesel = "44051401359"
        invalid_pesel = "44051401358"

        self.assertTrue(PeselValidator.is_valid(valid_pesel))
        self.assertFalse(PeselValidator.is_valid(invalid_pesel))
        self.assertFalse(PeselValidator.is_valid("123456"))
        self.assertFalse(PeselValidator.is_valid("abcd1234567"))

    def test_edge_cases(self):
        self.assertTrue(PeselValidator.validate_birth_date("00222901325"))
        self.assertTrue(PeselValidator.validate_birth_date("04222901325"))
        self.assertTrue(PeselValidator.validate_birth_date("18210112345"))
        self.assertTrue(PeselValidator.validate_birth_date("99210112345"))

if __name__ == "__main__":
    unittest.main()