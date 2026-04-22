from database import MediaDatabase
from models import MediaItem


def print_items(items):
    if not items:
        print("No items found.")
        return

    for item in items:
        print(
            f"ID: {item.item_id} | "
            f"Title: {item.title} | "
            f"Category: {item.category} | "
            f"Status: {item.status} | "
            f"Rating: {item.rating} | "
            f"Notes: {item.notes} | "
            f"Image Path: {item.image_path}"
        )


def main():
    db = MediaDatabase()

    while True:
        print("\n=== Media Library Tracker Test ===")
        print("1. Add item")
        print("2. View all items")
        print("3. Delete item")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            category = input("Category: ").strip()
            status = input("Status: ").strip()
            rating_input = input("Rating (leave empty if none): ").strip()
            notes = input("Notes: ").strip()
            image_path = input("Image path (optional): ").strip()

            rating = None
            if rating_input:
                try:
                    rating = float(rating_input)
                except ValueError:
                    print("Invalid rating. It must be a number.")
                    continue

            try:
                item = MediaItem(
                    title=title,
                    category=category,
                    status=status,
                    rating=rating,
                    notes=notes,
                    image_path=image_path
                )
                new_id = db.add_item(item)
                print(f"Item added successfully with ID {new_id}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            items = db.get_all_items()
            print_items(items)

        elif choice == "3":
            item_id_input = input("Enter item ID to delete: ").strip()

            if not item_id_input.isdigit():
                print("Invalid ID.")
                continue

            deleted = db.delete_item(int(item_id_input))
            if deleted:
                print("Item deleted successfully.")
            else:
                print("No item found with that ID.")

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()