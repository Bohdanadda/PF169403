from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class AdminUser:
    username: str
    password: str
    is_active: bool = True

    def login(self, password: str) -> bool:
        """Attempt to log in with the given password."""
        return self.is_active and self.password == password

    def reset_password(self, new_password: str) -> None:
        """Reset the admin's password."""
        if not new_password:
            raise ValueError("New password cannot be empty")
        self.password = new_password


@dataclass
class SystemLog:
    timestamp: datetime
    operation: str
    admin: AdminUser

    def __str__(self) -> str:
        """Return a string representation of the log entry."""
        return f"{self.timestamp}: {self.operation} by {self.admin.username}"


@dataclass
class AdminPanel:
    logs: List[SystemLog] = field(default_factory=list)

    def add_log(self, operation: str, admin: AdminUser) -> None:
        """Add a new log entry."""
        log = SystemLog(timestamp=datetime.now(), operation=operation, admin=admin)
        self.logs.append(log)

    def view_logs(self, admin: AdminUser) -> List[SystemLog]:
        """View all logs if the admin is active."""
        if not admin.is_active:
            raise PermissionError("Inactive admin cannot view logs")
        return self.logs 