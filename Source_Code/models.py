from dataclasses import dataclass
from typing import Optional


@dataclass
class MediaItem:
    title: str
    category: str
    status: str
    rating: Optional[float] = None
    notes: str = ""
    image_path: str = ""
    item_id: Optional[int] = None