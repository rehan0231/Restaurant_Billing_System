
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from database import get_connection


class OrderManagement:

    def __init__(self, parent, on_back):

        self.parent = parent
        self.on_back = on_back

        # Cart stores selected food items
        self.cart = {}

        self.create_order_screen()


    # ==========================================
    # MAIN ORDER SCREEN
    # ==========================================

    def create_order_screen(self):

        self.parent.configure(bg="#F1F5F9")

        # Header
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
            text="New Customer Order",
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

        # Customer information
        self.create_customer_section()

        # Main content
        body = tk.Frame(
            self.parent,
            bg="#F1F5F9"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )

        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # Menu section
        self.create_menu_section(body)

        # Cart and billing section
        self.create_cart_section(body)

        # Load available menu items
        self.refresh_menu()


    # ==========================================
    # CUSTOMER INFORMATION
    # ==========================================

    def create_customer_section(self):

        customer_frame = tk.Frame(
            self.parent,
            bg="white"
        )

        customer_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        for column in range(3):

            customer_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # Customer name
        tk.Label(
            customer_frame,
            text="Customer Name (Optional)",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=(10, 3)
        )

        self.customer_name_entry = tk.Entry(
            customer_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.customer_name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(2, 12),
            ipady=6
        )

        # Customer mobile
        tk.Label(
            customer_frame,
            text="Mobile Number (Optional)",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=12,
            pady=(10, 3)
        )

        self.phone_entry = tk.Entry(
            customer_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.phone_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=12,
            pady=(2, 12),
            ipady=6
        )

        # Order type
        tk.Label(
            customer_frame,
            text="Order Type",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=12,
            pady=(10, 3)
        )

        self.order_type_box = ttk.Combobox(
            customer_frame,
            font=("Arial", 11),
            values=["Dine-in", "Takeaway"],
            state="readonly"
        )

        self.order_type_box.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=12,
            pady=(2, 12),
            ipady=5
        )

        self.order_type_box.set("Dine-in")


    # ==========================================
    # MENU SECTION
    # ==========================================

    def create_menu_section(self, parent):

        menu_frame = tk.Frame(
            parent,
            bg="white"
        )

        menu_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        tk.Label(
            menu_frame,
            text="Available Food Items",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        # Search row
        search_frame = tk.Frame(
            menu_frame,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.menu_search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.menu_search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        self.menu_search_entry.bind(
            "<Return>",
            lambda event: self.search_menu()
        )

        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 9, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.search_menu
        ).pack(
            side="left",
            padx=5,
            ipady=7,
            ipadx=8
        )

        tk.Button(
            search_frame,
            text="All",
            font=("Arial", 9, "bold"),
            bg="#64748B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.refresh_menu()
        ).pack(
            side="left",
            ipadx=8,
            ipady=7
        )


        # Menu table
        table_frame = tk.Frame(
            menu_frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = (
            "ID",
            "Food Item",
            "Category",
            "Price"
        )

        self.menu_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        widths = {
            "ID": 45,
            "Food Item": 150,
            "Category": 110,
            "Price": 85
        }

        for col in columns:

            self.menu_table.heading(
                col,
                text=col
            )

            self.menu_table.column(
                col,
                width=widths[col],
                minwidth=45,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.menu_table.yview
        )

        self.menu_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.menu_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )


        # Quantity and add button
        add_frame = tk.Frame(
            menu_frame,
            bg="white"
        )

        add_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            add_frame,
            text="Quantity:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left"
        )

        self.quantity_entry = tk.Entry(
            add_frame,
            font=("Arial", 11),
            width=6,
            justify="center",
            relief="solid",
            bd=1
        )

        self.quantity_entry.pack(
            side="left",
            padx=10,
            ipady=5
        )

        self.quantity_entry.insert(0, "1")

        tk.Button(
            add_frame,
            text="Add to Cart",
            font=("Arial", 10, "bold"),
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.add_to_cart
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=8
        )


    # ==========================================
    # CART SECTION
    # ==========================================

    def create_cart_section(self, parent):

        cart_frame = tk.Frame(
            parent,
            bg="white"
        )

        cart_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        tk.Label(
            cart_frame,
            text="Your Order Cart",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )


        # Cart table
        cart_table_frame = tk.Frame(
            cart_frame,
            bg="white"
        )

        cart_table_frame.pack(
            fill="both",
            expand=True,
            padx=10
        )

        columns = (
            "ID",
            "Food Item",
            "Qty",
            "Price",
            "Total"
        )

        self.cart_table = ttk.Treeview(
            cart_table_frame,
            columns=columns,
            show="headings",
            height=7
        )

        widths = {
            "ID": 35,
            "Food Item": 100,
            "Qty": 40,
            "Price": 65,
            "Total": 70
        }

        for col in columns:

            self.cart_table.heading(
                col,
                text=col
            )

            self.cart_table.column(
                col,
                width=widths[col],
                minwidth=35,
                anchor="center"
            )

        self.cart_table.pack(
            fill="both",
            expand=True
        )


        # Cart action buttons
        cart_buttons = tk.Frame(
            cart_frame,
            bg="white"
        )

        cart_buttons.pack(
            fill="x",
            padx=10,
            pady=10
        )

        tk.Button(
            cart_buttons,
            text="Remove Selected",
            font=("Arial", 9, "bold"),
            bg="#DC2626",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.remove_cart_item
        ).pack(
            side="left",
            padx=3,
            ipadx=5,
            ipady=6
        )

        tk.Button(
            cart_buttons,
            text="Clear Cart",
            font=("Arial", 9, "bold"),
            bg="#64748B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_cart
        ).pack(
            side="left",
            padx=3,
            ipadx=5,
            ipady=6
        )


        # Billing summary
        self.create_billing_summary(cart_frame)


    # ==========================================
    # BILLING SUMMARY
    # ==========================================

    def create_billing_summary(self, parent):

        summary = tk.Frame(
            parent,
            bg="#F8FAFC",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # Subtotal
        subtotal_row = tk.Frame(
            summary,
            bg="#F8FAFC"
        )

        subtotal_row.pack(
            fill="x",
            padx=10,
            pady=4
        )

        tk.Label(
            subtotal_row,
            text="Subtotal",
            font=("Arial", 10),
            bg="#F8FAFC"
        ).pack(side="left")

        self.subtotal_value = tk.Label(
            subtotal_row,
            text="₹0.00",
            font=("Arial", 10, "bold"),
            bg="#F8FAFC"
        )

        self.subtotal_value.pack(side="right")


        # Discount
        discount_row = tk.Frame(
            summary,
            bg="#F8FAFC"
        )

        discount_row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Label(
            discount_row,
            text="Discount (₹)",
            font=("Arial", 10),
            bg="#F8FAFC"
        ).pack(side="left")

        self.discount_entry = tk.Entry(
            discount_row,
            width=9,
            font=("Arial", 10),
            justify="right"
        )

        self.discount_entry.pack(side="right")

        self.discount_entry.insert(0, "0")


        # Tax rate
        tax_row = tk.Frame(
            summary,
            bg="#F8FAFC"
        )

        tax_row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Label(
            tax_row,
            text="Tax Rate (%)",
            font=("Arial", 10),
            bg="#F8FAFC"
        ).pack(side="left")

        self.tax_rate_entry = tk.Entry(
            tax_row,
            width=9,
            font=("Arial", 10),
            justify="right"
        )

        self.tax_rate_entry.pack(side="right")

        self.tax_rate_entry.insert(0, "0")


        # Tax amount
        tax_amount_row = tk.Frame(
            summary,
            bg="#F8FAFC"
        )

        tax_amount_row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Label(
            tax_amount_row,
            text="Tax Amount",
            font=("Arial", 10),
            bg="#F8FAFC"
        ).pack(side="left")

        self.tax_value = tk.Label(
            tax_amount_row,
            text="₹0.00",
            font=("Arial", 10, "bold"),
            bg="#F8FAFC"
        )

        self.tax_value.pack(side="right")


        # Grand total
        total_row = tk.Frame(
            summary,
            bg="#17324D"
        )

        total_row.pack(
            fill="x",
            padx=5,
            pady=8
        )

        tk.Label(
            total_row,
            text="GRAND TOTAL",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#17324D"
        ).pack(
            side="left",
            padx=8,
            pady=10
        )

        self.total_value = tk.Label(
            total_row,
            text="₹0.00",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#17324D"
        )

        self.total_value.pack(
            side="right",
            padx=8
        )


        # Recalculate when values change
        self.discount_entry.bind(
            "<KeyRelease>",
            self.update_totals
        )

        self.tax_rate_entry.bind(
            "<KeyRelease>",
            self.update_totals
        )


        # Payment method
        payment_row = tk.Frame(
            summary,
            bg="#F8FAFC"
        )

        payment_row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Label(
            payment_row,
            text="Payment Method",
            font=("Arial", 10, "bold"),
            bg="#F8FAFC"
        ).pack(
            side="left"
        )

        self.payment_box = ttk.Combobox(
            payment_row,
            values=["Cash", "UPI", "Card"],
            state="readonly",
            width=10,
            font=("Arial", 10)
        )

        self.payment_box.pack(side="right")

        self.payment_box.set("Cash")


        # Place order button
        tk.Button(
            summary,
            text="PLACE ORDER",
            font=("Arial", 12, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            relief="flat",
            cursor="hand2",
            command=self.place_order
        ).pack(
            fill="x",
            padx=10,
            pady=(8, 12),
            ipady=9
        )


    # ==========================================
    # LOAD MENU ITEMS
    # ==========================================

    def refresh_menu(self, search_text=""):

        conn = get_connection()

        try:

            if search_text:

                items = conn.execute("""

                    SELECT item_id, item_name, category, price

                    FROM menu_items

                    WHERE is_available = 1
                    AND (
                        item_name LIKE ?
                        OR category LIKE ?
                    )

                    ORDER BY item_name

                """, (
                    f"%{search_text}%",
                    f"%{search_text}%"
                )).fetchall()

            else:

                items = conn.execute("""

                    SELECT item_id, item_name, category, price

                    FROM menu_items

                    WHERE is_available = 1

                    ORDER BY item_name

                """).fetchall()


            # Clear previous data
            for row in self.menu_table.get_children():

                self.menu_table.delete(row)


            # Display available items
            for item in items:

                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        item["item_id"],
                        item["item_name"],
                        item["category"],
                        f"{item['price']:.2f}"
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
    # SEARCH MENU
    # ==========================================

    def search_menu(self):

        search_text = self.menu_search_entry.get().strip()

        self.refresh_menu(search_text)


    # ==========================================
    # ADD ITEM TO CART
    # ==========================================

    def add_to_cart(self):

        selected = self.menu_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Item",
                "Please select a food item first.",
                parent=self.parent
            )

            return


        try:

            quantity = int(
                self.quantity_entry.get().strip()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Quantity",
                "Please enter a valid positive quantity.",
                parent=self.parent
            )

            return


        values = self.menu_table.item(
            selected[0],
            "values"
        )

        item_id = int(values[0])
        item_name = values[1]
        price = Decimal(str(values[3]))


        # If item already exists, increase quantity
        if item_id in self.cart:

            self.cart[item_id]["quantity"] += quantity

        else:

            self.cart[item_id] = {
                "name": item_name,
                "price": price,
                "quantity": quantity
            }


        self.refresh_cart()

        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")


    # ==========================================
    # REFRESH CART TABLE
    # ==========================================

    def refresh_cart(self):

        # Clear previous rows
        for row in self.cart_table.get_children():

            self.cart_table.delete(row)


        # Insert cart items
        for item_id, item in self.cart.items():

            quantity = item["quantity"]
            price = item["price"]

            item_total = price * quantity

            self.cart_table.insert(
                "",
                "end",
                values=(
                    item_id,
                    item["name"],
                    quantity,
                    f"₹{price:.2f}",
                    f"₹{item_total:.2f}"
                )
            )


        self.update_totals()


    # ==========================================
    # REMOVE CART ITEM
    # ==========================================

    def remove_cart_item(self):

        selected = self.cart_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Item",
                "Please select an item from the cart.",
                parent=self.parent
            )

            return


        values = self.cart_table.item(
            selected[0],
            "values"
        )

        item_id = int(values[0])

        if item_id in self.cart:

            del self.cart[item_id]

        self.refresh_cart()


    # ==========================================
    # CLEAR CART
    # ==========================================

    def clear_cart(self):

        self.cart.clear()

        self.refresh_cart()


    # ==========================================
    # CALCULATE BILL
    # ==========================================

    def calculate_totals(self):

        subtotal = sum(
            (
                item["price"] * item["quantity"]
                for item in self.cart.values()
            ),
            Decimal("0.00")
        )

        discount = Decimal(
            self.discount_entry.get().strip() or "0"
        )

        tax_rate = Decimal(
            self.tax_rate_entry.get().strip() or "0"
        )

        if discount < 0 or discount > subtotal:

            raise ValueError(
                "Discount must be between zero and subtotal."
            )

        if tax_rate < 0 or tax_rate > 100:

            raise ValueError(
                "Tax rate must be between 0 and 100."
            )

        taxable_amount = subtotal - discount

        tax_amount = (
            taxable_amount * tax_rate / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        grand_total = (
            taxable_amount + tax_amount
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return (
            subtotal,
            discount,
            tax_rate,
            tax_amount,
            grand_total
        )


    # ==========================================
    # UPDATE BILL SUMMARY
    # ==========================================

    def update_totals(self, event=None):

        try:

            totals = self.calculate_totals()

            subtotal, discount, tax_rate, tax_amount, total = totals

            self.subtotal_value.config(
                text=f"₹{subtotal:.2f}"
            )

            self.tax_value.config(
                text=f"₹{tax_amount:.2f}"
            )

            self.total_value.config(
                text=f"₹{total:.2f}"
            )

        except (InvalidOperation, ValueError):

            self.tax_value.config(
                text="Invalid input"
            )

            self.total_value.config(
                text="Check values"
            )


    # ==========================================
    # PLACE ORDER
    # ==========================================

    def place_order(self):

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Please add food items before placing an order.",
                parent=self.parent
            )

            return


        customer_name = (
            self.customer_name_entry.get().strip()
        )

        customer_phone = (
            self.phone_entry.get().strip()
        )

        order_type = self.order_type_box.get()

        payment_method = self.payment_box.get()


        # Validate customer details
        if customer_phone and not customer_name:

            messagebox.showwarning(
                "Customer Details",
                "Enter customer name when providing a mobile number.",
                parent=self.parent
            )

            return


        if customer_phone and not customer_phone.isdigit():

            messagebox.showwarning(
                "Invalid Mobile",
                "Mobile number should contain digits only.",
                parent=self.parent
            )

            return


        try:

            totals = self.calculate_totals()

            subtotal, discount, tax_rate, tax_amount, grand_total = totals

        except (InvalidOperation, ValueError) as e:

            messagebox.showerror(
                "Billing Error",
                str(e),
                parent=self.parent
            )

            return


        if not order_type or not payment_method:

            messagebox.showwarning(
                "Missing Details",
                "Please select order type and payment method.",
                parent=self.parent
            )

            return


        # Confirmation
        confirm = messagebox.askyesno(
            "Confirm Order",
            f"Grand Total: ₹{grand_total:.2f}\n\n"
            f"Payment: {payment_method}\n\n"
            "Do you want to save this order?",
            parent=self.parent
        )

        if not confirm:
            return


        conn = None

        try:

            conn = get_connection()

            # Start database transaction
            conn.execute("BEGIN")

            customer_id = None


            # Save customer if details are provided
            if customer_name:

                cursor = conn.execute("""

                    INSERT INTO customers
                    (name, phone)

                    VALUES (?, ?)

                """, (
                    customer_name,
                    customer_phone
                ))

                customer_id = cursor.lastrowid


            # Save main order
            cursor = conn.execute("""

                INSERT INTO orders (
                    customer_id,
                    order_type,
                    subtotal,
                    discount,
                    tax_rate,
                    tax_amount,
                    grand_total,
                    payment_method
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, (
                customer_id,
                order_type,
                float(subtotal),
                float(discount),
                float(tax_rate),
                float(tax_amount),
                float(grand_total),
                payment_method
            ))

            order_id = cursor.lastrowid


            # Save individual order items
            for item_id, item in self.cart.items():

                quantity = item["quantity"]
                price = item["price"]

                item_total = price * quantity

                conn.execute("""

                    INSERT INTO order_items (
                        order_id,
                        item_id,
                        item_name,
                        quantity,
                        unit_price,
                        item_total
                    )

                    VALUES (?, ?, ?, ?, ?, ?)

                """, (
                    order_id,
                    item_id,
                    item["name"],
                    quantity,
                    float(price),
                    float(item_total)
                ))


            # Save all database changes
            conn.commit()


            messagebox.showinfo(
                "Order Successful",
                f"Order #{order_id} saved successfully!\n\n"
                f"Grand Total: ₹{grand_total:.2f}",
                parent=self.parent
            )


            # Clear order after success
            self.cart.clear()

            self.customer_name_entry.delete(0, tk.END)

            self.phone_entry.delete(0, tk.END)

            self.order_type_box.set("Dine-in")

            self.payment_box.set("Cash")

            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, "0")

            self.tax_rate_entry.delete(0, tk.END)
            self.tax_rate_entry.insert(0, "0")

            self.refresh_cart()

            self.refresh_menu()


        except sqlite3.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Order Error",
                f"Could not save order:\n{e}",
                parent=self.parent
            )

        finally:

            if conn:
                conn.close()
