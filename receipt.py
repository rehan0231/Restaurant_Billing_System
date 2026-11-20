
from pathlib import Path
import webbrowser
from decimal import Decimal

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

from database import get_connection


# ==========================================
# PROJECT SETTINGS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

BILLS_DIR = BASE_DIR / "bills"

# Edit these details for your restaurant
RESTAURANT_NAME = "RESTAURANT BILLING SYSTEM"

RESTAURANT_ADDRESS = ""

RECEIPT_WIDTH = 80 * mm


# ==========================================
# FONT CONFIGURATION
# ==========================================

def register_receipt_fonts():

    font_pairs = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ),
        (
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
        )
    ]

    for regular_path, bold_path in font_pairs:

        if Path(regular_path).exists() and Path(bold_path).exists():

            registered = pdfmetrics.getRegisteredFontNames()

            if "ReceiptRegular" not in registered:

                pdfmetrics.registerFont(
                    TTFont("ReceiptRegular", regular_path)
                )

                pdfmetrics.registerFont(
                    TTFont("ReceiptBold", bold_path)
                )

            return "ReceiptRegular", "ReceiptBold", True

    return "Helvetica", "Helvetica-Bold", False


# ==========================================
# MONEY FORMAT
# ==========================================

def format_money(amount, supports_rupee):

    value = Decimal(str(amount or 0))

    formatted = f"{value:,.2f}"

    if supports_rupee:
        return f"₹{formatted}"

    return f"INR {formatted}"


# ==========================================
# DRAW SEPARATOR
# ==========================================

def draw_separator(pdf, y):

    pdf.setStrokeColor(
        HexColor("#94A3B8")
    )

    pdf.setLineWidth(0.5)

    pdf.line(
        6 * mm,
        y,
        RECEIPT_WIDTH - 6 * mm,
        y
    )

    return y - 3 * mm


# ==========================================
# DRAW LEFT AND RIGHT TEXT
# ==========================================

def draw_left_right(
    pdf,
    left_text,
    right_text,
    y,
    regular_font,
    bold_font,
    bold=False,
    size=8
):

    font = bold_font if bold else regular_font

    pdf.setFont(font, size)
    pdf.setFillColor(black)

    pdf.drawString(
        6 * mm,
        y,
        str(left_text)
    )

    pdf.drawRightString(
        RECEIPT_WIDTH - 6 * mm,
        y,
        str(right_text)
    )

    return y - 5 * mm


# ==========================================
# GENERATE PDF RECEIPT
# ==========================================

def generate_receipt(order_id):

    regular_font, bold_font, supports_rupee = register_receipt_fonts()

    BILLS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = get_connection()

    try:

        # Fetch order and customer details
        order = conn.execute("""

            SELECT
                o.order_id,
                COALESCE(c.name, 'Walk-in Customer') AS customer_name,
                COALESCE(c.phone, '') AS customer_phone,
                o.order_type,
                o.subtotal,
                o.discount,
                o.tax_rate,
                o.tax_amount,
                o.grand_total,
                o.payment_method,
                o.created_at

            FROM orders o

            LEFT JOIN customers c
            ON o.customer_id = c.customer_id

            WHERE o.order_id = ?

        """, (order_id,)).fetchone()


        if order is None:

            raise ValueError(
                f"Order #{order_id} was not found."
            )


        # Fetch order items
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


    finally:

        conn.close()


    # ======================================
    # PREPARE CONTENT
    # ======================================

    margin = 6 * mm

    content_width = RECEIPT_WIDTH - (2 * margin)


    title_lines = simpleSplit(
        RESTAURANT_NAME,
        bold_font,
        10,
        content_width
    )


    address_lines = simpleSplit(
        RESTAURANT_ADDRESS,
        regular_font,
        7,
        content_width
    ) if RESTAURANT_ADDRESS else []


    metadata = [
        f"Bill Number: #{order['order_id']}",
        f"Date: {order['created_at']}",
        f"Customer: {order['customer_name']}",
        f"Mobile: {order['customer_phone'] or 'N/A'}",
        f"Order Type: {order['order_type']}",
        f"Payment Method: {order['payment_method']}"
    ]


    metadata_lines = []

    for text in metadata:

        metadata_lines.extend(
            simpleSplit(
                str(text),
                regular_font,
                7,
                content_width
            )
        )


    # Prepare item names
    prepared_items = []

    for item in items:

        name_lines = simpleSplit(
            str(item["item_name"]),
            regular_font,
            8,
            content_width
        )

        if not name_lines:
            name_lines = ["Food Item"]

        prepared_items.append(
            (item, name_lines)
        )


    # Calculate dynamic receipt height
    item_height = sum(
        len(lines) * 4 + 7
        for item, lines in prepared_items
    )

    page_height_mm = (
        85
        + len(title_lines) * 5
        + len(address_lines) * 4
        + len(metadata_lines) * 4
        + item_height
    )

    page_height = max(
        110 * mm,
        page_height_mm * mm
    )


    # PDF filename
    output_path = BILLS_DIR / f"Receipt_Order_{order_id}.pdf"


    # Create PDF
    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(RECEIPT_WIDTH, page_height)
    )

    pdf.setTitle(
        f"Restaurant Receipt - Order {order_id}"
    )

    pdf.setAuthor(
        RESTAURANT_NAME
    )

    y = page_height - 8 * mm


    # ======================================
    # RESTAURANT HEADER
    # ======================================

    pdf.setFillColor(
        HexColor("#17324D")
    )

    pdf.setFont(
        bold_font,
        10
    )

    for line in title_lines:

        pdf.drawCentredString(
            RECEIPT_WIDTH / 2,
            y,
            line
        )

        y -= 5 * mm


    pdf.setFillColor(black)

    pdf.setFont(
        bold_font,
        8
    )

    pdf.drawCentredString(
        RECEIPT_WIDTH / 2,
        y,
        "CUSTOMER BILL / RECEIPT"
    )

    y -= 6 * mm


    # Restaurant address
    pdf.setFont(
        regular_font,
        7
    )

    for line in address_lines:

        pdf.drawCentredString(
            RECEIPT_WIDTH / 2,
            y,
            line
        )

        y -= 4 * mm


    y = draw_separator(pdf, y)


    # ======================================
    # ORDER INFORMATION
    # ======================================

    pdf.setFont(
        regular_font,
        7
    )

    for line in metadata_lines:

        pdf.drawString(
            margin,
            y,
            line
        )

        y -= 4 * mm


    y = draw_separator(pdf, y - 1 * mm)


    # ======================================
    # ITEM DETAILS
    # ======================================

    pdf.setFont(
        bold_font,
        8
    )

    pdf.drawString(
        margin,
        y,
        "ITEM DETAILS"
    )

    y -= 6 * mm


    for item, name_lines in prepared_items:

        pdf.setFont(
            regular_font,
            8
        )

        pdf.setFillColor(black)

        # Food name
        for line in name_lines:

            pdf.drawString(
                margin,
                y,
                line
            )

            y -= 4 * mm


        # Quantity and price
        quantity = item["quantity"]

        unit_price = format_money(
            item["unit_price"],
            supports_rupee
        )

        item_total = format_money(
            item["item_total"],
            supports_rupee
        )

        pdf.setFont(
            regular_font,
            7
        )

        pdf.drawString(
            margin,
            y,
            f"{quantity} x {unit_price}"
        )

        pdf.drawRightString(
            RECEIPT_WIDTH - margin,
            y,
            item_total
        )

        y -= 7 * mm


    y = draw_separator(pdf, y)


    # ======================================
    # BILL SUMMARY
    # ======================================

    subtotal = order["subtotal"]

    discount = order["discount"]

    tax_rate = order["tax_rate"]

    tax_amount = order["tax_amount"]

    grand_total = order["grand_total"]


    y = draw_left_right(
        pdf,
        "Subtotal",
        format_money(subtotal, supports_rupee),
        y,
        regular_font,
        bold_font
    )

    y = draw_left_right(
        pdf,
        "Discount",
        format_money(discount, supports_rupee),
        y,
        regular_font,
        bold_font
    )


    taxable_amount = (
        Decimal(str(subtotal))
        - Decimal(str(discount))
    )

    y = draw_left_right(
        pdf,
        "Taxable Amount",
        format_money(taxable_amount, supports_rupee),
        y,
        regular_font,
        bold_font
    )

    y = draw_left_right(
        pdf,
        f"Tax ({tax_rate}%)",
        format_money(tax_amount, supports_rupee),
        y,
        regular_font,
        bold_font
    )


    y = draw_separator(pdf, y)


    # Grand total
    pdf.setFillColor(
        HexColor("#17324D")
    )

    pdf.setFont(
        bold_font,
        10
    )

    pdf.drawString(
        margin,
        y,
        "GRAND TOTAL"
    )

    pdf.drawRightString(
        RECEIPT_WIDTH - margin,
        y,
        format_money(grand_total, supports_rupee)
    )

    y -= 9 * mm


    # ======================================
    # FOOTER
    # ======================================

    y = draw_separator(pdf, y)

    pdf.setFont(
        bold_font,
        8
    )

    pdf.setFillColor(
        HexColor("#17324D")
    )

    pdf.drawCentredString(
        RECEIPT_WIDTH / 2,
        y,
        "Thank You For Visiting!"
    )

    y -= 5 * mm

    pdf.setFont(
        regular_font,
        7
    )

    pdf.setFillColor(black)

    pdf.drawCentredString(
        RECEIPT_WIDTH / 2,
        y,
        "Please Visit Again"
    )


    # Save PDF
    pdf.save()

    return output_path


# ==========================================
# OPEN GENERATED PDF
# ==========================================

def open_receipt(file_path):

    path = Path(file_path).resolve()

    if not path.exists():

        raise FileNotFoundError(
            "Receipt PDF was not found."
        )

    return webbrowser.open(
        path.as_uri()
    )


# ==========================================
# DIRECT TEST
# ==========================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print("Usage: python3 receipt.py ORDER_ID")

        sys.exit(1)

    try:

        order_id = int(sys.argv[1])

        file_path = generate_receipt(order_id)

        print("Receipt generated successfully!")

        print("File location:", file_path)

        open_receipt(file_path)

    except Exception as e:

        print("Receipt Error:", e)
