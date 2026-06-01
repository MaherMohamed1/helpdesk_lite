# HelpDesk Lite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal internal ticketing system — Flask + SQLite + plain HTML.

**Features:**
- 🔐 User authentication (login/signup)
- 🎫 Ticket management (create, view, update status)
- 📊 Dashboard with ticket overview
- 🎨 Responsive UI design
- ⚡ Minimal dependencies, fast setup

## Folder Structure

```
helpdesk/
├── server/
│   └── main.py          # Flask app (all routes + DB logic)
├── templates/
│   ├── tickets.html     # Ticket list + dashboard
│   └── submit.html      # Submit ticket form
├── static/
│   └── style.css        # All styles
├── requirements.txt
└── helpdesk.db          # Auto-created on first run
```

## Setup & Run

### 1. Create a Python virtual environment (recommended)

From the repository root (PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r helpdesk/requirements.txt
```

Or, change into the `helpdesk` folder and install there:

```powershell
cd helpdesk
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Start the development server

Run from inside the `helpdesk` folder (recommended):

```powershell
cd helpdesk
python server/main.py
```

Or from the repository root (explicit path):

```powershell
python helpdesk/server/main.py
```

Notes:
- Default development port is `8000`. To change the port set the `PORT` environment variable (PowerShell): ` $env:PORT=5001 ` then run the command above.
- The app creates `helpdesk.db` automatically on first startup.

### 3. Run in production (Waitress)

From the repository root:

```powershell
python helpdesk/run_prod.py
# or using the waitress CLI (if installed):
waitress-serve --listen=:8000 server.main:app
```

You can set `PORT`, `HOST`, and `SECRET_KEY` environment variables before starting the server. Example (PowerShell):

```powershell
$env:PORT=8000; $env:HOST='0.0.0.0'; $env:SECRET_KEY='your-secret'
python helpdesk/run_prod.py
```

### Helper scripts (Windows PowerShell)

Two convenience scripts are included in the `helpdesk` folder:
- `start_dev.ps1` — creates/activates a venv (with `-Install`) and starts the dev server.
- `start_prod.ps1` — creates/activates a venv (with `-Install`) and runs `run_prod.py` with optional `-Port` and `-Host` params.

Example (from repo root):

```powershell
powershell -ExecutionPolicy Bypass -File .\helpdesk\start_dev.ps1 -Install
powershell -File .\helpdesk\start_prod.ps1 -Port 8000
```

### 4. Smoke test

Quick check (from repo root):

```powershell
python helpdesk/smoke_test.py
```

This queries `/`, `/login`, `/signup`, `/tickets`, and `/submit` on `http://127.0.0.1:8000`.

## Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
FLASK_ENV=development
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///helpdesk.db
HOST=localhost
PORT=5000
```

## Deployment

### Docker

If you have Docker installed, build and run the container:

```bash
docker build -t helpdesk-lite .
docker run -p 8000:8000 helpdesk-lite
```

### Heroku

Deploy using the included `Procfile`:

```bash
heroku create your-app-name
git push heroku main
```

### Cloud Platforms

The app is compatible with AWS, Azure, Google Cloud, and other platforms. Install dependencies and set the required environment variables before running.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/YOUR-USERNAME/helpdesk_lite/issues) on GitHub.

## Troubleshooting

- Error "can't open file 'server/main.py'": you likely ran `python server/main.py` from the repository root. Either `cd helpdesk` first or run `python helpdesk/server/main.py` from repo root.
- `ModuleNotFoundError: No module named 'waitress'`: install dependencies with `pip install -r requirements.txt` (run from `helpdesk` folder or `pip install -r helpdesk/requirements.txt` from repo root).
- If `helpdesk.db` is missing, start the app (it is auto-created by `init_db()` in `server/main.py`). Confirm the file exists at `helpdesk/helpdesk.db` after the first run.

---

## API Reference

| Method | Endpoint                       | Description                  |
|--------|--------------------------------|------------------------------|
| GET    | `/tickets`                     | List all tickets (HTML page) |
| POST   | `/tickets`                     | Create a ticket (form)       |
| POST   | `/tickets/<id>/assign`         | Assign ticket to a name      |
| POST   | `/tickets/<id>/status`         | Advance to next status step  |

## Status Flow

```
To Do  →  In Progress  →  In Review  →  Done
```

Notes:
- Manager users may set any status; regular users advance according to allowed transitions.

