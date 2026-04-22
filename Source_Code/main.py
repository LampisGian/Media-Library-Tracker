from database import MediaDatabase
from models import MediaItem


def main():
    db = MediaDatabase()

    sample_item = MediaItem(
        title="Inception",
        category="Movie",
        status="Completed",
        rating=9.0,
        notes="Mind-bending sci-fi movie",
        image_path=""
    )

    db.add_item(sample_item)

    print("Current items in database:")
    for item in db.get_all_items():
        print(
            f"ID: {item.item_id}, "
            f"Title: {item.title}, "
            f"Category: {item.category}, "
            f"Status: {item.status}, "
            f"Rating: {item.rating}, "
            f"Notes: {item.notes}"
        )


if __name__ == "__main__":
    main()