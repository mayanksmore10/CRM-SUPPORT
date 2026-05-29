# Datastraw Support CRM

A full-stack customer support ticketing system built with **Python + FastAPI**, **SQLite**, and **HTML + Tailwind CSS**.

## Features

- **Create Tickets** — Customer name, email, subject, description with auto-generated ticket ID
- **List All Tickets** — Clean table view with ID, name, subject, status, and date
- **Live Search** — Search across names, emails, ticket IDs, and descriptions as you type
- **Filter by Status** — Filter by Open, In Progress, or Closed
- **View & Update Tickets** — Detailed ticket view with status updates and notes/comments

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML + Tailwind CSS (CDN) |
| Templates | Jinja2 |
| Deployment | Railway.app |

## Project Structure

```
crm-system/
├── main.py            # FastAPI app + page routes
├── database.py        # SQLite setup, ORM models
├── schemas.py         # Pydantic request/response schemas
├── routes/
│   └── tickets.py     # All 4 API endpoints
├── templates/
│   ├── base.html      # Shared layout (sidebar, topbar)
│   ├── index.html     # Ticket list + search + filter
│   ├── create.html    # New ticket form
│   └── detail.html    # Ticket detail + update + notes
├── static/            # Static assets (if any)
├── requirements.txt
├── Procfile           # Railway deployment
├── .env.example
└── .gitignore
```

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/datastraw-crm.git
cd datastraw-crm
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/tickets` | Create a new ticket |
| GET | `/api/tickets` | List all tickets (with optional `?status=` & `?search=`) |
| GET | `/api/tickets/{ticket_id}` | Get single ticket with notes |
| PUT | `/api/tickets/{ticket_id}` | Update status or add a note |

## Deployment (Railway.app)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo
4. Railway auto-detects the `Procfile` and deploys

## Database Schema

**tickets** — `id`, `ticket_id`, `customer_name`, `customer_email`, `subject`, `description`, `status`, `created_at`, `updated_at`

**notes** — `id`, `ticket_id` (FK), `note_text`, `created_at`
