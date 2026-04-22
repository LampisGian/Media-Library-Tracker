from dataclasses import dataclass, field
from typing import Optional


class MediaConfig:
    ALLOWED_CATEGORIES = ["Movie", "Book", "Game", "Series", "Other"]
    ALLOWED_STATUSES = ["Planned", "In Progress", "Completed", "Dropped"]
    MIN_RATING = 0.0
    MAX_RATING = 10.0


@dataclass
class MediaItem:
    title: str
    category: str
    status: str
    rating: Optional[float] = None
    notes: str = ""
    image_path: str = ""
    item_id: Optional[int] = field(default=None)

    def __post_init__(self):
        self.title = self.title.strip()
        self.category = self.category.strip()
        self.status = self.status.strip()
        self.notes = self.notes.strip()
        self.image_path = self.image_path.strip()

        self._validate_title()
        self._validate_category()
        self._validate_status()
        self._validate_rating()

    def _validate_title(self):
        if not self.title:
            raise ValueError("Title cannot be empty.")

    def _validate_category(self):
        if self.category not in MediaConfig.ALLOWED_CATEGORIES:
            raise ValueError(
                f"Invalid category: {self.category}. "
                f"Allowed categories: {MediaConfig.ALLOWED_CATEGORIES}"
            )

    def _validate_status(self):
        if self.status not in MediaConfig.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status: {self.status}. "
                f"Allowed statuses: {MediaConfig.ALLOWED_STATUSES}"
            )

    def _validate_rating(self):
        if self.rating is None:
            return

        if not isinstance(self.rating, (int, float)):
            raise ValueError("Rating must be a number.")

        if not (MediaConfig.MIN_RATING <= self.rating <= MediaConfig.MAX_RATING):
            raise ValueError(
                f"Rating must be between "
                f"{MediaConfig.MIN_RATING} and {MediaConfig.MAX_RATING}."
            )

        self.rating = float(self.rating)