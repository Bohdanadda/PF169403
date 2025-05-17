from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.exceptions import PaymentError, ValidationError


class PaymentType(Enum):
    """Types of payment accepted by the cinema."""
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"


class PaymentProcessor:
    """Handles payment processing for the cinema."""

    def __init__(self, payment_type: PaymentType, amount: float):
        """Initialize a payment processor.

        Args:
            payment_type: The type of payment to process
            amount: The amount to process

        Raises:
            ValidationError: If the payment type is invalid or amount is not positive
        """
        if not isinstance(payment_type, PaymentType):
            raise ValidationError("Invalid payment type")
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        self.payment_type = payment_type
        self.amount = amount

    def process_payment(self) -> str:
        """Process the payment.

        Returns:
            A message indicating the payment was successful

        Raises:
            PaymentError: If the payment processing fails
        """
        try:
            # In a real system, this would integrate with a payment gateway
            return f"Payment of {
                self.amount} via {
                self.payment_type.value} processed successfully."
        except Exception as e:
            raise PaymentError(f"Payment processing failed: {str(e)}")
