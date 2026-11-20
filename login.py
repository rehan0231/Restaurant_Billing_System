
import tkinter as tk
from tkinter import messagebox

from auth import verify_admin


class LoginWindow:

    def __init__(self, root, on_success):

        self.root = root
        self.on_success = on_success

        self.create_login_screen()


    def create_login_screen(self):

        # Main window settings
        self.root.title("Restaurant Billing System - Login")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)
        self.root.configure(bg="#EEF2F7")
        self.root.resizable(True, True)

        # Main container
        container = tk.Frame(
            self.root,
            bg="white"
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=860,
            height=500
        )


        # ==============================
        # LEFT PANEL
        # ==============================

        left_panel = tk.Frame(
            container,
            bg="#17324D",
            width=320,
            height=500
        )

        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="RESTAURANT",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#17324D"
        ).pack(pady=(135, 5))

        tk.Label(
            left_panel,
            text="BILLING SYSTEM",
            font=("Arial", 16),
            fg="#CBD5E1",
            bg="#17324D"
        ).pack()

        tk.Label(
            left_panel,
            text="Smart Billing\nEasy Management",
            font=("Arial", 14),
            fg="white",
            bg="#17324D",
            justify="center"
        ).pack(pady=40)


        # ==============================
        # RIGHT PANEL
        # ==============================

        right_panel = tk.Frame(
            container,
            bg="white"
        )

        right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )


        # Form container
        form = tk.Frame(
            right_panel,
            bg="white"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=55
        )


        # ==============================
        # HEADING
        # ==============================

        tk.Label(
            form,
            text="Admin Login",
            font=("Arial", 26, "bold"),
            fg="#17324D",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            form,
            text="Enter your credentials to continue",
            font=("Arial", 11),
            fg="gray",
            bg="white"
        ).pack(anchor="w", pady=(5, 30))


        # ==============================
        # USERNAME LABEL
        # ==============================

        tk.Label(
            form,
            text="Username",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#222222"
        ).pack(anchor="w")


        # Username outer frame
        username_box = tk.Frame(
            form,
            bg="#CBD5E1",
            height=52
        )

        username_box.pack(
            fill="x",
            pady=(8, 22)
        )

        username_box.pack_propagate(False)


        # Username input
        self.username_entry = tk.Entry(
            username_box,
            font=("Arial", 14),
            relief="flat",
            bd=0
        )

        self.username_entry.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )


        # ==============================
        # PASSWORD LABEL
        # ==============================

        tk.Label(
            form,
            text="Password",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#222222"
        ).pack(anchor="w")


        # Password outer frame
        password_box = tk.Frame(
            form,
            bg="#CBD5E1",
            height=52
        )

        password_box.pack(
            fill="x",
            pady=(8, 28)
        )

        password_box.pack_propagate(False)


        # Password input
        self.password_entry = tk.Entry(
            password_box,
            font=("Arial", 14),
            show="*",
            relief="flat",
            bd=0
        )

        self.password_entry.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )


        # ==============================
        # LOGIN BUTTON
        # ==============================

        login_button = tk.Button(
            form,
            text="LOGIN",
            font=("Arial", 13, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login
        )

        login_button.pack(
            fill="x",
            ipady=12
        )


        # Keyboard focus
        self.username_entry.focus_set()

        # Enter key login
        self.root.bind(
            "<Return>",
            self.handle_enter
        )


    # ==============================
    # HANDLE ENTER KEY
    # ==============================

    def handle_enter(self, event):

        self.login()

        return "break"


    # ==============================
    # LOGIN FUNCTION
    # ==============================

    def login(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get()


        # Validate empty fields
        if not username or not password:

            messagebox.showwarning(
                "Missing Details",
                "Please enter username and password.",
                parent=self.root
            )

            return


        # Verify admin credentials
        if verify_admin(username, password):

            messagebox.showinfo(
                "Login Successful",
                "Welcome to Restaurant Billing System!",
                parent=self.root
            )

            self.root.unbind("<Return>")

            self.on_success(username)

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=self.root
            )

            self.password_entry.delete(0, tk.END)

            self.password_entry.focus_set()
