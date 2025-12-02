# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class AssetMovementLog(Document):

    def before_insert(self):
        self.movement_datetime = now_datetime()
