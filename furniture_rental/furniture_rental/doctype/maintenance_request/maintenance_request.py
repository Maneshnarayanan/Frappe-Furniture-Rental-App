# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class MaintenanceRequest(Document):

    def on_submit(self):
        self.mark_serial_unavailable()

    def on_cancel(self):
        self.mark_serial_available()

    def mark_serial_unavailable(self):
        if self.serial_no:
            sn = frappe.get_doc("Serial No", self.serial_no)
            sn.status = "Under Maintenance"
            sn.save(ignore_permissions=True)

    def mark_serial_available(self):
        if self.serial_no:
            sn = frappe.get_doc("Serial No", self.serial_no)
            sn.status = "Available"
            sn.save(ignore_permissions=True)
