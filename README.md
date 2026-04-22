# Media Library Tracker

## Description

Media Library Tracker is a local desktop application created for organizing and managing personal media collections in a simple and visually interactive way. The program supports different types of media, including movies, books, games, and TV series, and allows the user to store them in a structured library with persistent storage.

Each media item contains core information such as title, category, status, rating, notes, and an optional cover image path. The application was developed using object-oriented programming principles, with a clear separation between the data model, database layer, command-line testing environment, and graphical user interface.

The system uses SQLite for permanent data storage, making it possible to save records, retrieve them later, search and sort them efficiently, update existing entries, and delete them when necessary. In addition, the graphical interface was designed with `tkinter` and includes a modern dark-themed layout with cover-based browsing, filtering tools, editing support, CSV export, and basic collection statistics.

Overall, the purpose of the project is to provide a practical and user-friendly way to track personal media consumption while demonstrating the implementation of database management, GUI development, validation, and error handling in Python.

## Getting Started

1. Clone this repository or download the project files.
2. Install the required Python packages if necessary.
3. Make sure the project follows object-oriented programming principles.

### 1) macOS app (`.app`)

- Download the provided **Media Library Tracker.app** or build it from source
- Open the generated **Media Library Tracker.app**
- Browse your media library through the graphical interface
- Use the available GUI features such as:
  - add new items
  - edit existing items
  - delete items
  - toggle item status
  - search, filter, and sort the collection
  - export filtered results to CSV
  - view category and completion statistics

> **Note:** The macOS application stores its SQLite database and exported files in the standard macOS application data location:
>
> `~/Library/Application Support/Media Library Tracker/`
> **Note:** Cover images used by the application can also be stored in:
>
> `~/Library/Application Support/Media Library Tracker/covers/`

---

### 2) Run from source (Python / CLI)

- Download or clone the full project folder
- Open a terminal in the project directory
- Move into the `Source_Code/src` folder
- Run the CLI version from the command line
```bash
python main.py
# or
python3 main.py
```
> **Note:**  The CLI version allows you to test the core functionality of the application directly from the terminal, including adding items, viewing records, deleting entries, searching, sorting, exporting to CSV, and displaying statistics.

## Tasks
- Define structure: Title, Category, Status, Rating, Notes. Choose storage method (SQLite or JSON).
- Add/view/delete items. Store records persistently.
- Implement sorting and searching by fields.
- Add "mark as watched/read" toggle.
- Add export filtered list to CSV button.
- Add optional image (poster/cover path). ?? 
- Add GUI using `tkinter`.
- Add statistics (total by category, watched vs. unwatched).
- Handle errors, test edge cases (missing data).
- Final testing. Create README with instructions and screenshots. Submit as Git repo.

## Estimated time to work 2 weeks
