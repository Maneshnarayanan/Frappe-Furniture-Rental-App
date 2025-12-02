// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Settlement", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.trigger("pull_contract_details");
        }

          if (frm.doc.rental_contract) {
            frm.add_custom_button("View Contract", () => {
                frappe.set_route("Form", "Rental Contract", frm.doc.rental_contract);
            }, "View");

            frm.add_custom_button("View Returns", () => {
                frappe.set_route("List", "Rental Return", {
                    rental_contract: frm.doc.rental_contract
                });
            }, "View");
        }

        if (frm.doc.customer) {
            frm.add_custom_button("Customer Ledger", () => {
                frappe.set_route("query-report", "General Ledger", {
                    party: frm.doc.customer,
                    party_type: "Customer"
                });
            }, "View");
        }
    },

    late_fee(frm) { frm.trigger("calculate_totals"); },
    damage_charges(frm) { frm.trigger("calculate_totals"); },
    cleaning_charges(frm) { frm.trigger("calculate_totals"); },
    missing_item_charges(frm) { frm.trigger("calculate_totals"); },

    calculate_totals(frm) {
        let charges = 
            (frm.doc.late_fee || 0) +
            (frm.doc.damage_charges || 0) +
            (frm.doc.cleaning_charges || 0) +
            (frm.doc.missing_item_charges || 0);

        frm.set_value("total_charges", charges);

        let deposit = frm.doc.deposit_received || 0;

        if (charges > deposit) {
            frm.set_value("net_payable", charges - deposit);
            frm.set_value("net_receivable", 0);
        } else {
            frm.set_value("net_receivable", deposit - charges);
            frm.set_value("net_payable", 0);
        }
    },

    pull_contract_details(frm) {
        if (!frm.doc.rental_contract) return;

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Rental Contract",
                name: frm.doc.rental_contract
            },
            callback(r) {
                if (!r.message) return;
                let doc = r.message;

                frm.set_value("customer", doc.customer);
                frm.set_value("deposit_received", doc.deposit_amount);
                frm.set_value("total_rent_amount", doc.total_rent);
                frm.set_value("contract_period", `${doc.start_date} → ${doc.end_date}`);
            }
        });
    }
});
