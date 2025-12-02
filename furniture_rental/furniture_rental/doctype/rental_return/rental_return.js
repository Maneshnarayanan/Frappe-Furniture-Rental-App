// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Return", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.trigger("calculate_late_fee");
        }
        if (frm.doc.docstatus === 1) {

            // View Maintenance Requests created for this Return
            frm.add_custom_button("View Maintenance Requests", () => {
                frappe.set_route("List", "Maintenance Request", {
                    rental_contract: frm.doc.rental_contract
                });
            }, "View");

            // Create Settlement
            frm.add_custom_button("Create Settlement", () => {
                frappe.new_doc("Rental Settlement", {
                    rental_contract: frm.doc.rental_contract,
                    customer: frm.doc.customer,
                    deposit_received: frm.doc.deposit_received
                });
            }, "Create");
        }
    },

    return_date(frm) {
        frm.trigger("calculate_late_fee");
    },

    calculate_late_fee(frm) {
        let return_date = frm.doc.return_date;
        let contract_end = frm.doc.contract_end_date;

        if (!return_date || !contract_end) return;

        let diff = frappe.datetime.get_diff(return_date, contract_end);
        frm.set_value("late_days", diff > 0 ? diff : 0);

        let late_fee = (frm.doc.late_days || 0) * (frm.doc.late_fee_per_day || 0);
        frm.set_value("late_fee", late_fee);
    }
});


frappe.ui.form.on("Rental Return Item", {
    serial_no(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);

        if (!row.serial_no) return;

        frappe.db.get_doc("Serial No", row.serial_no)
            .then(sn => {
                row.condition_before = sn.rental_condition;
                frm.refresh_field("items");
            });
    },

    condition_on_return(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);

        if (["Damaged", "Needs Repair", "Severely Damaged"].includes(row.condition_on_return)) {
            frappe.msgprint(`⚠️ Item ${row.serial_no} returned in bad condition. Maintenance will be created automatically.`);
        }
    }
});

