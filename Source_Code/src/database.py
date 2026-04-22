import csv
import os
import sqlite3
from typing import List, Optional

from models import MediaItem


class MediaDatabase:
    ALLOWED_SORT_FIELDS = ["title", "category", "status", "rating"]
    ALLOWED_SORT_ORDERS = ["ASC", "DESC"]

    def __init__(self, db_name: str = "../data/media_library.db"):
        self.db_name = db_name
        self._ensure_data_directories()
        self._create_table()

    def _ensure_data_directories(self) -> None:
        db_folder = os.path.dirname(self.db_name)
        if db_folder:
            os.makedirs(db_folder, exist_ok=True)

        export_folder = os.path.join(os.path.dirname(self.db_name), "exports")
        os.makedirs(export_folder, exist_ok=True)

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self) -> None:
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

        return [self._row_to_media_item(row) for row in rows]

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

        return self._row_to_media_item(row)

    def delete_item(self, item_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM media_items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0

    def search_items(
        self,
        title: str = "",
        category: str = "",
        status: str = ""
    ) -> List[MediaItem]:
        query = """
            SELECT id, title, category, status, rating, notes, image_path
            FROM media_items
            WHERE 1=1
        """
        parameters = []

        if title.strip():
            query += " AND LOWER(title) LIKE ?"
            parameters.append(f"%{title.strip().lower()}%")

        if category.strip():
            query += " AND LOWER(category) = ?"
            parameters.append(category.strip().lower())

        if status.strip():
            query += " AND LOWER(status) = ?"
            parameters.append(status.strip().lower())

        query += " ORDER BY id ASC"

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            rows = cursor.fetchall()

        return [self._row_to_media_item(row) for row in rows]

    def sort_items(self, sort_by: str = "title", order: str = "ASC") -> List[MediaItem]:
        sort_by = sort_by.strip().lower()
        order = order.strip().upper()

        if sort_by not in self.ALLOWED_SORT_FIELDS:
            raise ValueError(
                f"Invalid sort field: {sort_by}. "
                f"Allowed fields: {self.ALLOWED_SORT_FIELDS}"
            )

        if order not in self.ALLOWED_SORT_ORDERS:
            raise ValueError(
                f"Invalid sort order: {order}. "
                f"Allowed orders: {self.ALLOWED_SORT_ORDERS}"
            )

        query = f"""
            SELECT id, title, category, status, rating, notes, image_path
            FROM media_items
            ORDER BY {sort_by} {order}, id ASC
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [self._row_to_media_item(row) for row in rows]

    def update_status(self, item_id: int, new_status: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE media_items
                SET status = ?
                WHERE id = ?
            """, (new_status, item_id))
            conn.commit()
            return cursor.rowcount > 0

    def toggle_completed_status(self, item_id: int) -> bool:
        item = self.get_item_by_id(item_id)

        if item is None:
            return False

        if item.status == "Completed":
            new_status = "Planned"
        else:
            new_status = "Completed"

        return self.update_status(item_id, new_status)

    def export_items_to_csv(self, items: List[MediaItem], file_name: str) -> str:
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        data_folder = os.path.dirname(self.db_name)
        export_folder = os.path.join(data_folder, "exports")
        os.makedirs(export_folder, exist_ok=True)

        full_path = os.path.join(export_folder, file_name)

        with open(full_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "ID",
                "Title",
                "Category",
                "Status",
                "Rating",
                "Notes",
                "Image Path"
            ])

            for item in items:
                writer.writerow([
                    item.item_id,
                    item.title,
                    item.category,
                    item.status,
                    item.rating,
                    item.notes,
                    item.image_path
                ])

        return full_path

    def _row_to_media_item(self, row) -> MediaItem:
        return MediaItem(
            item_id=row[0],
            title=row[1],
            category=row[2],
            status=row[3],
            rating=row[4],
            notes=row[5] or "",
            image_path=row[6] or ""
        )
    def update_item(self, item: MediaItem) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE media_items
                SET title = ?, category = ?, status = ?, rating = ?, notes = ?, image_path = ?
                WHERE id = ?
            """, (
                item.title,
                item.category,
                item.status,
                item.rating,
                item.notes,
                item.image_path,
                item.item_id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def get_category_statistics(self) -> dict:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category, COUNT(*)
                FROM media_items
                GROUP BY category
                ORDER BY category ASC
            """)
            rows = cursor.fetchall()

        stats = {}
        for category, count in rows:
            stats[category] = count

        return stats


    def get_completion_statistics(self) -> dict:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,
                    SUM(CASE WHEN status != 'Completed' THEN 1 ELSE 0 END) AS not_completed_count
                FROM media_items
            """)
            row = cursor.fetchone()

        completed = row[0] if row and row[0] is not None else 0
        not_completed = row[1] if row and row[1] is not None else 0

        return {
            "completed": completed,
            "not_completed": not_completed
        }


    def get_all_statistics(self) -> dict:
        return {
            "by_category": self.get_category_statistics(),
            "completion": self.get_completion_statistics()
        }   

            