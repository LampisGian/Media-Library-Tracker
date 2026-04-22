import sqlite3
from typing import List, Optional

from models import MediaItem


class MediaDatabase:
    def __init__(self, db_name: str = "media_library.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS media_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL,
                    rating REAL,
                    notes TEXT,
                    image_path TEXT
                )
            """)
            conn.commit()

    def add_item(self, item: MediaItem) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO media_items (title, category, status, rating, notes, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.title,
                item.category,
                item.status,
                item.rating,
                item.notes,
                item.image_path
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_items(self) -> List[MediaItem]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, category, status, rating, notes, image_path
                FROM media_items
                ORDER BY id ASC
            """)
            rows = cursor.fetchall()

        items = []
        for row in rows:
            item = MediaItem(
                title=row[1],
                category=row[2],
                status=row[3],
                rating=row[4],
                notes=row[5] or "",
                image_path=row[6] or "",
                item_id=row[0]
            )
            items.append(item)

        return items

    def get_item_by_id(self, item_id: int) -> Optional[MediaItem]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, category, status, rating, notes, image_path
                FROM media_items
                WHERE id = ?
            """, (item_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return MediaItem(
            title=row[1],
            category=row[2],
            status=row[3],
            rating=row[4],
            notes=row[5] or "",
            image_path=row[6] or "",
            item_id=row[0]
        )

    def delete_item(self, item_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM media_items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0