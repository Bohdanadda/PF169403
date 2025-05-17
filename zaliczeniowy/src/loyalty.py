from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

from .viewer import Ticket, Viewer


class LoyaltyTier(Enum):
    """Customer loyalty tiers with their point multipliers."""
    BRONZE = 1.0
    SILVER = 1.2
    GOLD = 1.5
    PLATINUM = 2.0


class RewardType(Enum):
    """Types of rewards available to loyalty program members."""
    FREE_TICKET = "Free movie ticket"
    POPCORN = "Free popcorn"
    DRINK = "Free drink"
    UPGRADE = "Seat upgrade"
    BIRTHDAY = "Birthday bonus points"


@dataclass
class LoyaltyReward:
    """
    Represents a reward in the loyalty program.

    Fields
    ------
    type: RewardType
        Type of reward
    points_required: int
        Points needed to claim this reward
    expiry_days: int
        Number of days until reward expires after claiming
    """
    type: RewardType
    points_required: int
    expiry_days: int

    def __post_init__(self) -> None:
        """Validate reward configuration."""
        if self.points_required < 0:
            raise ValueError("Points required cannot be negative")
        if self.expiry_days < 1:
            raise ValueError("Expiry days must be positive")


@dataclass
class LoyaltyMember:
    """
    Represents a member in the loyalty program.

    Fields
    ------
    viewer: Viewer
        The cinema viewer who is a member
    join_date: datetime
        When they joined the program
    points: int
        Current point balance
    tier: LoyaltyTier
        Current membership tier
    claimed_rewards: List[Tuple[RewardType, datetime]]
        History of claimed rewards
    """
    viewer: Viewer
    join_date: datetime = field(default_factory=datetime.now)
    points: int = 0
    tier: LoyaltyTier = LoyaltyTier.BRONZE
    claimed_rewards: List[tuple[RewardType, datetime]
                          ] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate member data."""
        if self.points < 0:
            raise ValueError("Points cannot be negative")


class LoyaltyProgram:
    """Manages the cinema's loyalty program."""

    def __init__(self) -> None:
        self._members: Dict[int, LoyaltyMember] = {}  # viewer_id -> member
        self._rewards: Dict[RewardType, LoyaltyReward] = {
            RewardType.FREE_TICKET: LoyaltyReward(RewardType.FREE_TICKET, 1000, 30),
            RewardType.POPCORN: LoyaltyReward(RewardType.POPCORN, 500, 14),
            RewardType.DRINK: LoyaltyReward(RewardType.DRINK, 300, 14),
            RewardType.UPGRADE: LoyaltyReward(RewardType.UPGRADE, 200, 7),
            RewardType.BIRTHDAY: LoyaltyReward(RewardType.BIRTHDAY, 0, 7)
        }
        self._tier_thresholds = {
            LoyaltyTier.BRONZE: 0,
            LoyaltyTier.SILVER: 5000,
            LoyaltyTier.GOLD: 10000,
            LoyaltyTier.PLATINUM: 20000
        }

    def add_member(self, viewer: Viewer) -> LoyaltyMember:
        """Add a new member to the loyalty program."""
        if viewer.id in self._members:
            raise ValueError(f"Viewer {viewer.id} is already a member")

        member = LoyaltyMember(viewer=viewer)
        self._members[viewer.id] = member
        return member

    def record_purchase(self, viewer_id: int, amount: float) -> None:
        """Record a purchase and award points."""
        if amount < 0:
            raise ValueError("Purchase amount cannot be negative")

        member = self._members.get(viewer_id)
        if not member:
            raise ValueError(f"No member found with viewer ID {viewer_id}")

        # Award 10 points per currency unit, multiplied by tier bonus
        points = int(amount * 10 * member.tier.value)
        member.points += points

        # Check for tier upgrade
        for tier, threshold in sorted(
                self._tier_thresholds.items(), key=lambda x: x[1], reverse=True):
            if member.points >= threshold:
                member.tier = tier
                break

    def claim_reward(self, viewer_id: int, reward_type: RewardType) -> None:
        """Claim a reward for a member."""
        member = self._members.get(viewer_id)
        if not member:
            raise ValueError(f"No member found with viewer ID {viewer_id}")

        reward = self._rewards.get(reward_type)
        if not reward:
            raise ValueError(f"Invalid reward type: {reward_type}")

        if member.points < reward.points_required:
            raise ValueError(
                f"Insufficient points. Need {
                    reward.points_required}, has {
                    member.points}")

        # Check if reward was claimed recently and hasn't expired
        now = datetime.now()
        for claimed_type, claim_date in member.claimed_rewards:
            if claimed_type == reward_type:
                if now - claim_date < timedelta(days=reward.expiry_days):
                    raise ValueError(
                        f"Cannot claim {
                            reward_type.value} again yet")

        member.points -= reward.points_required
        member.claimed_rewards.append((reward_type, now))

    def get_member(self, viewer_id: int) -> Optional[LoyaltyMember]:
        """Get a member's information."""
        return self._members.get(viewer_id)

    def get_available_rewards(self, viewer_id: int) -> List[RewardType]:
        """Get list of rewards the member can claim."""
        member = self._members.get(viewer_id)
        if not member:
            raise ValueError(f"No member found with viewer ID {viewer_id}")

        available = []
        now = datetime.now()

        for reward_type, reward in self._rewards.items():
            # Check points requirement
            if member.points < reward.points_required:
                continue

            # Check if reward was claimed recently
            can_claim = True
            for claimed_type, claim_date in member.claimed_rewards:
                if claimed_type == reward_type:
                    if now - claim_date < timedelta(days=reward.expiry_days):
                        can_claim = False
                        break

            if can_claim:
                available.append(reward_type)

        return available
