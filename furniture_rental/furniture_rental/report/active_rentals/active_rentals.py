import frappe

def execute(filters=None):
    columns = [
        {"label": "Contract", "fieldname": "rental_contract", "fieldtype": "Link", "options": "Rental Contract", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120},
        {"label": "Plan Type", "fieldname": "plan_type", "fieldtype": "Data", "width": 120},
        {"label": "Total Rent", "fieldname": "total_rent", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "contract_status", "fieldtype": "Data", "width": 120}
    ]

    data = frappe.get_all(
        "Rental Contract",
        filters={"contract_status": "Active", "docstatus": 1},
        fields=["name as rental_contract", "customer", "start_date", "end_date", "plan_type", "total_rent", "contract_status"]
    )

    return columns, data
