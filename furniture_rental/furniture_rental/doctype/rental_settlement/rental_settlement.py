# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RentalSettlement(Document):

    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        charges = (
            (self.late_fee or 0)
            + (self.damage_charges or 0)
            + (self.cleaning_charges or 0)
            + (self.missing_item_charges or 0)
        )

        self.total_charges = charges

        deposit = self.deposit_received or 0

        # customer owes the company
        if charges > deposit:
            self.net_payable = charges - deposit
            self.net_receivable = 0
        else:
            self.net_receivable = deposit - charges
            self.net_payable = 0

    def on_submit(self):
        self.update_contract_status()

    def update_contract_status(self):
        contract = frappe.get_doc("Rental Contract", self.rental_contract)
        contract.contract_status = "Completed"
        contract.save(ignore_permissions=True)
