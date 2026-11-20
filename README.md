# Restaurant Billing System

A desktop application for managing restaurant menu items, customer orders, billing, and receipts. It is built with Python's Tkinter GUI toolkit and stores application data locally in SQLite.

## Features

- Admin login with salted PBKDF2 password hashing
- Dashboard with sales and order summaries
- Add, update, delete, and search menu items
- Create customer orders and manage a cart
- Apply discounts and tax, and select a payment method
- Search order history and view order details
- Generate and open PDF receipts

## Requirements

- Python 3.10 or later
- Tkinter (included with most standard Python installations)
- Dependencies listed in `requirements.txt`

## Setup and run

From the project directory, create and activate a virtual environment, install dependencies, and start the application:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On first launch, the application creates the SQLite database at `database/restaurant.db` and adds sample menu items.

## Default login

On a new database, the default admin account is:

- **Username:** `admin`
- **Password:** `admin123`

Change the default credentials before using the application with real or sensitive data.

## Project files

- `main.py` — application entry point and window navigation
- `login.py`, `auth.py` — login UI and authentication
- `dashboard.py` — dashboard and navigation
- `menu.py` — menu management
- `order.py` — order creation and billing
- `order_history.py` — order search and history
- `receipt.py` — PDF receipt generation
- `database.py` — SQLite schema and database initialization

The database and generated PDF receipts are local runtime data and are excluded from Git.
