import frappe
from frappe.utils import today

def execute(filters=None):
    columns = [
        {"label": "Contract", "fieldname": "rental_contract", "fieldtype": "Link", "options": "Rental Contract", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120},
        {"label": "Days Overdue", "fieldname": "overdue_days", "fieldtype": "Int", "width": 120},
        {"label": "Plan Type", "fieldname": "plan_type", "fieldtype": "Data", "width": 120},
        {"label": "Total Rent", "fieldname": "total_rent", "fieldtype": "Currency", "width": 120}
    ]

    contracts = frappe.get_all(
        "Rental Contract",
        filters={"docstatus": 1, "contract_status": ["!=", "Completed"], "end_date": ["<", today()]},
        fields=["name", "customer", "end_date", "plan_type", "total_rent"]
    )

    data = []

    for c in contracts:
        data.append({
            "rental_contract": c.name,
            "customer": c.customer,
            "end_date": c.end_date,
            "overdue_days": frappe.utils.date_diff(today(), c.end_date),
            "plan_type": c.plan_type,
            "total_rent": c.total_rent
        })

    return columns, data
