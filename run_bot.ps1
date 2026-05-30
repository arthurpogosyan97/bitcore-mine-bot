$ErrorActionPreference = "Stop"

$BundledPython = "C:\Users\AZARTRAZE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Python = "python"

try {
    & $Python --version | Out-Null
} catch {
    if (Test-Path $BundledPython) {
        $Python = $BundledPython
    } else {
        throw "Python was not found. Install Python 3.12+ or run from an environment where python is available."
    }
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    & $Python -m venv .venv
}

Write-Host "Installing dependencies..."
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

Write-Host "Starting BitCore Mine..."
.\.venv\Scripts\python.exe main.py
if ($LASTEXITCODE -ne 0) {
    throw "Bot stopped with an error."
}
