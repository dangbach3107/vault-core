$ErrorActionPreference = "Stop"
$repositoryPath = Split-Path -Parent $PSScriptRoot
Push-Location $repositoryPath
try {
    & .\.venv\Scripts\python.exe -m backend.dev_database
    if ($LASTEXITCODE -ne 0) { throw "Database setup failed. See the message above." }
} finally {
    Pop-Location
}
