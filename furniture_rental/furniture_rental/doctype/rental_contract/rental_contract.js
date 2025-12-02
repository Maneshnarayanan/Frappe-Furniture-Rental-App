// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.set_value("contract_date", frappe.datetime.get_today());
        }


        if (!frm.is_new() && frm.doc.docstatus === 1) {

            // Create Delivery Note
            frm.add_custom_button("Create Delivery Note", () => {
                frappe.new_doc("Delivery Note", {
                    customer: frm.doc.customer,
                    rental_contract: frm.doc.name,
                    is_rental_delivery: 1
                });
            }, "Create");

            // Create Rental Return
            frm.add_custom_button("Create Rental Return", () => {
                frappe.new_doc("Rental Return", {
                    rental_contract: frm.doc.name,
                    customer: frm.doc.customer,
                    contract_end_date: frm.doc.end_date
                });
            }, "Create");

            // Create Settlement
            frm.add_custom_button("Create Settlement", () => {
                frappe.new_doc("Rental Settlement", {
                    rental_contract: frm.doc.name,
                    customer: frm.doc.customer,
                    deposit_received: frm.doc.deposit_amount,
                    total_rent_amount: frm.doc.total_rent
                });
            }, "Create");

            // View Movement Logs
            frm.add_custom_button("Asset Movements", () => {
                frappe.set_route("List", "Asset Movement Log", {
                    rental_contract: frm.doc.name
                });
            }, "View");
        }


    },

    start_date(frm) {
        frm.trigger("calculate_total_rent");
    },

    end_date(frm) {
        frm.trigger("calculate_total_rent");
    },

    plan_type(frm) {
        frm.trigger("calculate_total_rent");
    },

    calculate_total_rent(frm) {
        let items = frm.doc.items || [];
        let plan = frm.doc.plan_type;
        let start = frm.doc.start_date;
        let end = frm.doc.end_date;

        if (!start || !end || !plan) return;

        let days = frappe.datetime.get_diff(end, start);
        if (days < 0) {
            frappe.msgprint("End date cannot be before Start date.");
            return;
        }

        let total = 0;
        items.forEach(row => {
            if (plan === "Daily") {
                total += (row.daily_rate || 0) * days;
            } else if (plan === "Weekly") {
                total += (row.weekly_rate || 0) * (days / 7);
            } else if (plan === "Monthly") {
                total += (row.monthly_rate || 0) * (days / 30);
            }
        });

        frm.set_value("total_rent", total);
    }
});


frappe.ui.form.on("Rental Contract Item", {
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);

        if (!row.item_code) return;

        frappe.db.get_doc("Item", row.item_code)
            .then(doc => {
                row.daily_rate = doc.rental_daily_rate;
                row.weekly_rate = doc.rental_weekly_rate;
                row.monthly_rate = doc.rental_monthly_rate;
                frm.refresh_field("items");
                frm.trigger("calculate_total_rent");
            });
    },

    serial_no(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);

        if (!row.serial_no) return;

        frappe.db.get_doc("Serial No", row.serial_no)
            .then(sn => {
                row.condition_at_checkout = sn.rental_condition;
                frm.refresh_field("items");
            });
    }
});
