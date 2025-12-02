import frappe
from frappe.utils import today, add_days, date_diff

# ---------------------------------------------------------
# 1. CHECK OVERDUE RENTALS
# ---------------------------------------------------------

def check_overdue_items():
    """Mark overdue rental contracts + auto-create notifications"""
    contracts = frappe.get_all(
        "Rental Contract",
        filters={"docstatus": 1, "contract_status": "Active", "end_date": ("<", today())},
        fields=["name", "customer", "end_date"]
    )

    for c in contracts:
        overdue_days = date_diff(today(), c.end_date)
        frappe.db.set_value("Rental Contract", c.name, "overdue_days", overdue_days)
        frappe.db.commit()


# ---------------------------------------------------------
# 2. SEND RETURN REMINDERS
# ---------------------------------------------------------

def send_return_reminders():
    """Send reminders for items due today or overdue."""

    contracts = frappe.get_all(
        "Rental Contract",
        filters={"docstatus": 1, "contract_status": "Active"},
        fields=["name", "customer", "customer_name", "end_date"]
    )

    for c in contracts:
        if c.end_date == today() or c.end_date < today():

            message = f"""
Dear {c.customer_name},

This is a friendly reminder that your rental contract {c.name} 
is due for return on {c.end_date}.

If already returned, please ignore.

Thank you,
Furniture Rental Team
"""

            # Send Email
            customer_email = frappe.db.get_value("Customer", c.customer, "email_id")
            if customer_email:
                frappe.sendmail(
                    recipients=[customer_email],
                    subject=f"Rental Return Reminder: {c.name}",
                    message=message
                )


# ---------------------------------------------------------
# 3. SYNC SERIAL STATUS (extra safety)
# ---------------------------------------------------------

def sync_serial_status():
    """Ensure serial numbers match rental status (optional safety feature)."""

    rented_items = frappe.get_all(
        "Rental Contract Item",
        filters={"parenttype": "Rental Contract"},
        fields=["serial_no", "parent"],
    )

    for item in rented_items:
        serial = frappe.get_doc("Serial No", item.serial_no)

        # If contract submitted but serial not marked “Out on Rent”
        contract_status = frappe.db.get_value("Rental Contract", item.parent, "contract_status")

        if contract_status == "Active" and serial.status != "Out on Rent":
            serial.status = "Out on Rent"
            serial.save(ignore_permissions=True)
