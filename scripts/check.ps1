param([switch]$Package)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = $null
$candidates = @(
    (Join-Path $projectRoot '.venv\Scripts\python.exe'),
    (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
)
foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $pythonExe = $candidate
        break
    }
}
if (-not $pythonExe) {
    foreach ($name in @('python', 'python3', 'py')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if ($command -and $command.Source -notlike '*\Microsoft\WindowsApps\*') {
            $pythonExe = $command.Source
            break
        }
    }
}
if (-not $pythonExe) { throw 'Python 3.10+ is required. Install Python or create .venv first.' }
Push-Location -LiteralPath $projectRoot
try {
    & $pythonExe -X utf8 scripts/verify.py
    if ($LASTEXITCODE -ne 0) { throw 'Offline verification failed.' }
    if ($Package) {
        & $pythonExe -X utf8 scripts/package_submission.py
        if ($LASTEXITCODE -ne 0) { throw 'Packaging failed.' }
    }
    & $pythonExe -X utf8 scripts/package_submission.py --check
    if ($LASTEXITCODE -ne 0) { throw 'Submission ZIP/checksums verification failed.' }
} finally {
    Pop-Location
}
