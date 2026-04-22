from database import MediaDatabase
from models import MediaItem, MediaConfig


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
            f"Notes: {item.notes}"
        )


def print_choices(title, values):
    print(title)
    for index, value in enumerate(values, start=1):
        print(f"{index}. {value}")


def get_choice_from_list(prompt, values):
    while True:
        print_choices(prompt, values)
        choice = input("Choose an option number: ").strip()

        if choice.isdigit():
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(values):
                return values[choice_index]

        print("Invalid choice. Please try again.\n")


def get_rating():
    while True:
        rating_input = input("Rating (0-10, leave empty if none): ").strip()

        if rating_input == "":
            return None

        try:
            rating = float(rating_input)
            if 0 <= rating <= 10:
                return rating
            print("Rating must be between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def add_item_flow(db: MediaDatabase):
    print("\nAdd New Media Item")

    title = input("Title: ").strip()
    category = get_choice_from_list("Available categories:", MediaConfig.ALLOWED_CATEGORIES)
    status = get_choice_from_list("Available statuses:", MediaConfig.ALLOWED_STATUSES)
    rating = get_rating()
    notes = input("Notes: ").strip()
    image_path = input("Image path (optional): ").strip()

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
        print(f"Item added successfully with ID {new_id}.\n")
    except ValueError as error:
        print(f"Error: {error}\n")


def view_items_flow(db: MediaDatabase):
    print("\nLibrary Items")
    items = db.get_all_items()
    print_items(items)
    print()


def delete_item_flow(db: MediaDatabase):
    print("\nDelete Media Item")
    item_id_input = input("Enter item ID to delete: ").strip()

    if not item_id_input.isdigit():
        print("Invalid ID.\n")
        return

    item_id = int(item_id_input)
    deleted = db.delete_item(item_id)

    if deleted:
        print("Item deleted successfully.\n")
    else:
        print("No item found with that ID.\n")


def search_items_flow(db: MediaDatabase):
    print("\nSearch Items")
    print("Leave fields empty if you do not want to use them.")

    title = input("Search by title: ").strip()
    category = input("Search by category: ").strip()
    status = input("Search by status: ").strip()

    items = db.search_items(title=title, category=category, status=status)
    print_items(items)
    print()


def sort_items_flow(db: MediaDatabase):
    print("\nSort Items")
    print("Available sort fields: title, category, status, rating")
    sort_by = input("Sort by: ").strip()
    order = input("Order (ASC or DESC): ").strip()

    try:
        items = db.sort_items(sort_by=sort_by, order=order)
        print_items(items)
    except ValueError as error:
        print(f"Error: {error}")
    print()


def toggle_status_flow(db: MediaDatabase):
    print("\nMark as Watched/Read Toggle")
    item_id_input = input("Enter item ID: ").strip()

    if not item_id_input.isdigit():
        print("Invalid ID.\n")
        return

    item_id = int(item_id_input)
    updated = db.toggle_completed_status(item_id)

    if updated:
        print("Item status toggled successfully.\n")
    else:
        print("No item found with that ID.\n")


def export_filtered_items_flow(db: MediaDatabase):
    print("\nExport Filtered Items to CSV")
    print("Leave fields empty if you do not want to use them.")

    title = input("Filter by title: ").strip()
    category = input("Filter by category: ").strip()
    status = input("Filter by status: ").strip()
    file_name = input("Enter CSV file name (example: exported_items.csv): ").strip()

    if not file_name:
        print("File name cannot be empty.\n")
        return

    if not file_name.lower().endswith(".csv"):
        file_name += ".csv"

    items = db.search_items(title=title, category=category, status=status)

    if not items:
        print("No matching items found. CSV file was not created.\n")
        return

    db.export_items_to_csv(items, file_name)
    print(f"Filtered items exported successfully to {file_name}.\n")


def main():
    db = MediaDatabase()

    while True:
        print("=== Media Library Tracker ===")
        print("1. Add item")
        print("2. View all items")
        print("3. Delete item")
        print("4. Search items")
        print("5. Sort items")
        print("6. Toggle watched/read status")
        print("7. Export filtered items to CSV")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_item_flow(db)
        elif choice == "2":
            view_items_flow(db)
        elif choice == "3":
            delete_item_flow(db)
        elif choice == "4":
            search_items_flow(db)
        elif choice == "5":
            sort_items_flow(db)
        elif choice == "6":
            toggle_status_flow(db)
        elif choice == "7":
            export_filtered_items_flow(db)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()