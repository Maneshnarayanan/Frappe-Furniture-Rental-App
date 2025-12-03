# Furniture Rental for ERPNext

Furniture Rental is a complete rental management module built on top of ERPNext & Frappe Framework.  
It enables businesses to manage rental contracts, item delivery, returns, maintenance, settlements, and stock movement with automated workflows and business logic.

---

## 🚀 Features

### ✔ Rental Contract Management
- Create rental contracts with items, serial numbers, rental plans, and rental periods.
- Supports daily, weekly, and monthly rental rates.
- Auto-calculates total rent based on plan and duration.
- Tracks deposit amount, conditions, and customer details.
- Automatically marks rented serial items as **Out on Rent**.

### ✔ Delivery Workflow
- Automatic Delivery Assignment creation on contract submission.
- Serial numbers update to **Out on Rent** status.
- Asset Movement Logs track every movement of rental items.

### ✔ Rental Return Workflow
- Record return date, conditions, serial numbers, and notes.
- Auto-calculates late days & late fees.
- Automatically creates Maintenance Requests for damaged items.
- Updates serial items back to **Available** or **Under Maintenance**.

### ✔ Maintenance Management
- Auto-generated maintenance requests for damaged returns.
- Serial items locked during maintenance (status: Under Maintenance).
- Released only when maintenance is completed.

### ✔ Settlement / Final Billing
- Complete settlement summary including:
  - Total Rent
  - Deposit
  - Late Fees
  - Damage Charges
  - Cleaning Charges
  - Missing Item Charges
- Calculates net payable or refundable balance.
- Marks rental contract as **Completed** on settlement.

### ✔ Reports
- **Item Availability**
- **Active Rentals**
- **Pending Returns**
- **Items Out on Rent (optional)**

### ✔ Scheduler Jobs
- Daily overdue checker.
- Automatic return reminders.
- Hourly sync of serial number status.

### ✔ Workspace (Dashboard)
A dedicated Furniture Rental workspace with:
- Quick shortcuts
- Operational reports
- Links to inventory and customer data

---

## 📦 Installation

1. Go to your Frappe bench folder:
```bash
cd frappe-bench
