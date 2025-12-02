import frappe
from frappe.utils import getdate

def execute(filters=None):
    filters = filters or {}

    start = filters.get("start_date")
    end = filters.get("end_date")

    columns = [
        {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Serial No", "fieldname": "serial_no", "fieldtype": "Link", "options": "Serial No", "width": 150},
        {"label": "Condition", "fieldname": "condition", "fieldtype": "Data", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Available?", "fieldname": "available", "fieldtype": "Data", "width": 100}
    ]

    data = []
    serials = frappe.get_all("Serial No", fields=["name", "item_code", "rental_condition", "status"])

    for sn in serials:
        available = "Yes"

        # check overlap with existing rental contracts
        rentals = frappe.db.sql("""
            SELECT name, start_date, end_date
            FROM `tabRental Contract`
            WHERE docstatus = 1
            AND %s BETWEEN start_date AND end_date
            OR %s BETWEEN start_date AND end_date
            OR start_date BETWEEN %s AND %s
        """, (start, end, start, end), as_dict=True)

        if rentals:
            available = "No"

        data.append({
            "item_code": sn.item_code,
            "serial_no": sn.name,
            "condition": sn.rental_condition,
            "status": sn.status,
            "available": available
        })

    return columns, data
