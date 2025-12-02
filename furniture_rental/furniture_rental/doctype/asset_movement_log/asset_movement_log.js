// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Movement Log", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.set_value("movement_datetime", frappe.datetime.now_datetime());
        }

         if (frm.doc.serial_no) {
            frm.add_custom_button("View Serial No", () => {
                frappe.set_route("Form", "Serial No", frm.doc.serial_no);
            });
        }
    }
});
