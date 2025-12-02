# --- Configuration ---
# Get the directory where this script is running (The Scripts folder)
$ScriptDir = $PSScriptRoot
# Go up one level if this script is inside a "Scripts" subfolder, 
# but the Repo Root is "Test Scripts QA"
$RepoPath = (Get-Item $ScriptDir).Parent.FullName 

# Change this to your Test Scripts Branch
$Branch = "master" 

# --- Logic ---
Set-Location $RepoPath

# 1. Fetch latest data (Public Repo - No Token needed)
$FetchOutput = git fetch origin 2>&1

if (-not $?) {
    Write-Host "Error: Could not fetch from GitHub." -ForegroundColor Red
    exit
}

# 2. Compare Local vs Remote
try {
    $LocalHash = git rev-parse HEAD
    $RemoteHash = git rev-parse "origin/$Branch"
}
catch {
    Write-Host "Error: Could not read branch '$Branch'." -ForegroundColor Red
    exit
}

if ($LocalHash -eq $RemoteHash) {
    # Up to date - do nothing
}
else {
    Write-Host "New Test Scripts detected! ($LocalHash -> $RemoteHash)"
    
    # 3. Safety Check: Is a Sikuli test currently running?
    #    We look for the Java process used by Sikuli
    $SikuliRunning = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "sikulixide" }

    if ($SikuliRunning) {
        Write-Host "Warning: A test is currently running. Skipping update to prevent crash." -ForegroundColor Yellow
        # We DO NOT force kill tests, as that might corrupt results. 
        # We wait for the next scheduled run when the machine is idle.
        exit
    }

    # 4. Force Update (Reset to match GitHub)
    Write-Host "Downloading new test scripts..."
    git reset --hard "origin/$Branch"

    Write-Host "Test Scripts Updated Successfully."
}