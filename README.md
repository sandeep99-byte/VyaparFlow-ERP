# VyaparFlow ERP (MVP)

A beginner-friendly Django starter for a small-business ERP. It includes shop registration, login, product/stock records, customers, expenses, single-product sales invoices, stock deduction, low-stock warnings, dashboard metrics, and printable invoices.

## Requirements
- Python 3.10 or newer
- Internet only for installing Django and loading Bootstrap CDN in the UI
- VS Code (optional)

## Run on Windows PowerShell
Open PowerShell in this project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ and create a shop account. You can also open http://127.0.0.1:8000/admin/ after creating a superuser:

```powershell
python manage.py createsuperuser
```

## Current MVP scope
- Register/login/logout
- One shop per user
- Products and stock
- Customers
- Expenses
- One product per invoice
- Automatically deduct stock when a sale is created
- Dashboard, low-stock list, and print/save invoice as PDF through browser

## Important limitations
This is a learning MVP, not production-ready accounting software. It does not yet implement GST returns/compliance, purchase ledger, multiple line items per invoice, refunds, payment history, backups, audit logs, full profit calculation, or hardened production security. The dashboard's estimated amount is sales minus recorded expenses, not accounting profit. Before real business use, add tests, stronger invoice numbering, database backups, HTTPS, production secrets/settings, proper payment and inventory ledgers, and accounting/tax review.

## Next milestones
1. Add edit/delete and search for products/customers.
2. Add multi-item invoices and purchase/stock movement ledger.
3. Add payments and customer outstanding balances.
4. Add GST configuration and validated invoice formats.
5. Add PWA manifest/service worker for installable Android experience.
6. Deploy with a production database and tenant-isolation tests.
