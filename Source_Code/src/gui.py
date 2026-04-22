#This file contains the MediaLibraryGUI class which implements the graphical user interface for the media 
# library tracker application using Tkinter. The GUI allows users to view, add, edit, delete, and filter 
# media items in a visually appealing way. It includes a carousel display for media items, a details 
# panel for the selected item, and various controls for managing the media library. The class interacts 
# with the MediaDatabase to perform all data operations and updates the interface accordingly. The GUI is 
# designed to be user-friendly and responsive, providing an enjoyable experience for users to manage their 
# media collection.    


import os
import tkinter as tk
from tkinter import messagebox, filedialog

from PIL import Image, ImageTk, ImageOps

from database import MediaDatabase
from models import MediaItem, MediaConfig


class ItemDialog(tk.Toplevel):
    def __init__(self, parent, db: MediaDatabase, on_success, item=None):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.on_success = on_success
        self.item = item

        self.title("Edit Media Item" if item else "Add New Media Item")
        self.geometry("460x650")
        self.resizable(False, False)
        self.configure(bg="#14171A")

        self.title_var = tk.StringVar(value=item.title if item else "")
        self.category_var = tk.StringVar(
            value=item.category if item else MediaConfig.ALLOWED_CATEGORIES[0]
        )
        self.status_var = tk.StringVar(
            value=item.status if item else MediaConfig.ALLOWED_STATUSES[0]
        )
        self.rating_var = tk.StringVar(
            value="" if not item or item.rating is None else str(item.rating)
        )
        self.image_path_var = tk.StringVar(value=item.image_path if item else "")

        self._build()

        self.transient(parent)
        self.grab_set()
        self.focus()

    def _make_button(
        self,
        parent,
        text,
        command,
        bg,
        active_bg,
        fg="white",
        padx=16,
        pady=10,
        font=("Helvetica", 10, "bold")
    ):
        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            bd=0,
            relief="flat"
        )

        btn.bind("<Enter>", lambda _: btn.config(bg=active_bg))
        btn.bind("<Leave>", lambda _: btn.config(bg=bg))
        btn.bind("<Button-1>", lambda _: command())

        return btn

    def _build(self):
        container = tk.Frame(self, bg="#14171A")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            container,
            text="Edit Item" if self.item else "Add New Item",
            bg="#14171A",
            fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(anchor="w", pady=(0, 20))

        self._label(container, "Title")
        tk.Entry(
            container,
            textvariable=self.title_var,
            bg="#1E2329",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Helvetica", 11)
        ).pack(fill="x", pady=(0, 12), ipady=8)

        self._label(container, "Category")
        category_menu = tk.OptionMenu(container, self.category_var, *MediaConfig.ALLOWED_CATEGORIES)
        category_menu.config(
            bg="#1E2329",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            font=("Helvetica", 11)
        )
        category_menu["menu"].config(
            bg="#1E2329",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white"
        )
        category_menu.pack(fill="x", pady=(0, 12), ipady=4)

        self._label(container, "Status")
        status_menu = tk.OptionMenu(container, self.status_var, *MediaConfig.ALLOWED_STATUSES)
        status_menu.config(
            bg="#1E2329",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            font=("Helvetica", 11)
        )
        status_menu["menu"].config(
            bg="#1E2329",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white"
        )
        status_menu.pack(fill="x", pady=(0, 12), ipady=4)

        self._label(container, "Rating (0-10)")
        tk.Entry(
            container,
            textvariable=self.rating_var,
            bg="#1E2329",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Helvetica", 11)
        ).pack(fill="x", pady=(0, 12), ipady=8)

        self._label(container, "Notes")
        self.notes_text = tk.Text(
            container,
            height=6,
            bg="#1E2329",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Helvetica", 11),
            wrap="word"
        )
        self.notes_text.pack(fill="x", pady=(0, 12))
        if self.item and self.item.notes:
            self.notes_text.insert("1.0", self.item.notes)

        self._label(container, "Cover Path")
        path_row = tk.Frame(container, bg="#14171A")
        path_row.pack(fill="x", pady=(0, 18))

        tk.Entry(
            path_row,
            textvariable=self.image_path_var,
            bg="#1E2329",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Helvetica", 11)
        ).pack(side="left", fill="x", expand=True, ipady=8)

        self._make_button(
            path_row,
            text="Browse",
            command=self.browse_image,
            bg="#2E7CF6",
            active_bg="#4B91FF",
            padx=14,
            pady=8,
            font=("Helvetica", 10, "bold")
        ).pack(side="left", padx=(8, 0))

        buttons = tk.Frame(container, bg="#14171A")
        buttons.pack(fill="x")

        self._make_button(
            buttons,
            text="Cancel",
            command=self.destroy,
            bg="#2A2F36",
            active_bg="#3A414A"
        ).pack(side="right")

        self._make_button(
            buttons,
            text="Save Changes" if self.item else "Add Item",
            command=self.save_item,
            bg="#00A67E",
            active_bg="#1AB890"
        ).pack(side="right", padx=(0, 8))

    def _label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            bg="#14171A",
            fg="#D7DCE2",
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 6))

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose Cover Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")]
        )
        if file_path:
            self.image_path_var.set(file_path)

    def save_item(self):
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        status = self.status_var.get().strip()
        rating_text = self.rating_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        image_path = self.image_path_var.get().strip()

        rating = None
        if rating_text:
            try:
                rating = float(rating_text)
            except ValueError:
                messagebox.showerror("Invalid Rating", "Rating must be a number.")
                return

        try:
            media_item = MediaItem(
                title=title,
                category=category,
                status=status,
                rating=rating,
                notes=notes,
                image_path=image_path,
                item_id=self.item.item_id if self.item else None
            )

            if self.item:
                self.db.update_item(media_item)
            else:
                self.db.add_item(media_item)

            self.on_success()
            self.destroy()
        except ValueError as error:
            messagebox.showerror("Invalid Data", str(error))


class MediaLibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = MediaDatabase()
        self.title("Media Library Tracker")
        self.geometry("1500x900")
        self.minsize(1200, 760)
        self.configure(bg="#0E1114")

        self.filtered_items = []
        self.selected_index = 0
        self.cover_cache = {}

        self.search_var = tk.StringVar()
        self.category_filter_var = tk.StringVar(value="All")
        self.status_filter_var = tk.StringVar(value="All")
        self.sort_by_var = tk.StringVar(value="title")
        self.sort_order_var = tk.StringVar(value="ASC")

        self._build_ui()
        self.load_items()

        self.bind("<Left>", lambda e: self.move_left())
        self.bind("<Right>", lambda e: self.move_right())

    def _make_button(
        self,
        parent,
        text,
        command,
        bg,
        active_bg,
        fg="white",
        padx=16,
        pady=10,
        font=("Helvetica", 10, "bold"),
        width=None
    ):
        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            bd=0,
            relief="flat"
        )

        if width is not None:
            btn.config(width=width)

        btn.bind("<Enter>", lambda _: btn.config(bg=active_bg))
        btn.bind("<Leave>", lambda _: btn.config(bg=bg))
        btn.bind("<Button-1>", lambda _: command())

        return btn

    def _build_ui(self):
        self.topbar = tk.Frame(self, bg="#11161B", height=64)
        self.topbar.pack(fill="x", side="top")
        self.topbar.pack_propagate(False)

        tk.Label(
            self.topbar,
            text="Media Library Tracker",
            bg="#11161B",
            fg="white",
            font=("Helvetica", 20, "bold")
        ).pack(side="left", padx=24)

        self._make_button(
            self.topbar,
            text="+ Add",
            command=self.open_add_dialog,
            bg="#2E7CF6",
            active_bg="#4B91FF"
        ).pack(side="right", padx=(10, 20), pady=10)

        self._make_button(
            self.topbar,
            text="Delete",
            command=self.delete_selected,
            bg="#D9534F",
            active_bg="#E46A66"
        ).pack(side="right", padx=10, pady=10)

        self._make_button(
            self.topbar,
            text="Toggle Status",
            command=self.toggle_selected_status,
            bg="#2A2F36",
            active_bg="#3A414A"
        ).pack(side="right", padx=10, pady=10)

        self.filter_bar = tk.Frame(self, bg="#161B21", height=68)
        self.filter_bar.pack(fill="x", side="top")
        self.filter_bar.pack_propagate(False)

        tk.Entry(
            self.filter_bar,
            textvariable=self.search_var,
            bg="#222831",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Helvetica", 11)
        ).pack(side="left", padx=(20, 10), pady=14, ipadx=60, ipady=9)

        self._combobox(self.filter_bar, self.category_filter_var, ["All"] + MediaConfig.ALLOWED_CATEGORIES).pack(
            side="left", padx=10, pady=14
        )
        self._combobox(self.filter_bar, self.status_filter_var, ["All"] + MediaConfig.ALLOWED_STATUSES).pack(
            side="left", padx=10, pady=14
        )
        self._combobox(self.filter_bar, self.sort_by_var, ["title", "category", "status", "rating"]).pack(
            side="left", padx=10, pady=14
        )
        self._combobox(self.filter_bar, self.sort_order_var, ["ASC", "DESC"]).pack(
            side="left", padx=10, pady=14
        )

        self._make_button(
            self.filter_bar,
            text="Apply",
            command=self.load_items,
            bg="#00A67E",
            active_bg="#1AB890"
        ).pack(side="left", padx=10, pady=14)

        self._make_button(
            self.filter_bar,
            text="Export CSV",
            command=self.export_filtered,
            bg="#2A2F36",
            active_bg="#3A414A"
        ).pack(side="left", padx=10, pady=14)

        self._make_button(
            self.filter_bar,
            text="Reset",
            command=self.reset_filters,
            bg="#2A2F36",
            active_bg="#3A414A"
        ).pack(side="left", padx=10, pady=14)

        self.stats_frame = tk.Frame(self, bg="#12171C", height=34)
        self.stats_frame.pack(fill="x", side="top")
        self.stats_frame.pack_propagate(False)

        self.stats_category_label = tk.Label(
            self.stats_frame,
            text="By category: -",
            bg="#12171C",
            fg="#DCE2E8",
            font=("Helvetica", 10),
            anchor="w",
            justify="left"
        )
        self.stats_category_label.pack(side="left", padx=20, pady=6)

        self.stats_completion_label = tk.Label(
            self.stats_frame,
            text="Completed: 0 | Not completed: 0",
            bg="#12171C",
            fg="#DCE2E8",
            font=("Helvetica", 10, "bold"),
            anchor="e",
            justify="right"
        )
        self.stats_completion_label.pack(side="right", padx=20, pady=6)

        self.center_frame = tk.Frame(self, bg="#0E1114")
        self.center_frame.pack(fill="both", expand=True)

        self.carousel_frame = tk.Frame(self.center_frame, bg="#0E1114", height=360)
        self.carousel_frame.pack(fill="x", expand=False, pady=(10, 8))
        self.carousel_frame.pack_propagate(False)

        self.nav_frame = tk.Frame(self.center_frame, bg="#0E1114")
        self.nav_frame.pack(fill="x", pady=(0, 8))

        self._make_button(
            self.nav_frame,
            text="◀",
            command=self.move_left,
            bg="#1D232A",
            active_bg="#303844",
            font=("Helvetica", 18, "bold"),
            width=4
        ).pack(side="left", padx=(25, 10))

        self.status_info_label = tk.Label(
            self.nav_frame,
            text="0 items",
            bg="#0E1114",
            fg="#C7CFD9",
            font=("Helvetica", 11)
        )
        self.status_info_label.pack(side="left", padx=8)

        self._make_button(
            self.nav_frame,
            text="▶",
            command=self.move_right,
            bg="#1D232A",
            active_bg="#303844",
            font=("Helvetica", 18, "bold"),
            width=4
        ).pack(side="right", padx=(10, 25))

        self.details_frame = tk.Frame(self, bg="#14191F", height=170)
        self.details_frame.pack(fill="x", side="bottom")
        self.details_frame.pack_propagate(False)

        self._build_details_panel()

    def _combobox(self, parent, variable, values):
        box = tk.OptionMenu(parent, variable, *values)
        box.config(
            bg="#222831",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Helvetica", 11),
            width=14
        )
        box["menu"].config(
            bg="#222831",
            fg="white",
            activebackground="#2E7CF6",
            activeforeground="white"
        )
        return box

    def _build_details_panel(self):
        left = tk.Frame(self.details_frame, bg="#14191F")
        left.pack(side="left", fill="both", expand=True, padx=24, pady=16)

        self.details_title = tk.Label(
            left,
            text="No item selected",
            bg="#14191F",
            fg="white",
            font=("Helvetica", 18, "bold"),
            anchor="w"
        )
        self.details_title.pack(fill="x", pady=(0, 8))

        self.details_meta = tk.Label(
            left,
            text="Category: -   |   Status: -   |   Rating: -",
            bg="#14191F",
            fg="#C8D0D9",
            font=("Helvetica", 11),
            anchor="w"
        )
        self.details_meta.pack(fill="x", pady=(0, 8))

        self.details_notes = tk.Label(
            left,
            text="Notes: -",
            bg="#14191F",
            fg="#DCE2E8",
            font=("Helvetica", 11),
            anchor="w",
            justify="left",
            wraplength=900
        )
        self.details_notes.pack(fill="x")

        right = tk.Frame(self.details_frame, bg="#14191F")
        right.pack(side="right", padx=24, pady=16, anchor="n")

        self.details_path = tk.Label(
            right,
            text="Cover path: -",
            bg="#14191F",
            fg="#9FA9B5",
            font=("Helvetica", 10),
            justify="right",
            anchor="e",
            wraplength=300
        )
        self.details_path.pack(anchor="e", pady=(0, 10))

        self._make_button(
            right,
            text="Edit Selected",
            command=self.open_edit_dialog,
            bg="#2E7CF6",
            active_bg="#4B91FF"
        ).pack(anchor="e")

    def load_items(self):
        title_query = self.search_var.get().strip()
        category = self.category_filter_var.get().strip()
        status = self.status_filter_var.get().strip()
        sort_by = self.sort_by_var.get().strip()
        sort_order = self.sort_order_var.get().strip()

        if title_query or category != "All" or status != "All":
            items = self.db.search_items(
                title=title_query,
                category="" if category == "All" else category,
                status="" if status == "All" else status
            )
            items = self._sort_loaded_items(items, sort_by, sort_order)
        else:
            items = self.db.sort_items(sort_by=sort_by, order=sort_order)

        self.filtered_items = items
        self.selected_index = 0 if items else -1
        self.render_carousel()
        self.update_details()
        self.update_statistics()

    def _sort_loaded_items(self, items, sort_by, sort_order):
        reverse = sort_order == "DESC"

        def key_func(item):
            value = getattr(item, sort_by)
            if value is None:
                return -1 if sort_by == "rating" else ""
            return value

        return sorted(items, key=key_func, reverse=reverse)

    def render_carousel(self):
        for widget in self.carousel_frame.winfo_children():
            widget.destroy()

        if not self.filtered_items:
            tk.Label(
                self.carousel_frame,
                text="No items found",
                bg="#0E1114",
                fg="#B8C1CB",
                font=("Helvetica", 18, "bold")
            ).place(relx=0.5, rely=0.5, anchor="center")
            self.status_info_label.config(text="0 items")
            return

        self.status_info_label.config(
            text=f"{len(self.filtered_items)} items   |   Selected: {self.selected_index + 1}/{len(self.filtered_items)}"
        )

        frame_width = max(self.carousel_frame.winfo_width(), 1200)
        center_x = frame_width // 2
        center_y = 155

        visible_offsets = [-3, -2, -1, 0, 1, 2, 3]
        for offset in visible_offsets:
            index = self.selected_index + offset
            if index < 0 or index >= len(self.filtered_items):
                continue

            item = self.filtered_items[index]

            if offset == 0:
                width, height = 190, 270
                x = center_x
                y = center_y
                border = "#5A616B"
                text_color = "white"
            else:
                factor = max(0.6, 1 - abs(offset) * 0.13)
                width = int(190 * factor)
                height = int(270 * factor)
                x = center_x + (offset * 145)
                y = center_y + abs(offset) * 12
                border = "#2B3138"
                text_color = "#B9C2CB"

            image = self.load_cover(item.image_path, (width, height))
            label = tk.Label(
                self.carousel_frame,
                image=image,
                bg="#0E1114",
                bd=0,
                highlightthickness=1,
                highlightbackground=border,
                cursor="hand2"
            )
            label.image = image
            label.place(x=x, y=y, anchor="center")
            label.bind("<Button-1>", lambda e, idx=index: self.select_index(idx))

            title = tk.Label(
                self.carousel_frame,
                text=item.title,
                bg="#0E1114",
                fg=text_color,
                font=("Helvetica", 12 if offset == 0 else 10, "bold"),
                wraplength=170,
                justify="center",
                cursor="hand2"
            )
            title.place(x=x, y=y + (height // 2) + 20, anchor="center")
            title.bind("<Button-1>", lambda e, idx=index: self.select_index(idx))

    def load_cover(self, path, size):
        cache_key = (path, size)
        if cache_key in self.cover_cache:
            return self.cover_cache[cache_key]

        try:
            if path and os.path.exists(path):
                image = Image.open(path).convert("RGB")
                image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            else:
                image = Image.new("RGB", size, "#232A32")
        except Exception:
            image = Image.new("RGB", size, "#232A32")

        photo = ImageTk.PhotoImage(image)
        self.cover_cache[cache_key] = photo
        return photo

    def select_index(self, index):
        if 0 <= index < len(self.filtered_items):
            self.selected_index = index
            self.render_carousel()
            self.update_details()

    def move_left(self):
        if not self.filtered_items:
            return
        self.selected_index = (self.selected_index - 1) % len(self.filtered_items)
        self.render_carousel()
        self.update_details()

    def move_right(self):
        if not self.filtered_items:
            return
        self.selected_index = (self.selected_index + 1) % len(self.filtered_items)
        self.render_carousel()
        self.update_details()

    def update_details(self):
        if not self.filtered_items or self.selected_index < 0:
            self.details_title.config(text="No item selected")
            self.details_meta.config(text="Category: -   |   Status: -   |   Rating: -")
            self.details_notes.config(text="Notes: -")
            self.details_path.config(text="Cover path: -")
            return

        item = self.filtered_items[self.selected_index]
        rating_text = item.rating if item.rating is not None else "-"

        self.details_title.config(text=item.title)
        self.details_meta.config(
            text=f"Category: {item.category}   |   Status: {item.status}   |   Rating: {rating_text}"
        )
        self.details_notes.config(text=f"Notes: {item.notes if item.notes else '-'}")
        self.details_path.config(text=f"Cover path: {item.image_path if item.image_path else '-'}")

    def update_statistics(self):
        stats = self.db.get_all_statistics()
        category_stats = stats["by_category"]
        completion_stats = stats["completion"]

        if category_stats:
            category_text = " | ".join(
                [f"{category}: {count}" for category, count in category_stats.items()]
            )
        else:
            category_text = "No items"

        self.stats_category_label.config(text=f"By category: {category_text}")
        self.stats_completion_label.config(
            text=f"Completed: {completion_stats['completed']}   |   Not completed: {completion_stats['not_completed']}"
        )

    def get_selected_item(self):
        if not self.filtered_items or self.selected_index < 0:
            return None
        return self.filtered_items[self.selected_index]

    def delete_selected(self):
        item = self.get_selected_item()
        if item is None:
            messagebox.showwarning("No Item", "There is no selected item.")
            return

        confirm = messagebox.askyesno("Delete", f"Delete '{item.title}'?")
        if not confirm:
            return

        self.db.delete_item(item.item_id)
        self.load_items()

    def toggle_selected_status(self):
        item = self.get_selected_item()
        if item is None:
            messagebox.showwarning("No Item", "There is no selected item.")
            return

        self.db.toggle_completed_status(item.item_id)
        self.load_items()

    def open_add_dialog(self):
        ItemDialog(self, self.db, self.load_items)

    def open_edit_dialog(self):
        item = self.get_selected_item()
        if item is None:
            messagebox.showwarning("No Item", "There is no selected item.")
            return

        ItemDialog(self, self.db, self.load_items, item=item)

    def export_filtered(self):
        if not self.filtered_items:
            messagebox.showwarning("No Items", "There are no items to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export Filtered Items",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        base_name = os.path.basename(file_path)
        temp_path = self.db.export_items_to_csv(self.filtered_items, base_name)

        if os.path.abspath(temp_path) != os.path.abspath(file_path):
            with open(temp_path, "rb") as src:
                data = src.read()
            with open(file_path, "wb") as dst:
                dst.write(data)

        messagebox.showinfo("Export Complete", f"CSV exported to:\n{file_path}")

    def reset_filters(self):
        self.search_var.set("")
        self.category_filter_var.set("All")
        self.status_filter_var.set("All")
        self.sort_by_var.set("title")
        self.sort_order_var.set("ASC")
        self.load_items()


if __name__ == "__main__":
    app = MediaLibraryGUI()
    app.mainloop()