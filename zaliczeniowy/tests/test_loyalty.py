import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.loyalty import (LoyaltyMember, LoyaltyProgram, LoyaltyReward,
                         LoyaltyTier, RewardType)
from src.viewer import Viewer

# Module level datetime mock
mock_datetime = datetime(2025, 1, 1, 12, 0)


class TestLoyaltyReward(unittest.TestCase):
    """Test cases for LoyaltyReward class."""

    def test_valid_reward_creation(self):
        """Test creating a valid reward."""
        reward = LoyaltyReward(RewardType.FREE_TICKET, 1000, 30)
        self.assertEqual(reward.type, RewardType.FREE_TICKET)
        self.assertEqual(reward.points_required, 1000)
        self.assertEqual(reward.expiry_days, 30)

    def test_negative_points_required(self):
        """Test that negative points required raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            LoyaltyReward(RewardType.POPCORN, -100, 14)
        self.assertEqual(str(ctx.exception),
                         "Points required cannot be negative")

    def test_invalid_expiry_days(self):
        """Test that non-positive expiry days raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            LoyaltyReward(RewardType.DRINK, 300, 0)
        self.assertEqual(str(ctx.exception), "Expiry days must be positive")


class TestLoyaltyMember(unittest.TestCase):
    """Test cases for LoyaltyMember class."""

    def setUp(self):
        """Set up test data."""
        self.viewer = Viewer(
            name="Test User",
            email="test@example.com",
            age=25
        )

    def test_valid_member_creation(self):
        """Test creating a valid loyalty member."""
        member = LoyaltyMember(viewer=self.viewer, join_date=mock_datetime)
        self.assertEqual(member.viewer, self.viewer)
        self.assertEqual(member.join_date, mock_datetime)
        self.assertEqual(member.points, 0)
        self.assertEqual(member.tier, LoyaltyTier.BRONZE)
        self.assertEqual(member.claimed_rewards, [])

    def test_negative_points(self):
        """Test that negative points raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            LoyaltyMember(viewer=self.viewer, points=-100)
        self.assertEqual(str(ctx.exception), "Points cannot be negative")


class TestLoyaltyProgram(unittest.TestCase):
    """Test cases for LoyaltyProgram class."""

    def setUp(self):
        """Set up test fixtures."""
        self.viewer = Viewer(
            name="Test User",
            email="test@example.com",
            age=25
        )
        self.program = LoyaltyProgram()
        self.reward = LoyaltyReward(
            RewardType.POPCORN,
            100,
            30
        )
        # Create and configure loyalty datetime mock
        self.datetime_patcher = patch('src.loyalty.datetime')
        self.mock_dt = self.datetime_patcher.start()
        self.mock_dt.now = Mock(return_value=mock_datetime)
        self.mock_dt.datetime = datetime
        self.mock_dt.timedelta = timedelta
        # Add cleanup
        self.addCleanup(self.datetime_patcher.stop)

    def test_add_member(self):
        """Test adding a new member."""
        member = self.program.add_member(self.viewer)
        self.assertEqual(member.viewer, self.viewer)
        self.assertEqual(member.points, 0)
        self.assertEqual(member.tier, LoyaltyTier.BRONZE)

    def test_add_duplicate_member(self):
        """Test that adding a duplicate member raises ValueError."""
        self.program.add_member(self.viewer)
        with self.assertRaises(ValueError) as ctx:
            self.program.add_member(self.viewer)
        self.assertEqual(str(ctx.exception),
                         f"Viewer {self.viewer.id} is already a member")

    def test_record_purchase(self):
        """Test recording a purchase and awarding points."""
        member = self.program.add_member(self.viewer)
        self.program.record_purchase(self.viewer.id, 100.0)
        # 100 * 10 points/unit * 1.0 (BRONZE tier multiplier) = 1000 points
        self.assertEqual(member.points, 1000)
        self.assertEqual(member.tier, LoyaltyTier.BRONZE)

    def test_tier_upgrade(self):
        """Test tier upgrades based on points."""
        member = self.program.add_member(self.viewer)

        # Record purchases to reach different tiers
        purchases = [
            (500.0, LoyaltyTier.SILVER),    # 5000 points
            (500.0, LoyaltyTier.GOLD),      # 10000 points
            (1000.0, LoyaltyTier.PLATINUM)  # 20000 points
        ]

        for amount, expected_tier in purchases:
            self.program.record_purchase(self.viewer.id, amount)
            self.assertEqual(member.tier, expected_tier)

    def test_claim_reward(self):
        """Test claiming a reward."""
        member = self.program.add_member(self.viewer)
        self.program.record_purchase(self.viewer.id, 100.0)  # 1000 points
        self.program.claim_reward(
            self.viewer.id,
            RewardType.DRINK)  # 300 points
        self.assertEqual(member.points, 700)  # 1000 - 300
        self.assertEqual(
            member.claimed_rewards, [
                (RewardType.DRINK, mock_datetime)])

    def test_claim_reward_insufficient_points(self):
        """Test claiming a reward with insufficient points."""
        member = self.program.add_member(self.viewer)
        with self.assertRaises(ValueError) as ctx:
            self.program.claim_reward(
                self.viewer.id,
                RewardType.FREE_TICKET)  # 1000 points needed
        self.assertEqual(
            str(ctx.exception),
            f"Insufficient points. Need 1000, has 0"
        )

    def test_claim_reward_too_soon(self):
        """Test claiming the same reward too soon."""
        member = self.program.add_member(self.viewer)
        self.program.record_purchase(self.viewer.id, 200.0)  # 2000 points

        # First claim
        self.program.claim_reward(self.viewer.id, RewardType.DRINK)

        # Try to claim again before expiry
        self.mock_dt.now.return_value = mock_datetime + timedelta(days=7)
        with self.assertRaises(ValueError) as ctx:
            self.program.claim_reward(self.viewer.id, RewardType.DRINK)
        self.assertEqual(
            str(ctx.exception),
            "Cannot claim Free drink again yet"
        )

    def test_get_available_rewards(self):
        """Test getting available rewards."""
        member = self.program.add_member(self.viewer)
        self.program.record_purchase(self.viewer.id, 100.0)  # 1000 points

        available = self.program.get_available_rewards(self.viewer.id)
        self.assertIn(RewardType.FREE_TICKET, available)  # 1000 points
        self.assertIn(RewardType.POPCORN, available)      # 500 points
        self.assertIn(RewardType.DRINK, available)        # 300 points
        self.assertIn(RewardType.UPGRADE, available)      # 200 points
        self.assertIn(RewardType.BIRTHDAY, available)     # 0 points

    def test_get_available_rewards_after_claim(self):
        """Test that claimed rewards are not available until expiry."""
        member = self.program.add_member(self.viewer)
        self.program.record_purchase(self.viewer.id, 100.0)  # 1000 points

        # Claim a reward
        self.program.claim_reward(self.viewer.id, RewardType.DRINK)

        # Check availability before expiry
        self.mock_dt.now.return_value = mock_datetime + timedelta(days=7)
        available = self.program.get_available_rewards(self.viewer.id)
        self.assertNotIn(RewardType.DRINK, available)

        # Check availability after expiry
        self.mock_dt.now.return_value = mock_datetime + timedelta(days=15)
        available = self.program.get_available_rewards(self.viewer.id)
        self.assertIn(RewardType.DRINK, available)


if __name__ == "__main__":
    unittest.main()
