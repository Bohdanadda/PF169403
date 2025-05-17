from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from .film import Film, ScreeningTime
from .promotions import SpecialScreening
from .viewer import Ticket, TicketType


@dataclass
class ScreeningStats:
    """
    Statistics for a single screening.

    Fields
    ------
    screening: ScreeningTime
        The screening these stats are for
    tickets_sold: int
        Number of tickets sold
    revenue: float
        Total revenue from ticket sales
    average_price: float
        Average price per ticket
    """
    screening: ScreeningTime
    tickets_sold: int
    revenue: float
    average_price: float

    @property
    def occupancy_rate(self) -> float:
        """Calculate the occupancy rate for this screening."""
        return self.tickets_sold / \
            self.screening.hall.capacity if self.screening.hall.capacity > 0 else 0.0


class CinemaStats:
    """
    Manages statistics and reporting for a cinema.
    """

    def __init__(self) -> None:
        # (hall_number, start_time) -> stats
        self._screening_stats: Dict[Tuple[int, str], ScreeningStats] = {}
        self._ticket_type_counts: Dict[TicketType, int] = {
            t: 0 for t in TicketType}
        self._special_screening_stats: Dict[SpecialScreening, ScreeningStats] = {
        }

    def record_ticket_sale(
            self,
            ticket: Ticket,
            screening: ScreeningTime) -> None:
        """Record a ticket sale for statistics."""
        key = (screening.hall.number, screening.start.isoformat())
        if key not in self._screening_stats:
            self._screening_stats[key] = ScreeningStats(
                screening=screening,
                tickets_sold=0,
                revenue=0.0,
                average_price=0.0
            )

        stats = self._screening_stats[key]
        stats.tickets_sold += 1
        stats.revenue += ticket.price
        stats.average_price = stats.revenue / stats.tickets_sold
        self._ticket_type_counts[ticket.type] += 1

    def record_special_screening_sale(
            self,
            ticket: Ticket,
            special: SpecialScreening) -> None:
        """Record a ticket sale for a special screening."""
        if special not in self._special_screening_stats:
            self._special_screening_stats[special] = ScreeningStats(
                screening=special.screening,
                tickets_sold=0,
                revenue=0.0,
                average_price=0.0
            )

        stats = self._special_screening_stats[special]
        stats.tickets_sold += 1
        stats.revenue += ticket.price
        stats.average_price = stats.revenue / stats.tickets_sold
        self._ticket_type_counts[ticket.type] += 1

    def get_screening_stats(
            self,
            screening: ScreeningTime) -> Optional[ScreeningStats]:
        """Get statistics for a specific screening."""
        key = (screening.hall.number, screening.start.isoformat())
        return self._screening_stats.get(key)

    def get_special_screening_stats(
            self, special: SpecialScreening) -> Optional[ScreeningStats]:
        """Get statistics for a specific special screening."""
        return self._special_screening_stats.get(special)

    def get_ticket_type_distribution(self) -> Dict[TicketType, float]:
        """Get the distribution of ticket types as percentages."""
        total = sum(self._ticket_type_counts.values())
        if total == 0:
            return {t: 0.0 for t in TicketType}
        return {t: round((count / total) * 100, 2)
                for t, count in self._ticket_type_counts.items()}

    def get_top_screenings(self, limit: int = 5) -> List[ScreeningStats]:
        """Get the top screenings by revenue."""
        all_stats = list(self._screening_stats.values()) + \
            list(self._special_screening_stats.values())
        return sorted(all_stats, key=lambda s: s.revenue, reverse=True)[:limit]

    def get_occupancy_report(self, start_date: datetime,
                             end_date: datetime) -> List[Tuple[ScreeningTime, float]]:
        """Get occupancy rates for screenings in a date range."""
        report = []
        for stats in self._screening_stats.values():
            screening_date = stats.screening.start.date()
            if start_date.date() <= screening_date <= end_date.date():
                report.append((stats.screening, stats.occupancy_rate))
        return sorted(report, key=lambda x: x[0].start)

    def get_revenue_report(self, start_date: datetime,
                           end_date: datetime) -> Tuple[float, float]:
        """Get total and average revenue for a date range."""
        relevant_stats = [stats for stats in self._screening_stats.values(
        ) if start_date.date() <= stats.screening.start.date() <= end_date.date()]
        if not relevant_stats:
            return 0.0, 0.0

        total_revenue = sum(stats.revenue for stats in relevant_stats)
        average_revenue = total_revenue / len(relevant_stats)
        return total_revenue, average_revenue

    def reset(self) -> None:
        """Reset all statistics to initial state."""
        self._screening_stats.clear()
        self._special_screening_stats.clear()
        self._ticket_type_counts = {t: 0 for t in TicketType}
