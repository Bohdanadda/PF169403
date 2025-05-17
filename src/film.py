from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, TYPE_CHECKING, Any, TypeVar, Protocol

from src.exceptions import ValidationError, ScheduleConflictError
from src.promotions import CinemaPromotion

VALID_RATINGS = {"G", "PG", "PG-13", "R", "NC-17"}
MAX_DURATION = 960  # 16 godzin w minutach
MIN_DURATION = 1    # 1 minuta


class ScreeningTime:
    def __init__(self, start: datetime, hall: int):
        if start <= datetime.now():
            raise ValidationError("Screening time must be in the future")
        if hall <= 0:
            raise ValidationError("Hall number must be positive")
        self.start = start
        self.hall = hall

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScreeningTime):
            return NotImplemented
        return self.start == other.start and self.hall == other.hall

    def __hash__(self) -> int:
        return hash((self.start, self.hall))


@dataclass(frozen=True)
class Film:
    title: str
    duration: int  # w minutach
    rating: str
    screenings: List[ScreeningTime] = field(default_factory=list)
    _promotions: Dict[ScreeningTime, CinemaPromotion] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title:
            raise ValidationError("Title cannot be empty")
        if self.duration <= 0:
            raise ValidationError("Duration must be a positive integer")
        if not self.rating:
            raise ValidationError("Rating cannot be empty")
        if self.rating not in ["G", "PG", "PG-13", "R", "NC-17"]:
            raise ValidationError("Invalid rating")
        if self.duration < MIN_DURATION or self.duration > MAX_DURATION:
            raise ValidationError(f"duration must be between {MIN_DURATION} and {MAX_DURATION} minutes")

    def add_screening(self, screening: ScreeningTime) -> None:
        if screening in self.screenings:
            raise ValidationError("Screening already exists")

        for existing in self.screenings:
            if existing.hall == screening.hall:
                existing_end = existing.start + timedelta(minutes=self.duration)
                screening_end = screening.start + timedelta(minutes=self.duration)
                if (existing.start <= screening.start < existing_end or
                    existing.start < screening_end <= existing_end or
                    (screening.start <= existing.start and screening_end >= existing_end)):
                    raise ScheduleConflictError(
                        f"Screening conflicts with existing screening in hall {existing.hall}"
                    )

        self.screenings.append(screening)
        self.screenings.sort(key=lambda s: s.start)

    def remove_screening(self, screening: ScreeningTime) -> None:
        if screening not in self.screenings:
            raise ValidationError("Screening does not exist")
        self.screenings.remove(screening)

    def apply_promotion(self, screening: ScreeningTime, promotion: CinemaPromotion) -> None:
        """Apply a promotion to a screening."""
        if not isinstance(screening, ScreeningTime):
            raise ValueError("screening must be a ScreeningTime object")
        
        if screening not in self.screenings:
            raise ValueError("Screening not found")
        if screening in self._promotions:
            raise ValueError("Screening already has a promotion")
        if promotion.expires_at < datetime.now():
            raise ValueError("Promotion has expired")
        
        self._promotions[screening] = promotion

    def remove_promotion(self, screening: ScreeningTime) -> None:
        """Remove a promotion from a screening."""
        if not isinstance(screening, ScreeningTime):
            raise ValueError("screening must be a ScreeningTime object")
        if screening not in self.screenings:
            raise ValueError("Screening not found")
        if screening not in self._promotions:
            raise ValueError("Screening has no promotion")
        
        del self._promotions[screening]

    def get_promotion(self, screening: ScreeningTime) -> Optional[CinemaPromotion]:
        """Get the promotion for a screening."""
        if not isinstance(screening, ScreeningTime):
            raise ValueError("screening must be a ScreeningTime object")
        if screening not in self.screenings:
            raise ValueError("Screening not found")
        
        return self._promotions.get(screening)

    
    def upcoming_screenings(self, now: Optional[datetime] = None) -> List[ScreeningTime]:
        
        if now is None:
            now = datetime.now()
        return [s for s in self.screenings if s.start > now]

    
    def __repr__(self) -> str:  # pragma: no cover
        return f"<Film {self.title!r}, {len(self.screenings)} screenings>"

    def __str__(self) -> str:
        """Return a string representation of the film."""
        return f"{self.title} ({self.rating}) - {self.duration} min"

    def __hash__(self) -> int:
        """Make Film hashable for use in dictionaries and sets."""
        return hash((self.title, self.duration, self.rating))