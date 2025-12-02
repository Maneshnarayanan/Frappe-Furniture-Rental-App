// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Maintenance Request", {
    refresh(frm) {
        if (frm.doc.docstatus === 0 && frm.doc.serial_no) {
            frappe.msgprint("This item will be marked as 'Under Maintenance' when submitted.");
        }
          if (frm.doc.serial_no) {
            frm.add_custom_button("View Serial No", () => {
                frappe.set_route("Form", "Serial No", frm.doc.serial_no);
            }, "View");
        }

        if (frm.doc.rental_contract) {
            frm.add_custom_button("View Contract", () => {
                frappe.set_route("Form", "Rental Contract", frm.doc.rental_contract);
            }, "View");
        }

        if (frm.doc.docstatus === 1) {
            frm.add_custom_button("Mark Completed", () => {
                frappe.call({
                    method: "frappe.client.submit",
                    args: {
                        doc: {
                            doctype: "Maintenance Request",
                            name: frm.doc.name,
                            status: "Completed"
                        }
                    },
                    callback() {
                        frm.reload_doc();
                    }
                });
            }, "Action");
        }
    }
});
