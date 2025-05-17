from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, TYPE_CHECKING, Dict, Any, Set

if TYPE_CHECKING:
    from .film import Film, ScreeningTime


class ScreeningType(Enum):
    """Types of special screenings with their price multipliers."""
    REGULAR = 1.0
    PREMIERE = 1.5
    MIDNIGHT = 0.8
    MATINEE = 0.7
    SENIOR_DAY = 0.6


@dataclass
class SpecialScreening:
    film: Film
    screening: ScreeningTime
    type: ScreeningType
    description: str

    def __post_init__(self) -> None:
        """Validate the special screening data."""
        if not isinstance(self.type, ScreeningType):
            raise ValueError("type must be a ScreeningType")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("description must be a non-empty string")

    def __hash__(self) -> int:
        """Make the class hashable."""
        return hash((self.film, self.screening, self.type, self.description))

    def __eq__(self, other: object) -> bool:
        """Compare two special screenings for equality."""
        if not isinstance(other, SpecialScreening):
            return NotImplemented
        return (self.film == other.film and
                self.screening == other.screening and
                self.type == other.type and
                self.description == other.description)

    @property
    def base_price(self) -> float:
        """Base price for this type of screening."""
        return self.type.value


class CinemaPromotion:
    """Represents a promotion for a film screening."""
    def __init__(self, name: str, discount_percent: float, conditions: Dict[str, Any], expires_at: datetime):
        self.name = name
        self.discount_percent = discount_percent
        self.conditions = conditions
        self.expires_at = expires_at
        self._applied_screenings: Set[str] = set()

    def apply(self, screening_id: str) -> None:
        self._applied_screenings.add(screening_id)

    def is_applied(self, screening_id: str) -> bool:
        return screening_id in self._applied_screenings

    def apply_to_screening(self, screening: SpecialScreening) -> None:
        """Apply this promotion to a special screening."""
        if datetime.now() > self.expires_at:
            raise ValueError("Promotion has expired")
        if screening in self._applied_screenings:
            raise ValueError("Promotion already applied to this screening")
        self._applied_screenings.add(screening)

    def remove_from_screening(self, screening: SpecialScreening) -> None:
        """Remove this promotion from a special screening."""
        try:
            self._applied_screenings.remove(screening)
        except KeyError as exc:
            raise ValueError("Promotion not applied to this screening") from exc

    @property
    def applied_screenings(self) -> List[SpecialScreening]:
        """Return a list of screenings this promotion is applied to."""
        return list(self._applied_screenings)

    def is_valid(self) -> bool:
        """Check if the promotion is still valid."""
        return datetime.now() <= self.expires_at

    def calculate_discount(self, base_price: float) -> float:
        """Calculate the discounted price."""
        return base_price * self.discount_percent 

__all__ = ["CinemaPromotion", "ScreeningType", "SpecialScreening"] 