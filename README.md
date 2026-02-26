# Katrina's Electronics — Point of Sale System

A full-stack **Point of Sale (POS) and shop management web application** built to demonstrate my proficiency in **Django**, **PostgreSQL**, **HTMX**, **TailwindCSS**, and modern Python web development practices.

The project simulates a real-world electronics retail system for a fictional shop — *Katrina's Electronics* — covering everything from inventory and sales to worker management and financial reporting.

---

## Skills Demonstrated

- **Django (v6.0)** — Models, views, URL routing, middleware, template engine, Django Admin, custom adapters
- **PostgreSQL** — Relational data modelling, migrations, ForeignKey/UUID primary keys
- **HTMX** — Partial page updates and AJAX-like interactions without writing JavaScript frameworks
- **jQuery** — Dynamic cart UI, real-time total calculations, discount toggling
- **TailwindCSS + DaisyUI** — Responsive, component-driven frontend styling
- **django-allauth** — Email-based authentication with mandatory email verification
- **Cloudinary** — Cloud file storage for generated receipt PDFs
- **ReportLab** — Programmatic PDF receipt generation
- **Docker Compose** — Containerised local development database
- **django-environ** — Environment variable management with `.env` support
- **WhiteNoise** — Static file serving

---

## What the Application Does

- **Sales** — Complete sales transactions with Cash; auto-generates a PDF receipt per sale
- **Product Inventory** — Manage electronics stock (phones, accessories, etc.) with buy/sell pricing, discounts, stock counts, and IMEI tracking for phone sales
- **Worker Management** — Create staff profiles, assign roles (owner / manager / staff), activate or deactivate accounts, and track individual sales
- **Financial Dashboard** — Revenue, profit, and cash flow breakdowns by period with a searchable Cash Tracker
- **Role-Based Access Control** — Views and features gated by worker role via custom middleware
- **Cart System** — Fully interactive cart with real-time price/discount updates using HTMX and jQuery

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 (Python) |
| Database | PostgreSQL 15 |
| Frontend | Django Templates, TailwindCSS, DaisyUI |
| Interactivity | HTMX, jQuery |
| Auth | django-allauth |
| File Storage | Cloudinary |
| PDF Generation | ReportLab |
| Dev Database | Docker Compose |

---

## Project Structure

```
Katrina_POS/
├── compose.yaml          # Docker Compose — local Postgres container
└── src/
    ├── manage.py
    ├── dn_core/          # Project settings & root URL config
    ├── dn_auth/          # Custom allauth adapter
    ├── dn_home/          # Dashboard, homepage & middleware
    ├── dn_products/      # Product models, inventory & stock
    ├── dn_sales/         # Sales, cart, receipts & finance reporting
    ├── dn_workers/       # Worker profiles, roles & activation
    ├── dn_utilities/     # Shared utilities
    ├── templates/        # Global base templates & includes
    ├── static/           # Project-level static assets
    └── theme/            # TailwindCSS theme app
```

---

## Running Locally

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js (for Tailwind CSS compilation)

### 1. Start the database

```bash
docker compose up -d
```

Starts a local PostgreSQL container on port **5433**:
- **DB:** `katrinadb` | **User:** `katrinauser` | **Password:** `katrina_12345`

### 2. Set up the Python environment

```bash
python -m venv dnvenv
source dnvenv/bin/activate      # Windows: dnvenv\Scripts\activate
pip install -r src/requirements.txt
```

### 3. Configure environment variables

Create `src/.env`:

```env
SECRET_KEY=your-secret-key-here
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_PASSWORD=your-email-password
CLOUD_NAME=your-cloudinary-cloud
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
```

### 4. Migrate, create superuser & build CSS

```bash
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py tailwind install
python manage.py tailwind build
```

### 5. Run the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## URL Structure

| URL | Description |
|---|---|
| `/` | Homepage / dashboard |
| `/accounts/` | Login, signup, logout |
| `/products/` | Product inventory |
| `/sales/` | Sales & finance |
| `/workers` | Staff management |
| `/dn_admin/` | Django admin panel |
