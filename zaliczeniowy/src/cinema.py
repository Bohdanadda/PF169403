"""
cinema.py
~~~~~~~~~

Central domain objects for managing halls and seat reservations.
The module deliberately avoids any UI concerns; persistence happens
via a simple JSON structure to keep the example self‑contained.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from .film import Film, ScreeningTime

from src.exceptions import ReservationError, ValidationError


class Hall:
    """
    Represents a cinema hall.

    Fields
    ------
    number: int
        The hall number
    capacity: int
        The number of seats in the hall
    """

    def __init__(self, number: int, capacity: int):
        """Initialize a hall.

        Args:
            number: The hall number
            capacity: The number of seats in the hall

        Raises:
            ValidationError: If the capacity is not positive
        """
        if capacity <= 0:
            raise ValidationError("Capacity must be positive")
        self.number = number
        self.capacity = capacity
        self.available_seats = capacity

    def reserve_seats(self, seats: int) -> None:
        """Reserve seats in the hall.

        Args:
            seats: The number of seats to reserve

        Raises:
            ValidationError: If the number of seats is not positive
            ReservationError: If there are not enough seats available
        """
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")
        if seats > self.available_seats:
            raise ReservationError("Not enough seats available")
        self.available_seats -= seats

    def cancel_reservation(self, seats: int) -> None:
        """Cancel a seat reservation.

        Args:
            seats: The number of seats to cancel

        Raises:
            ValidationError: If the number of seats is not positive
            ReservationError: If there are not enough seats to cancel
        """
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")
        if seats > (self.capacity - self.available_seats):
            raise ReservationError("Not enough seats to cancel")
        self.available_seats += seats


class Cinema:
    """
    Aggregate root that owns halls and maintains seat reservations for screenings.
    """

    def __init__(self, name: str, halls: List[Hall] | None = None) -> None:
        self.name = name
        self._halls: Dict[int, Hall] = {h.number: h for h in (halls or [])}
        self._reservations: Dict[Tuple[int, str], int] = {}

    def add_screening(self, film, screening) -> None:
        """Add a screening to a film, ensuring the hall exists."""
        if screening.hall not in self._halls:
            raise ValidationError(f"Hall {screening.hall} does not exist")
        film.add_screening(screening)

    def reserve_seats(self, screening, hall, seats: int) -> None:
        """Reserve seats for a screening in a hall."""
        self._validate_reservation(screening, hall, seats)
        hall.reserve_seats(seats)

    def _validate_reservation(self, screening, hall, seats: int) -> None:
        """Validate reservation parameters."""
        if hall.number not in self._halls:
            raise ValidationError(f"Hall {hall.number} does not exist")
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")
        if seats > hall.capacity:
            raise ValidationError("Not enough seats available")

    def add_hall(self, hall: Hall, *, overwrite: bool = False) -> None:
        """Register a new hall. If *overwrite* is False, raising on duplicate numbers."""
        if not overwrite and hall.number in self._halls:
            raise ValidationError(f"Hall #{hall.number} already exists.")
        self._halls[hall.number] = hall

    def remove_hall(self, hall: Hall) -> None:
        """Remove a hall from the cinema."""
        if hall.number not in self._halls:
            raise ValidationError(f"Hall {hall.number} does not exist")
        del self._halls[hall.number]

    def hall(self, number: int) -> Hall:
        """Return the Hall by number, or raise KeyError."""
        return self._halls[number]

    @property
    def halls(self) -> List[Hall]:
        """Get all halls in the cinema."""
        return list(self._halls.values())

    def reserve(
            self,
            film,
            screening,
            seats: int,
            *,
            commit: bool = True) -> None:
        """
        Reserve *seats* seats for *screening* of *film*.

        Parameters
        ----------
        film: Film
            The film object – used only for validation that screening belongs to it.
        screening: ScreeningTime
            Identifies the start time + hall.
        seats: int
            Number of seats requested.
        commit: bool
            If False, act as a dry‑run (validation only).

        Raises
        ------
        ReservationError
            If requested seats exceed available capacity or screening not in film.
        """
        self._validate_reservation_request(film, screening, seats)

        if commit:
            key = (screening.hall, screening.start.isoformat())
            already_reserved = self._reservations.get(key, 0)
            self._reservations[key] = already_reserved + seats

    def _validate_reservation_request(
            self, film, screening, seats: int) -> None:
        """Validate reservation request parameters."""
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")

        if screening not in film.screenings:
            raise ReservationError(
                "Screening does not belong to the given film.")

        hall = self._halls.get(screening.hall)
        if hall is None:
            raise ReservationError(
                f"Hall #{
                    screening.hall} not registered in cinema.")

        key = (screening.hall, screening.start.isoformat())
        already_reserved = self._reservations.get(key, 0)
        available = hall.capacity - already_reserved
        if seats > available:
            raise ReservationError(
                f"Requested {seats} seats, but only {available} left in hall {
                    hall.number}.")

    def cancel_reservation(self, film, screening, seats: int) -> None:
        """Cancel a reservation for seats."""
        self._validate_cancellation_request(film, screening, seats)

        key = (screening.hall, screening.start.isoformat())
        already_reserved = self._reservations.get(key, 0)
        self._reservations[key] = already_reserved - seats

    def _validate_cancellation_request(
            self, film, screening, seats: int) -> None:
        """Validate cancellation request parameters."""
        if seats <= 0:
            raise ValidationError("Number of seats must be positive")

        if screening not in film.screenings:
            raise ReservationError(
                "Screening does not belong to the given film.")

        hall = self._halls.get(screening.hall)
        if hall is None:
            raise ReservationError(
                f"Hall #{
                    screening.hall} not registered in cinema.")

        key = (screening.hall, screening.start.isoformat())
        already_reserved = self._reservations.get(key, 0)
        if seats > already_reserved:
            raise ReservationError(
                f"Requested to cancel {seats} seats, but only {already_reserved} reserved in hall {
                    hall.number}.")

    def available_seats(self, screening) -> int:
        """Return remaining seat count for a given screening."""
        hall = self._halls[screening.hall]
        reserved = self._reservations.get(
            (screening.hall, screening.start.isoformat()), 0)
        return hall.capacity - reserved

    def get_available_seats(self, film, screening) -> int:
        """Get the number of available seats for a screening."""
        return self.available_seats(screening)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, file_path: str | Path) -> None:
        """
        Persist halls and reservations into *file_path* in JSON format.
        """
        payload = {
            "meta": {"name": self.name, "timestamp": datetime.now(timezone.utc).isoformat()},
            "halls": [
                {
                    "number": h.number,
                    "capacity": h.capacity,
                    "available_seats": h.available_seats
                }
                for h in self._halls.values()
            ],
            "reservations": [
                {
                    "hall": hall,
                    "screening_start": start_iso,
                    "reserved": seats,
                }
                for (hall, start_iso), seats in self._reservations.items()
            ],
        }
        try:
            Path(file_path).write_text(json.dumps(payload, indent=2))
        except (OSError, TypeError) as exc:
            raise IOError(
                f"Unable to write cinema data to {file_path}") from exc

    @classmethod
    def load(cls, file_path: str | Path) -> "Cinema":
        """
        Factory to reconstruct a Cinema instance from JSON file produced by `save`.
        """
        try:
            data = json.loads(Path(file_path).read_text())
            halls = []
            for h_dict in data["halls"]:
                hall = Hall(
                    number=h_dict["number"],
                    capacity=h_dict["capacity"])
                hall.available_seats = h_dict["available_seats"]
                halls.append(hall)
            cinema = cls(data["meta"]["name"], halls)
            reservations = data.get("reservations", [])
            for rec in reservations:
                key = (rec["hall"], rec["screening_start"])
                cinema._reservations[key] = rec["reserved"]
            return cinema
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise IOError(
                f"Unable to load cinema data from {file_path}") from exc

    def __repr__(self) -> str:
        return f"<Cinema {self.name!r}: {len(self._halls)} halls>"
