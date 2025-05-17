import unittest
from datetime import datetime

from src.admin import AdminPanel, AdminUser, SystemLog


class TestAdminUser(unittest.TestCase):
    """Test cases for AdminUser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.admin = AdminUser(username="admin", password="password123")

    def test_admin_login_success(self):
        """Test successful login with correct password."""
        self.assertTrue(self.admin.login("password123"))

    def test_admin_login_wrong_password(self):
        """Test login failure with incorrect password."""
        self.assertFalse(self.admin.login("wrongpassword"))

    def test_password_reset_flow(self):
        """Test password reset functionality."""
        self.admin.reset_password("newpassword123")
        self.assertEqual(self.admin.password, "newpassword123")
        self.assertTrue(self.admin.login("newpassword123"))


class TestSystemLog(unittest.TestCase):
    """Test cases for SystemLog class."""

    def setUp(self):
        """Set up test fixtures."""
        self.admin = AdminUser(username="admin", password="password123")
        self.log = SystemLog(
            timestamp=datetime.now(),
            operation="Film deleted",
            admin=self.admin)

    def test_string_representation(self):
        """Test string representation of log entry."""
        expected = f"{self.log.timestamp}: Film deleted by admin"
        self.assertEqual(str(self.log), expected)


class TestAdminPanel(unittest.TestCase):
    """Test cases for AdminPanel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.admin = AdminUser(username="admin", password="password123")
        self.panel = AdminPanel()

    def test_view_logs_as_admin(self):
        """Test viewing logs as an active admin."""
        self.panel.add_log("Film deleted", self.admin)
        logs = self.panel.view_logs(self.admin)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].operation, "Film deleted")

    def test_permission_denied_for_guest(self):
        """Test that inactive admin cannot view logs."""
        self.admin.is_active = False
        with self.assertRaises(PermissionError):
            self.panel.view_logs(self.admin)


if __name__ == "__main__":
    unittest.main()
