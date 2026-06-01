# Local Development Guide

## Quick Start

### Prerequisites
- Python 3.9+
- pip or conda

### Option 1: Using Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/helpdesk_lite.git
cd helpdesk_lite

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
cd helpdesk
pip install -r requirements.txt

# Copy environment template
copy ..\env.example .env

# Run development server
python server/main.py
```

The application will be available at `http://localhost:5000`

### Option 2: Using Docker

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/helpdesk_lite.git
cd helpdesk_lite

# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t helpdesk-lite .
docker run -p 5000:5000 helpdesk-lite
```

The application will be available at `http://localhost:5000`

## Running Tests

```bash
cd helpdesk
python ../smoke_test.py
```

## File Structure

```
helpdesk_lite/
├── .github/              # GitHub configuration
│   ├── workflows/        # CI/CD workflows
│   └── ISSUE_TEMPLATE/   # Issue templates
├── helpdesk/             # Main application
│   ├── server/
│   │   └── main.py       # Flask app
│   ├── templates/        # HTML templates
│   ├── static/           # CSS, JS, images
│   └── requirements.txt   # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── CONTRIBUTING.md       # Contributing guidelines
├── SECURITY.md           # Security policy
├── LICENSE               # MIT License
└── README.md             # Project documentation
```

## Development Tips

1. **Hot Reload**: Set `FLASK_DEBUG=1` in `.env` for automatic reloading
2. **Database Reset**: Delete `helpdesk/helpdesk.db` to reset the database
3. **Debugging**: Use Flask's built-in debugger with `FLASK_DEBUG=1`

## Common Issues

### Port Already in Use
If port 5000 is in use, set a different port:
```powershell
$env:PORT=5001
python helpdesk/server/main.py
```

### Module Not Found
Make sure you've activated the virtual environment and installed dependencies:
```bash
pip install -r helpdesk/requirements.txt
```

### Database Errors
If you encounter database errors, delete the database file and restart:
```bash
rm helpdesk/helpdesk.db
python server/main.py
```

## Need Help?

- Check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Open an [issue](https://github.com/YOUR-USERNAME/helpdesk_lite/issues)
- See the main [README.md](README.md)
