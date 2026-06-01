param(
    [int]$Port = 8000,
    [string]$Host = "0.0.0.0",
    [switch]$Install
)

if ($Install) {
    python -m venv .venv
    if (Test-Path .venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }
    pip install -r requirements.txt
}

if (Test-Path .venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }

$env:PORT = $Port
$env:HOST = $Host

python run_prod.py
