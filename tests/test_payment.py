import unittest

from src.exceptions import PaymentError, ValidationError
from src.payment import PaymentProcessor, PaymentType


class TestPaymentProcessor(unittest.TestCase):
    """Test cases for PaymentProcessor class."""

    def test_successful_payment(self):
        """Test successful payment processing."""
        processor = PaymentProcessor(
            payment_type=PaymentType.CARD, amount=100.0)
        result = processor.process_payment()
        self.assertEqual(
            result, "Payment of 100.0 via card processed successfully.")

    def test_invalid_payment_type(self):
        """Test payment with invalid payment type."""
        with self.assertRaises(ValidationError) as context:
            PaymentProcessor(payment_type="invalid", amount=100.0)
        self.assertIn("Invalid payment type", str(context.exception))

    def test_payment_amount_validation(self):
        """Test payment amount validation."""
        test_cases = [
            {
                "amount": -50.0,
                "payment_type": PaymentType.CASH,
                "expected_error": "Amount must be positive"
            },
            {
                "amount": 0.0,
                "payment_type": PaymentType.TRANSFER,
                "expected_error": "Amount must be positive"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(ValidationError) as context:
                    PaymentProcessor(
                        payment_type=test_case["payment_type"],
                        amount=test_case["amount"]
                    )
                self.assertIn(
                    test_case["expected_error"], str(
                        context.exception))

    def test_payment_amount_handling(self):
        """Test handling of different payment amounts."""
        test_cases = [
            {
                "amount": 99.99,
                "payment_type": PaymentType.CARD,
                "description": "decimal amount"
            },
            {
                "amount": 0.01,
                "payment_type": PaymentType.CARD,
                "description": "very small amount"
            },
            {
                "amount": 1000000.0,
                "payment_type": PaymentType.TRANSFER,
                "description": "very large amount"
            },
            {
                "amount": 1e6,
                "payment_type": PaymentType.CARD,
                "description": "scientific notation"
            },
            {
                "amount": 100.999,
                "payment_type": PaymentType.CASH,
                "description": "rounding needed"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["description"]):
                processor = PaymentProcessor(
                    payment_type=test_case["payment_type"],
                    amount=test_case["amount"]
                )
                result = processor.process_payment()
                expected = f"Payment of {
                    test_case['amount']} via {
                    test_case['payment_type'].value} processed successfully."
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
