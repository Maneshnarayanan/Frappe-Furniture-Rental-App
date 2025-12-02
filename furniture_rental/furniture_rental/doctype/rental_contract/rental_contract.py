# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate

class RentalContract(Document):

    def validate(self):
        self.validate_dates()
        self.calculate_total_rent()
        self.set_customer()

    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                frappe.throw("End Date cannot be before Start Date.")

    def calculate_total_rent(self):
        """Auto calculate total rent based on plan + items."""
        total = 0
        for d in self.items:
            if self.plan_type == "Daily":
                total += (d.daily_rate or 0) * date_diff(self.end_date, self.start_date)
            elif self.plan_type == "Weekly":
                weeks = date_diff(self.end_date, self.start_date) / 7
                total += (d.weekly_rate or 0) * weeks
            elif self.plan_type == "Monthly":
                months = date_diff(self.end_date, self.start_date) / 30
                total += (d.monthly_rate or 0) * months

        self.total_rent = total

    def set_customer(self):
        if self.customer:
            doc = frappe.get_doc("Customer", self.customer)
            self.customer_name = doc.customer_name

    def on_submit(self):
        self.create_delivery_assignment()
        self.update_serial_status("Out on Rent")

    def on_cancel(self):
        self.update_serial_status("Available")

    def update_serial_status(self, status):
        """Update Serial No condition for each item."""
        for d in self.items:
            if d.serial_no:
                sn = frappe.get_doc("Serial No", d.serial_no)
                sn.status = status
                sn.save(ignore_permissions=True)

    def create_delivery_assignment(self):
        assignment = frappe.new_doc("Delivery Assignment")
        assignment.rental_contract = self.name
        assignment.customer = self.customer
        assignment.delivery_date = self.start_date
        assignment.insert(ignore_permissions=True)
