# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class RentalReturn(Document):

    def validate(self):
        self.calculate_late_fee()

    def calculate_late_fee(self):
        if self.return_date and self.contract_end_date:
            days = date_diff(self.return_date, self.contract_end_date)
            self.late_days = days if days > 0 else 0
            self.late_fee = (self.late_days or 0) * (self.late_fee_per_day or 0)

    def on_submit(self):
        self.process_items()
        self.update_serial_condition()

    def process_items(self):
        """If damaged, auto-create maintenance request."""
        for d in self.items:
            if d.condition_on_return in ["Damaged", "Needs Repair", "Severely Damaged"]:
                self.create_maintenance_request(d)

    def create_maintenance_request(self, row):
        doc = frappe.new_doc("Maintenance Request")
        doc.item_code = row.item_code
        doc.serial_no = row.serial_no
        doc.rental_contract = self.rental_contract
        doc.issue_type = "Damage"
        doc.description = f"Returned damaged: {row.condition_on_return}"
        doc.insert(ignore_permissions=True)

    def update_serial_condition(self):
        for d in self.items:
            if d.serial_no:
                sn = frappe.get_doc("Serial No", d.serial_no)
                sn.rental_condition = d.condition_on_return
                sn.status = "Available"
                sn.save(ignore_permissions=True)
