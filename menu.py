
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database import get_connection


class MenuManagement:

    def __init__(self, parent, on_back):

        self.parent = parent
        self.on_back = on_back

        self.selected_item_id = None

        self.create_menu_screen()


    # ==========================================
    # MAIN MENU SCREEN
    # ==========================================

    def create_menu_screen(self):

        self.parent.configure(bg="#F1F5F9")

        # Header
        header = tk.Frame(
            self.parent,
            bg="white",
            height=75
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="Manage Menu",
            font=("Arial", 23, "bold"),
            fg="#17324D",
            bg="white"
        ).pack(
            side="left",
            padx=20
        )

        tk.Button(
            header,
            text="Back to Dashboard",
            font=("Arial", 10, "bold"),
            bg="#17324D",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.on_back
        ).pack(
            side="right",
            padx=20,
            pady=18,
            ipadx=10,
            ipady=5
        )


        # Main content
        main_frame = tk.Frame(
            self.parent,
            bg="#F1F5F9"
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )


        # Item form
        self.create_form(main_frame)

        # Search section
        self.create_search_section(main_frame)

        # Menu table
        self.create_menu_table(main_frame)

        # Load data
        self.refresh_items()


    # ==========================================
    # ADD / UPDATE FORM
    # ==========================================

    def create_form(self, parent):

        form_frame = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        form_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            form_frame,
            text="Food Item Details",
            font=("Arial", 16, "bold"),
            fg="#17324D",
            bg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 12)
        )


        # Input fields container
        fields_frame = tk.Frame(
            form_frame,
            bg="white"
        )

        fields_frame.pack(
            fill="x",
            padx=20
        )

        for column in range(3):

            fields_frame.grid_columnconfigure(
                column,
                weight=1
            )


        # Food name
        tk.Label(
            fields_frame,
            text="Food Name",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=8
        )

        self.name_entry = tk.Entry(
            fields_frame,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=8,
            ipady=7
        )


        # Category
        tk.Label(
            fields_frame,
            text="Category",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=8
        )

        self.category_box = ttk.Combobox(
            fields_frame,
            font=("Arial", 11),
            values=[
                "Fast Food",
                "Snacks",
                "Drinks",
                "Main Course",
                "Desserts",
                "Other"
            ],
            state="readonly"
        )

        self.category_box.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=8,
            pady=8,
            ipady=5
        )

        self.category_box.set("Fast Food")


        # Price
        tk.Label(
            fields_frame,
            text="Price (₹)",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=8
        )

        self.price_entry = tk.Entry(
            fields_frame,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.price_entry.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=8,
            pady=8,
            ipady=7
        )


        # Buttons container
        button_frame = tk.Frame(
            form_frame,
            bg="white"
        )

        button_frame.pack(
            anchor="w",
            padx=25,
            pady=15
        )


        # Add button
        tk.Button(
            button_frame,
            text="Add Item",
            font=("Arial", 10, "bold"),
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.add_item
        ).pack(
            side="left",
            padx=5,
            ipadx=15,
            ipady=8
        )


        # Update button
        tk.Button(
            button_frame,
            text="Update Item",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.update_item
        ).pack(
            side="left",
            padx=5,
            ipadx=15,
            ipady=8
        )


        # Delete button
        tk.Button(
            button_frame,
            text="Delete Item",
            font=("Arial", 10, "bold"),
            bg="#DC2626",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.delete_item
        ).pack(
            side="left",
            padx=5,
            ipadx=15,
            ipady=8
        )


        # Clear button
        tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 10, "bold"),
            bg="#64748B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_fields
        ).pack(
            side="left",
            padx=5,
            ipadx=15,
            ipady=8
        )


    # ==========================================
    # SEARCH SECTION
    # ==========================================

    def create_search_section(self, parent):

        search_frame = tk.Frame(
            parent,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            search_frame,
            text="Search Food Item",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            side="left",
            padx=15,
            pady=15
        )


        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            ipady=7
        )


        # Search button
        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.search_items
        ).pack(
            side="left",
            padx=5,
            ipadx=12,
            ipady=6
        )


        # Show all button
        tk.Button(
            search_frame,
            text="Show All",
            font=("Arial", 10, "bold"),
            bg="#64748B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.refresh_items
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=6
        )


    # ==========================================
    # MENU TABLE
    # ==========================================

    def create_menu_table(self, parent):

        table_frame = tk.Frame(
            parent,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            table_frame,
            text="Food Items List",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )


        # Treeview styling
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )


        columns = (
            "ID",
            "Food Name",
            "Category",
            "Price",
            "Status"
        )

        self.menu_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )


        column_widths = {
            "ID": 60,
            "Food Name": 200,
            "Category": 160,
            "Price": 120,
            "Status": 120
        }

        for col in columns:

            self.menu_table.heading(
                col,
                text=col
            )

            self.menu_table.column(
                col,
                width=column_widths[col],
                minwidth=60,
                anchor="center",
                stretch=True
            )


        # Status colors
        self.menu_table.tag_configure(
            "unavailable",
            foreground="#DC2626"
        )

        self.menu_table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        # Select row event
        self.menu_table.bind(
            "<<TreeviewSelect>>",
            self.select_item
        )


    # ==========================================
    # VALIDATE FORM
    # ==========================================

    def get_form_data(self):

        name = self.name_entry.get().strip()

        category = self.category_box.get().strip()

        price_text = self.price_entry.get().strip()


        if not name:

            messagebox.showwarning(
                "Validation",
                "Please enter food name.",
                parent=self.parent
            )

            return None


        if not category:

            messagebox.showwarning(
                "Validation",
                "Please select category.",
                parent=self.parent
            )

            return None


        try:

            price = float(price_text)

            if price <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Validation",
                "Please enter a valid price greater than zero.",
                parent=self.parent
            )

            return None


        return name, category, price


    # ==========================================
    # ADD FOOD ITEM
    # ==========================================

    def add_item(self):

        data = self.get_form_data()

        if data is None:
            return

        name, category, price = data

        conn = get_connection()

        try:

            conn.execute("""
                INSERT INTO menu_items
                (item_name, category, price)
                VALUES (?, ?, ?)
            """, (name, category, price))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Food item added successfully!",
                parent=self.parent
            )

            self.clear_fields()
            self.refresh_items()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "This food item already exists.",
                parent=self.parent
            )

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            conn.close()


    # ==========================================
    # SELECT FOOD ITEM
    # ==========================================

    def select_item(self, event):

        selected = self.menu_table.selection()

        if not selected:
            return

        values = self.menu_table.item(
            selected[0],
            "values"
        )

        self.selected_item_id = int(values[0])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.category_box.set(values[2])

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(
            0,
            str(float(values[3]))
        )


    # ==========================================
    # UPDATE FOOD ITEM
    # ==========================================

    def update_item(self):

        if self.selected_item_id is None:

            messagebox.showwarning(
                "Select Item",
                "Please select an item from the table first.",
                parent=self.parent
            )

            return


        data = self.get_form_data()

        if data is None:
            return

        name, category, price = data

        conn = get_connection()

        try:

            conn.execute("""
                UPDATE menu_items

                SET item_name = ?,
                    category = ?,
                    price = ?

                WHERE item_id = ?

            """, (
                name,
                category,
                price,
                self.selected_item_id
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Food item updated successfully!",
                parent=self.parent
            )

            self.clear_fields()
            self.refresh_items()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Another item with this name already exists.",
                parent=self.parent
            )

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            conn.close()


    # ==========================================
    # DELETE FOOD ITEM
    # ==========================================

    def delete_item(self):

        if self.selected_item_id is None:

            messagebox.showwarning(
                "Select Item",
                "Please select an item first.",
                parent=self.parent
            )

            return


        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to remove this food item?",
            parent=self.parent
        )

        if not answer:
            return


        conn = get_connection()

        try:

            try:

                conn.execute("""
                    DELETE FROM menu_items
                    WHERE item_id = ?
                """, (self.selected_item_id,))

                conn.commit()

                message = "Food item deleted successfully!"

            except sqlite3.IntegrityError:

                # Preserve old order history
                conn.execute("""
                    UPDATE menu_items
                    SET is_available = 0
                    WHERE item_id = ?
                """, (self.selected_item_id,))

                conn.commit()

                message = (
                    "This item exists in previous orders. "
                    "It has been marked unavailable "
                    "to preserve order history."
                )


            messagebox.showinfo(
                "Success",
                message,
                parent=self.parent
            )

            self.clear_fields()
            self.refresh_items()

        except sqlite3.Error as e:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            conn.close()


    # ==========================================
    # SEARCH FOOD ITEM
    # ==========================================

    def search_items(self):

        search_text = self.search_entry.get().strip()

        self.refresh_items(search_text)


    # ==========================================
    # REFRESH MENU TABLE
    # ==========================================

    def refresh_items(self, search_text=""):

        conn = get_connection()

        try:

            if search_text:

                items = conn.execute("""

                    SELECT
                        item_id,
                        item_name,
                        category,
                        price,
                        is_available

                    FROM menu_items

                    WHERE item_name LIKE ?
                    OR category LIKE ?

                    ORDER BY item_id DESC

                """, (
                    f"%{search_text}%",
                    f"%{search_text}%"
                )).fetchall()

            else:

                items = conn.execute("""

                    SELECT
                        item_id,
                        item_name,
                        category,
                        price,
                        is_available

                    FROM menu_items

                    ORDER BY item_id DESC

                """).fetchall()


            # Clear old rows
            for row in self.menu_table.get_children():

                self.menu_table.delete(row)


            # Add new rows
            for item in items:

                status = (
                    "Available"
                    if item["is_available"] == 1
                    else "Unavailable"
                )

                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        item["item_id"],
                        item["item_name"],
                        item["category"],
                        f"{item['price']:.2f}",
                        status
                    ),
                    tags=(
                        "normal"
                        if item["is_available"] == 1
                        else "unavailable"
                    )
                )

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            conn.close()


    # ==========================================
    # CLEAR FORM
    # ==========================================

    def clear_fields(self):

        self.selected_item_id = None

        self.name_entry.delete(0, tk.END)

        self.category_box.set("Fast Food")

        self.price_entry.delete(0, tk.END)

        for selected in self.menu_table.selection():

            self.menu_table.selection_remove(selected)
