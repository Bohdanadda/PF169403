from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.exceptions import ValidationError

if TYPE_CHECKING:
    from .film import Film
    from .ticket import Ticket, TicketType
else:
    from .film import Film
    from .ticket import Ticket, TicketType


@dataclass
class Viewer:
    """
    Represents a cinema viewer with their purchase history and preferences.

    Fields
    ------
    name: str
        Viewer's name
    email: str
        Viewer's email address
    age: int
        Viewer's age
    favorite_genres: List[str]
        List of viewer's favorite film genres
    purchase_history: List[Ticket]
        List of tickets purchased by the viewer
    loyalty_points: int
        Number of loyalty points accumulated
    id: str
        Unique identifier for the viewer
    """
    name: str
    email: str
    age: int
    favorite_genres: List[str] = field(default_factory=list)
    purchase_history: List[Ticket] = field(default_factory=list)
    loyalty_points: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reservations: Dict[datetime, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the viewer data."""
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Name cannot be empty")
        if not self.email or not isinstance(self.email, str):
            raise ValidationError("Email cannot be empty")
        if not self._is_valid_email(self.email):
            raise ValidationError("Invalid email format")
        if not isinstance(self.age, int) or self.age < 0:
            raise ValidationError("Age must be a non-negative integer")
        if not isinstance(self.favorite_genres, list):
            raise ValidationError("Favorite genres must be a list")
        if not isinstance(self.loyalty_points, int) or self.loyalty_points < 0:
            raise ValidationError(
                "Loyalty points must be a non-negative integer")
        if not isinstance(self.id, str):
            raise ValidationError("ID must be a string")

    def add_ticket(self, ticket: Ticket) -> None:
        """Add a ticket to the viewer's purchase history."""
        if not isinstance(ticket, Ticket):
            raise ValueError("ticket must be a Ticket object")
        self.purchase_history.append(ticket)
        self.loyalty_points += 10  # Add 10 points for each ticket

    def get_tickets_for_film(self, film: Film) -> List[Ticket]:
        """Get all tickets purchased for a specific film."""
        return [ticket for ticket in self.purchase_history if ticket.film == film]

    def get_total_spent(self) -> float:
        """Calculate total amount spent on tickets."""
        return sum(ticket.price for ticket in self.purchase_history)

    def get_favorite_films(self) -> List[Film]:
        """Get list of films the viewer has watched most frequently."""
        film_counts: Dict[Film, int] = {}
        for ticket in self.purchase_history:
            film_counts[ticket.film] = film_counts.get(ticket.film, 0) + 1
        return sorted(
            film_counts.keys(),
            key=lambda f: film_counts[f],
            reverse=True)

    def can_watch_film(self, film: Film) -> bool:
        """Check if viewer meets age requirements for a film."""
        rating_ages = {
            "G": 0,
            "PG": 0,
            "PG-13": 13,
            "R": 17,
            "NC-17": 18
        }
        return self.age >= rating_ages.get(film.rating, 0)

    def get_loyalty_status(self) -> str:
        """Get viewer's loyalty status based on points."""
        if self.loyalty_points >= 1000:
            return "PLATINUM"
        elif self.loyalty_points >= 500:
            return "GOLD"
        elif self.loyalty_points >= 100:
            return "SILVER"
        else:
            return "BRONZE"

    def __str__(self) -> str:
        """Return a string representation of the viewer."""
        return (
            f"Viewer: {self.name}\n"
            f"Email: {self.email}\n"
            f"Age: {self.age}\n"
            f"Favorite Genres: {', '.join(self.favorite_genres)}\n"
            f"Loyalty Status: {self.get_loyalty_status()}\n"
            f"Total Spent: ${self.get_total_spent():.2f}\n"
            f"Tickets Purchased: {len(self.purchase_history)}"
        )

    def _is_valid_email(self, email: str) -> bool:
        """Check if an email address is valid.

        Args:
            email: The email address to validate

        Returns:
            True if the email is valid, False otherwise
        """
        if not email or '@' not in email:
            return False
        local_part, domain = email.split('@', 1)
        return bool(local_part) and bool(domain) and '.' in domain

    def add_reservation(self, screening_time: datetime, seats: int) -> None:
        """Add a reservation for a screening.

        Args:
            screening_time: The time of the screening
            seats: The number of seats to reserve

        Raises:
            ValidationError: If the screening time is in the past, seats is not positive,
                           or a reservation already exists for this time
        """
        if screening_time <= datetime.now():
            raise ValidationError("Cannot make reservation for past time")
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")
        if screening_time in self.reservations:
            raise ValidationError("Reservation already exists for this time")
        self.reservations[screening_time] = {"seats": seats}

    def cancel_reservation(self, screening_time: datetime) -> None:
        """Cancel a reservation for a screening.

        Args:
            screening_time: The time of the screening to cancel

        Raises:
            ValidationError: If no reservation exists for this time
        """
        if screening_time not in self.reservations:
            raise ValidationError("No reservation exists for this time")
        del self.reservations[screening_time]

    def get_reservation(self, screening_time: datetime) -> Dict[str, Any]:
        """Get details of a reservation.

        Args:
            screening_time: The time of the screening

        Returns:
            The reservation details

        Raises:
            ValidationError: If no reservation exists for this time
        """
        if screening_time not in self.reservations:
            raise ValidationError("No reservation exists for this time")
        return self.reservations[screening_time]
