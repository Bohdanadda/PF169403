import unittest

from laboratorium1.src.email import Email

class TestValidateEmail(unittest.TestCase):

    def setUp(self):
        self.email = Email()

    def test_valid_emails(self):
        self.assertTrue(self.email.validate_email("169403@student.uwm.edu.pl"))
        self.assertTrue(self.email.validate_email("bogda.andreew05@gmail.com"))

    def test_missing_at_symbol(self):
        self.assertFalse(self.email.validate_email("169403student.uwm.edu.pl"))
        self.assertFalse(self.email.validate_email("bogda.andreew05.gmail.com"))

    def test_missing_domain(self):
        self.assertFalse(self.email.validate_email("@.com"))
        self.assertFalse(self.email.validate_email("user@.com"))

    def test_missing_username(self):
        self.assertFalse(self.email.validate_email("@domain.com"))

    def test_ivalide_characters(self):
        self.assertFalse(self.email.validate_email("user@domail,com"))
        self.assertFalse(self.email.validate_email("@domailcom"))
        self.assertFalse(self.email.validate_email("userdomail.com"))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()