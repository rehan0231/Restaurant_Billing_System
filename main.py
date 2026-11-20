
import tkinter as tk

from database import initialize_database
from auth import ensure_default_admin
from login import LoginWindow
from dashboard import DashboardWindow


# Open Dashboard after successful login
def show_dashboard(root, username):

    for widget in root.winfo_children():
        widget.destroy()

    root.unbind("<Return>")

    root.dashboard_window = DashboardWindow(
        root,
        username,
        on_logout=lambda: show_login(root)
    )


# Open Login screen
def show_login(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.dashboard_window = None

    root.login_window = LoginWindow(
        root,
        on_success=lambda username: show_dashboard(root, username)
    )


# Main application
def main():

    # Initialize database
    initialize_database()

    # Create default admin
    ensure_default_admin()

    # Create main window
    root = tk.Tk()

    # Open login screen
    show_login(root)

    # Start application
    root.mainloop()


if __name__ == "__main__":
    main()
