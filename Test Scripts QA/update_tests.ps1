# --- Configuration ---
# Automatically find the Git Root Directory
# (Walks up the folder tree until it finds the .git folder)
$CurrentDir = $PSScriptRoot
$RepoPath = $CurrentDir

while (-not (Test-Path "$RepoPath\.git") -and $RepoPath -ne (Get-Item $RepoPath).Root) {
    $RepoPath = (Get-Item $RepoPath).Parent.FullName
}

if (-not (Test-Path "$RepoPath\.git")) {
    Write-Host "Error: Could not find .git folder. Is this a cloned repository?" -ForegroundColor Red
    exit
}

Write-Host "Git Repository found at: $RepoPath"
Set-Location $RepoPath

# --- Logic ---

# 1. Fetch latest data from GitHub
#    This downloads the latest state without merging it yet.
Write-Host "Fetching latest scripts from GitHub..."
$FetchOutput = git fetch origin 2>&1

if (-not $?) {
    Write-Host "Error: Could not fetch from GitHub. Check internet connection." -ForegroundColor Red
    Write-Host "Details: $FetchOutput"
    # We exit here because if fetch failed, we can't reset.
    exit
}

# 2. Auto-Detect Branch Name (Main vs Master)
#    We check which one exists on the remote server.
if (git rev-parse --verify origin/main 2>$null) {
    $Branch = "main"
} elseif (git rev-parse --verify origin/master 2>$null) {
    $Branch = "master"
} else {
    Write-Host "Error: Could not detect 'main' or 'master' branch." -ForegroundColor Red
    exit
}

Write-Host "Target Branch Detected: $Branch"

# 3. Safety Check: Is Sikuli running?
#    We don't want to update files while a test is actively using them.
$SikuliRunning = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "sikulixide" }

if ($SikuliRunning) {
    Write-Host "Warning: Sikuli is currently running. Skipping update to prevent crash." -ForegroundColor Yellow
    exit
}

# 4. Force Update (The "No Matter What" Fix)
#    'reset --hard' destroys local changes and makes the folder mirror GitHub.
Write-Host "Forcing local scripts to match origin/$Branch..."
git reset --hard "origin/$Branch"

# 5. Update Dependencies (Optional - specific to test scripts)
if (Test-Path "requirements.txt") {
    Write-Host "Checking for dependency updates..."
    python -m pip install -r requirements.txt
}

Write-Host "Test Scripts Updated Successfully."