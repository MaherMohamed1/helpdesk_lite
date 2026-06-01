# HelpDesk Lite

A minimal internal ticketing system built with Flask, SQLite, and plain HTML.

## Overview

HelpDesk Lite is a lightweight ticketing system designed for internal team support. It provides essential features for submitting and tracking support tickets with a clean, minimal interface.

## Project Structure

```
helpdesk_lite/
├── helpdesk/
│   ├── server/
│   │   └── main.py              # Flask application (routes + database logic)
│   ├── templates/
│   │   ├── login.html           # User login page
│   │   ├── signup.html          # User registration page
│   │   ├── submit.html          # Ticket submission form
│   │   ├── ticket_detail.html   # Individual ticket view
│   │   └── tickets.html         # Ticket list & dashboard
│   ├── static/
│   │   └── style.css            # Application styles
│   ├── requirements.txt         # Python dependencies
│   ├── Procfile                 # Deployment configuration
│   ├── start_dev.ps1            # Development startup script (PowerShell)
│   ├── start_prod.ps1           # Production startup script (PowerShell)
│   ├── run_prod.py              # Production runner
│   ├── smoke_test.py            # Smoke tests
│   └── README.md                # Detailed setup guide
└── README.md                    # This file
```

## Quick Start

### Prerequisites

- Python 3.x
- pip

### Installation

1. **Create and activate a virtual environment:**

```powershell
cd helpdesk
python -m venv .venv
.\.venv\Scripts\Activate
```

2. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

3. **Run the application:**

```powershell
python server/main.py
```

The application will start on `http://localhost:5000`

## Development

### Using the start script:

```powershell
cd helpdesk
.\start_dev.ps1
```

### Running tests:

```powershell
python smoke_test.py
```

## Deployment

### Production deployment:

```powershell
cd helpdesk
.\start_prod.ps1
```

Or use the Procfile:

```bash
heroku create
git push heroku main
```

## Database

The application uses SQLite for data persistence. The database file (`helpdesk.db`) is automatically created on first run.

## Features

- **User Authentication**: Login and signup functionality
- **Ticket Management**: Submit, view, and track support tickets
- **Responsive UI**: Works on desktop and mobile browsers
- **Minimal Stack**: No complex frameworks, just Flask and SQLite

## Troubleshooting

For detailed setup instructions and troubleshooting, see [helpdesk/README.md](helpdesk/README.md).

## License

MIT
