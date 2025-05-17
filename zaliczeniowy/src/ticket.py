from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .film import Film, ScreeningTime


class TicketType(Enum):
    """Types of tickets with their price multipliers."""
    REGULAR = 1.0
    STUDENT = 0.8
    SENIOR = 0.7
    CHILD = 0.5
    VIP = 1.5


@dataclass(frozen=True)
class Ticket:
    """
    Represents a cinema ticket.

    Fields
    ------
    film: Film
        The film being shown
    screening: ScreeningTime
        The screening time
    type: TicketType
        The type of ticket
    seat_number: int
        The seat number
    price: float
        The ticket price
    purchase_date: datetime
        The date and time when the ticket was purchased
    """
    film: Film
    screening: ScreeningTime
    type: TicketType
    seat_number: int
    price: float
    purchase_date: datetime

    def __post_init__(self) -> None:
        """Validate the ticket data."""
        if not isinstance(self.type, TicketType):
            raise ValueError("type must be a TicketType")
        if not isinstance(self.seat_number, int) or self.seat_number <= 0:
            raise ValueError("seat_number must be a positive integer")
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("price must be a positive number")
        if not isinstance(self.purchase_date, datetime):
            raise ValueError("purchase_date must be a datetime object")

    @property
    def is_valid(self) -> bool:
        """Check if the ticket is still valid (not expired)."""
        return self.screening.start > datetime.now()

    def calculate_final_price(self, base_price: float) -> float:
        """Calculate the final price with ticket type multiplier."""
        return base_price * self.type.value

    def __str__(self) -> str:
        """Return a string representation of the ticket."""
        return (
            f"Ticket for {
                self.film.title} at {
                self.screening.start.strftime('%Y-%m-%d %H:%M')}\n" f"Type: {
                self.type.name}\n" f"Seat: {
                    self.seat_number}\n" f"Price: {
                        self.price:.2f}\n" f"Purchased: {
                            self.purchase_date.strftime('%Y-%m-%d %H:%M')}")
