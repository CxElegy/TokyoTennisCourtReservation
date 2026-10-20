from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Slot


class Site(ABC):
    """A reservation site. Add other wards by subclassing and registering in get_site()."""

    name: str

    @abstractmethod
    def fetch_available(self, facility_names: list[str]) -> list[Slot]:
        """Return currently available slots for the given facilities. Read-only."""
