
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database import get_connection
from receipt import generate_receipt, open_receipt


class OrderHistory:

    def __init__(self, parent, on_back):

        self.parent = parent
        self.on_back = on_back
        self.selected_order_id = None

        self.create_history_screen()


    # ==========================================
    # MAIN SCREEN
    # ==========================================

    def create_history_screen(self):

        self.parent.configure(bg="#F1F5F9")

        header = tk.Frame(
            self.parent,
            bg="white",
            height=75
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 12)
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="Order History",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#17324D"
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

        self.create_search_section()

        self.body = tk.Frame(
            self.parent,
            bg="#F1F5F9"
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(0, weight=3)
        self.body.grid_rowconfigure(1, weight=2)

        self.create_orders_table()
        self.create_order_details()

        self.refresh_history()


    # ==========================================
    # SEARCH SECTION
    # ==========================================

    def create_search_section(self):

        search_frame = tk.Frame(
            self.parent,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search Orders:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            side="left",
            padx=15,
            pady=14
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

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_orders()
        )

        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.search_orders
        ).pack(
            side="left",
            padx=5,
            ipadx=12,
            ipady=7
        )

        tk.Button(
            search_frame,
            text="Show All",
            font=("Arial", 10, "bold"),
            bg="#64748B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_search
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=7
        )


    # ==========================================
    # ORDERS TABLE
    # ==========================================

    def create_orders_table(self):

        orders_frame = tk.Frame(
            self.body,
            bg="white"
        )

        orders_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        orders_frame.grid_columnconfigure(0, weight=1)
        orders_frame.grid_rowconfigure(1, weight=1)

        tk.Label(
            orders_frame,
            text="All Customer Orders",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#17324D"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=12
        )

        table_area = tk.Frame(
            orders_frame,
            bg="white"
        )

        table_area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 12)
        )

        table_area.grid_rowconfigure(0, weight=1)
        table_area.grid_columnconfigure(0, weight=1)

        columns = (
            "Order ID",
            "Customer",
            "Mobile",
            "Order Type",
            "Payment",
            "Amount",
            "Date"
        )

        self.orders_table = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            height=6
        )

        widths = {
            "Order ID": 65,
            "Customer": 130,
            "Mobile": 100,
            "Order Type": 95,
            "Payment": 85,
            "Amount": 100,
            "Date": 145
        }

        for col in columns:

            self.orders_table.heading(
                col,
                text=col
            )

            self.orders_table.column(
                col,
                width=widths[col],
                minwidth=60,
                anchor="center",
                stretch=True
            )

        scrollbar_y = ttk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.orders_table.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_area,
            orient="horizontal",
            command=self.orders_table.xview
        )

        self.orders_table.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.orders_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.orders_table.bind(
            "<<TreeviewSelect>>",
            self.show_order_details
        )


    # ==========================================
    # SELECTED ORDER DETAILS
    # ==========================================

    def create_order_details(self):

        details_frame = tk.Frame(
            self.body,
            bg="white"
        )

        details_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        title_bar = tk.Frame(
            details_frame,
            bg="white"
        )

        title_bar.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        tk.Label(
            title_bar,
            text="Selected Order Details",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(side="left")

        self.receipt_button = tk.Button(
            title_bar,
            text="Generate PDF Receipt",
            font=("Arial", 9, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.generate_selected_receipt,
            state="disabled"
        )

        self.receipt_button.pack(
            side="right",
            ipadx=10,
            ipady=6
        )

        self.order_info = tk.Label(
            details_frame,
            text="Select an order from the above table.",
            font=("Arial", 10),
            bg="white",
            fg="#64748B",
            anchor="w",
            justify="left"
        )

        self.order_info.pack(
            fill="x",
            padx=15,
            pady=5
        )

        item_frame = tk.Frame(
            details_frame,
            bg="white"
        )

        item_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        item_frame.grid_rowconfigure(0, weight=1)
        item_frame.grid_columnconfigure(0, weight=1)

        columns = (
            "Food Item",
            "Quantity",
            "Unit Price",
            "Item Total"
        )

        self.items_table = ttk.Treeview(
            item_frame,
            columns=columns,
            show="headings",
            height=4
        )

        widths = {
            "Food Item": 250,
            "Quantity": 100,
            "Unit Price": 130,
            "Item Total": 130
        }

        for col in columns:

            self.items_table.heading(
                col,
                text=col
            )

            self.items_table.column(
                col,
                width=widths[col],
                minwidth=60,
                anchor="center",
                stretch=True
            )

        scrollbar = ttk.Scrollbar(
            item_frame,
            orient="vertical",
            command=self.items_table.yview
        )

        self.items_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.items_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        summary_frame = tk.Frame(
            details_frame,
            bg="#F1F5F9"
        )

        summary_frame.pack(
            fill="x",
            padx=12,
            pady=(5, 12)
        )

        self.bill_summary = tk.Label(
            summary_frame,
            text="Subtotal: ₹0.00    Discount: ₹0.00    "
                 "Tax: ₹0.00    Grand Total: ₹0.00",
            font=("Arial", 10, "bold"),
            bg="#F1F5F9",
            fg="#17324D",
            anchor="w"
        )

        self.bill_summary.pack(
            fill="x",
            padx=10,
            pady=10
        )


    # ==========================================
    # LOAD ORDERS
    # ==========================================

    def refresh_history(self, search_text=""):

        conn = None

        try:

            conn = get_connection()

            if search_text:

                search_value = f"%{search_text}%"

                orders = conn.execute("""

                    SELECT
                        o.order_id,
                        COALESCE(c.name, 'Walk-in Customer'),
                        COALESCE(c.phone, ''),
                        o.order_type,
                        o.payment_method,
                        o.grand_total,
                        o.created_at

                    FROM orders o

                    LEFT JOIN customers c
                    ON o.customer_id = c.customer_id

                    WHERE
                        CAST(o.order_id AS TEXT) LIKE ?
                        OR COALESCE(c.name, '') LIKE ?
                        OR COALESCE(c.phone, '') LIKE ?
                        OR o.payment_method LIKE ?
                        OR o.order_type LIKE ?
                        OR o.created_at LIKE ?

                    ORDER BY o.order_id DESC

                """, (
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value
                )).fetchall()

            else:

                orders = conn.execute("""

                    SELECT
                        o.order_id,
                        COALESCE(c.name, 'Walk-in Customer'),
                        COALESCE(c.phone, ''),
                        o.order_type,
                        o.payment_method,
                        o.grand_total,
                        o.created_at

                    FROM orders o

                    LEFT JOIN customers c
                    ON o.customer_id = c.customer_id

                    ORDER BY o.order_id DESC

                """).fetchall()

            for row in self.orders_table.get_children():
                self.orders_table.delete(row)

            for order in orders:

                self.orders_table.insert(
                    "",
                    "end",
                    values=(
                        order[0],
                        order[1],
                        order[2] or "-",
                        order[3],
                        order[4],
                        f"₹{order[5]:,.2f}",
                        order[6]
                    )
                )

            self.clear_order_details()

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            if conn:
                conn.close()


    # ==========================================
    # SEARCH
    # ==========================================

    def search_orders(self):

        search_text = self.search_entry.get().strip()

        self.refresh_history(search_text)


    def clear_search(self):

        self.search_entry.delete(0, tk.END)

        self.refresh_history()


    # ==========================================
    # SHOW SELECTED ORDER DETAILS
    # ==========================================

    def show_order_details(self, event=None):

        selected = self.orders_table.selection()

        if not selected:
            return

        values = self.orders_table.item(
            selected[0],
            "values"
        )

        if not values or not str(values[0]).isdigit():
            return

        order_id = int(values[0])

        conn = None

        try:

            conn = get_connection()

            order = conn.execute("""

                SELECT
                    o.order_id,
                    COALESCE(c.name, 'Walk-in Customer'),
                    COALESCE(c.phone, ''),
                    o.order_type,
                    o.payment_method,
                    o.subtotal,
                    o.discount,
                    o.tax_rate,
                    o.tax_amount,
                    o.grand_total,
                    o.created_at

                FROM orders o

                LEFT JOIN customers c
                ON o.customer_id = c.customer_id

                WHERE o.order_id = ?

            """, (order_id,)).fetchone()

            if order is None:
                return

            items = conn.execute("""

                SELECT
                    item_name,
                    quantity,
                    unit_price,
                    item_total

                FROM order_items

                WHERE order_id = ?

                ORDER BY id

            """, (order_id,)).fetchall()

            self.selected_order_id = order_id

            self.receipt_button.config(
                state="normal"
            )

            self.order_info.config(

                text=(
                    f"Order #{order[0]}    "
                    f"Customer: {order[1]}    "
                    f"Mobile: {order[2] or '-'}    "
                    f"Type: {order[3]}    "
                    f"Payment: {order[4]}    "
                    f"Date: {order[10]}"
                )
            )

            for row in self.items_table.get_children():
                self.items_table.delete(row)

            for item in items:

                self.items_table.insert(
                    "",
                    "end",
                    values=(
                        item[0],
                        item[1],
                        f"₹{item[2]:,.2f}",
                        f"₹{item[3]:,.2f}"
                    )
                )

            self.bill_summary.config(

                text=(
                    f"Subtotal: ₹{order[5]:,.2f}     "
                    f"Discount: ₹{order[6]:,.2f}     "
                    f"Tax ({order[7]}%): ₹{order[8]:,.2f}     "
                    f"Grand Total: ₹{order[9]:,.2f}"
                )
            )

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.parent
            )

        finally:

            if conn:
                conn.close()


    # ==========================================
    # GENERATE PDF RECEIPT
    # ==========================================

    def generate_selected_receipt(self):

        if self.selected_order_id is None:

            messagebox.showwarning(
                "Select Order",
                "Please select an order first.",
                parent=self.parent
            )

            return

        try:

            pdf_path = generate_receipt(
                self.selected_order_id
            )

            open_now = messagebox.askyesno(
                "Receipt Generated",
                f"PDF receipt generated successfully!\n\n"
                f"Saved at:\n{pdf_path}\n\n"
                f"Do you want to open it now?",
                parent=self.parent
            )

            if open_now:

                opened = open_receipt(pdf_path)

                if not opened:

                    messagebox.showinfo(
                        "PDF Saved",
                        "Receipt saved successfully. "
                        "Please open it from the bills folder.",
                        parent=self.parent
                    )

        except Exception as e:

            messagebox.showerror(
                "Receipt Error",
                str(e),
                parent=self.parent
            )


    # ==========================================
    # CLEAR ORDER DETAILS
    # ==========================================

    def clear_order_details(self):

        self.selected_order_id = None

        for row in self.items_table.get_children():
            self.items_table.delete(row)

        self.order_info.config(
            text="Select an order from the above table."
        )

        self.bill_summary.config(
            text=(
                "Subtotal: ₹0.00    "
                "Discount: ₹0.00    "
                "Tax: ₹0.00    "
                "Grand Total: ₹0.00"
            )
        )

        self.receipt_button.config(
            state="disabled"
        )
