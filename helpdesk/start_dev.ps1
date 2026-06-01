param(
    [switch]$Install
)

if ($Install) {
    python -m venv .venv
    if (Test-Path .venv\Scripts\Activate.ps1) {
        . .\.venv\Scripts\Activate.ps1
    }
    pip install -r requirements.txt
}

if (Test-Path .venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}

python server/main.py
