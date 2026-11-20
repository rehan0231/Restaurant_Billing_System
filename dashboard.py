
import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from menu import MenuManagement
from order import OrderManagement
from order_history import OrderHistory


class DashboardWindow:

    def __init__(self, root, username, on_logout):

        self.root = root
        self.username = username
        self.on_logout = on_logout

        self.menu_page = None
        self.order_page = None
        self.history_page = None

        self.create_dashboard()


    # ==========================================
    # MAIN DASHBOARD
    # ==========================================

    def create_dashboard(self):

        self.root.title(
            "Restaurant Billing System - Dashboard"
        )

        self.root.geometry("1200x780")
        self.root.minsize(1050, 650)
        self.root.configure(bg="#F1F5F9")

        main_frame = tk.Frame(
            self.root,
            bg="#F1F5F9"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        main_frame.grid_columnconfigure(
            0,
            minsize=250,
            weight=0
        )

        main_frame.grid_columnconfigure(
            1,
            weight=1
        )

        main_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_sidebar(main_frame)

        self.content = tk.Frame(
            main_frame,
            bg="#F1F5F9"
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.show_dashboard_page()


    # ==========================================
    # SIDEBAR
    # ==========================================

    def create_sidebar(self, parent):

        sidebar = tk.Frame(
            parent,
            bg="#17324D",
            width=250
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="RESTAURANT",
            font=("Arial", 19, "bold"),
            fg="white",
            bg="#17324D"
        ).pack(pady=(40, 5))

        tk.Label(
            sidebar,
            text="MANAGEMENT SYSTEM",
            font=("Arial", 9),
            fg="#CBD5E1",
            bg="#17324D"
        ).pack(pady=(0, 45))

        menu_buttons = [
            ("Dashboard", "Dashboard"),
            ("New Order", "New Order"),
            ("Manage Menu", "Manage Menu"),
            ("Order History", "Order History"),
            ("Sales Reports", "Sales Reports")
        ]

        for label, page in menu_buttons:

            btn = tk.Button(
                sidebar,
                text=label,
                font=("Arial", 12, "bold"),
                fg="white",
                bg="#17324D",
                activebackground="#2563EB",
                activeforeground="white",
                relief="flat",
                bd=0,
                anchor="w",
                cursor="hand2",
                command=lambda p=page: self.navigate(p)
            )

            btn.pack(
                fill="x",
                padx=15,
                pady=6,
                ipady=11
            )

        logout_button = tk.Button(
            sidebar,
            text="Logout",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#DC2626",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=25,
            ipady=10
        )


    # ==========================================
    # SHOW DASHBOARD PAGE
    # ==========================================

    def show_dashboard_page(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.menu_page = None
        self.order_page = None
        self.history_page = None

        self.create_header()
        self.create_statistics()
        self.create_quick_actions()
        self.create_recent_transactions()

        self.refresh_dashboard()


    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        header = tk.Frame(
            self.content,
            bg="white",
            height=80
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            fg="#17324D",
            bg="white"
        ).pack(
            side="left",
            padx=20
        )

        tk.Label(
            header,
            text=f"Welcome, {self.username}",
            font=("Arial", 12),
            fg="#64748B",
            bg="white"
        ).pack(
            side="right",
            padx=20
        )


    # ==========================================
    # STATISTICS CARDS
    # ==========================================

    def create_statistics(self):

        self.stats_frame = tk.Frame(
            self.content,
            bg="#F1F5F9"
        )

        self.stats_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        for column in range(3):

            self.stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.sales_value = self.create_card(
            self.stats_frame,
            "Total Sales",
            "₹0.00",
            "#2563EB",
            0
        )

        self.orders_value = self.create_card(
            self.stats_frame,
            "Total Orders",
            "0",
            "#16A34A",
            1
        )

        self.menu_value = self.create_card(
            self.stats_frame,
            "Menu Items",
            "0",
            "#D97706",
            2
        )


    def create_card(self, parent, title, value, color, column):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8,
            ipady=15
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 12),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            bg="white",
            fg=color
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        return value_label


    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    def create_quick_actions(self):

        action_frame = tk.Frame(
            self.content,
            bg="#F1F5F9"
        )

        action_frame.pack(
            fill="x",
            padx=28,
            pady=15
        )

        tk.Label(
            action_frame,
            text="Quick Actions",
            font=("Arial", 18, "bold"),
            fg="#17324D",
            bg="#F1F5F9"
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        tk.Button(
            action_frame,
            text="+ New Order",
            font=("Arial", 11, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.navigate("New Order")
        ).pack(
            side="left",
            ipadx=20,
            ipady=10,
            padx=(0, 12)
        )

        tk.Button(
            action_frame,
            text="Manage Menu",
            font=("Arial", 11, "bold"),
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.navigate("Manage Menu")
        ).pack(
            side="left",
            ipadx=20,
            ipady=10
        )


    # ==========================================
    # RECENT TRANSACTIONS
    # ==========================================

    def create_recent_transactions(self):

        table_frame = tk.Frame(
            self.content,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(10, 25)
        )

        tk.Label(
            table_frame,
            text="Recent Transactions",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#17324D"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        table_area = tk.Frame(
            table_frame,
            bg="white"
        )

        table_area.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 15)
        )

        table_area.grid_rowconfigure(0, weight=1)
        table_area.grid_columnconfigure(0, weight=1)

        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=34,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        columns = (
            "Order ID",
            "Customer",
            "Order Type",
            "Payment",
            "Amount",
            "Date"
        )

        self.transaction_table = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            height=8
        )

        widths = {
            "Order ID": 75,
            "Customer": 150,
            "Order Type": 110,
            "Payment": 100,
            "Amount": 110,
            "Date": 170
        }

        for col in columns:

            self.transaction_table.heading(
                col,
                text=col
            )

            self.transaction_table.column(
                col,
                width=widths[col],
                minwidth=65,
                anchor="center",
                stretch=True
            )

        self.transaction_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.transaction_table.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.transaction_table.configure(
            yscrollcommand=scrollbar.set
        )


    # ==========================================
    # FETCH DATABASE DATA
    # ==========================================

    def refresh_dashboard(self):

        conn = None

        try:

            conn = get_connection()

            # Total sales
            sales = conn.execute("""
                SELECT COALESCE(SUM(grand_total), 0)
                FROM orders
            """).fetchone()[0]

            # Total orders
            orders = conn.execute("""
                SELECT COUNT(*)
                FROM orders
            """).fetchone()[0]

            # Available menu items
            items = conn.execute("""
                SELECT COUNT(*)
                FROM menu_items
                WHERE is_available = 1
            """).fetchone()[0]


            # Update cards
            self.sales_value.config(
                text=f"₹{sales:,.2f}"
            )

            self.orders_value.config(
                text=str(orders)
            )

            self.menu_value.config(
                text=str(items)
            )


            # Fetch recent transactions
            recent_orders = conn.execute("""

                SELECT
                    o.order_id,
                    COALESCE(c.name, 'Walk-in Customer'),
                    o.order_type,
                    o.payment_method,
                    o.grand_total,
                    o.created_at

                FROM orders o

                LEFT JOIN customers c
                ON o.customer_id = c.customer_id

                ORDER BY o.order_id DESC

                LIMIT 8

            """).fetchall()


            # Clear old records
            for row in self.transaction_table.get_children():
                self.transaction_table.delete(row)


            # Insert latest orders
            if recent_orders:

                for order in recent_orders:

                    self.transaction_table.insert(
                        "",
                        "end",
                        values=(
                            order[0],
                            order[1],
                            order[2],
                            order[3],
                            f"₹{order[4]:,.2f}",
                            order[5]
                        )
                    )

            else:

                self.transaction_table.insert(
                    "",
                    "end",
                    values=(
                        "-",
                        "No transactions yet",
                        "-",
                        "-",
                        "-",
                        "-"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Dashboard Error",
                str(e),
                parent=self.root
            )

        finally:

            if conn:
                conn.close()


    # ==========================================
    # PAGE NAVIGATION
    # ==========================================

    def navigate(self, page):

        if page == "Dashboard":

            self.show_dashboard_page()


        elif page == "Manage Menu":

            for widget in self.content.winfo_children():
                widget.destroy()

            self.menu_page = MenuManagement(
                self.content,
                on_back=self.show_dashboard_page
            )


        elif page == "New Order":

            for widget in self.content.winfo_children():
                widget.destroy()

            self.order_page = OrderManagement(
                self.content,
                on_back=self.show_dashboard_page
            )


        elif page == "Order History":

            for widget in self.content.winfo_children():
                widget.destroy()

            self.history_page = OrderHistory(
                self.content,
                on_back=self.show_dashboard_page
            )


        else:

            messagebox.showinfo(
                page,
                f"{page} module will be developed next.",
                parent=self.root
            )


    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if result:
            self.on_logout()
