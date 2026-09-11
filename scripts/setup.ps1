param([string]$PythonExecutable = '')

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
        throw 'Install Node.js 22.12+ and reopen PowerShell before running setup.'
    }
    if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
        if (-not $PythonExecutable) {
            $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
            $cachedPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
            if ($pythonCommand) { $PythonExecutable = $pythonCommand.Source }
            elseif (Test-Path -LiteralPath $cachedPython) { $PythonExecutable = $cachedPython }
            else { throw 'Python not found. Install Python 3.12 or pass -PythonExecutable with its full path.' }
        }
        & $PythonExecutable -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
    }
    & ./.venv/Scripts/python.exe -m pip install -r backend/requirements.lock.txt --disable-pip-version-check
    if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }
    if (-not (Test-Path -LiteralPath '.env')) {
        Copy-Item -LiteralPath '.env.example' -Destination '.env'
    }
    Push-Location frontend
    try {
        & npm.cmd ci --cache ../.tmp/npm-cache --no-audit --no-fund
        if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    }
    finally { Pop-Location }
    Write-Output 'Setup complete. See README.md for the two server commands.'
}
finally { Pop-Location }
